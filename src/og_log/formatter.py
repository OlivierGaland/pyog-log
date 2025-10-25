import os, re, inspect
from datetime import datetime
from enum import Enum
from threading import current_thread

from .level import LEVEL

class FormatCallbackType(Enum):
    level = "Level"
    message = "Message"
    file = "File"
    standard = "Standard"
    text = "Text"

class Formatter():
    DEFAULT_FORMAT = "%date %level %thread %file %message"

    def __init__(self):
        self.set_format(Formatter.DEFAULT_FORMAT)

    def set_format(self,line):      # set line canvas (list of ordered method calls to format line)
        self.line_canvas = []

        tokens_found = re.findall(r'(%[\w\.]+)', line)  
        if len(tokens_found) == 0: raise Exception("No tokens found in format string")

        for token in tokens_found:
            if not line.startswith(token):
                text, line = line.split(token, 1)
                self.line_canvas.append((FormatCallbackType.text, self._token_text, {'text': text}))
                line = token + line

            tp, callback, kwargs = Formatter.TOKENS[token]
            if tp == FormatCallbackType.file: kwargs['cwd'] = os.getcwd()
            self.line_canvas.append((tp, callback, kwargs))
            line = line.split(token,1)[1]

        if len(line.rstrip()) > 0 :
            self.line_canvas.append((FormatCallbackType.text, self._token_text, {'text': line.rstrip()}))

    @staticmethod
    def _token_date(**kwargs):
        format_str = kwargs.get('format', '%Y-%m-%d %H:%M:%S.%f')
        padding = kwargs.get('padding', 0)
        date_string = datetime.now().strftime(format_str)
        if padding != 0: date_string = date_string[:padding]
        return date_string
    
    @staticmethod
    def _token_level(**kwargs):
        level = kwargs.get('level',LEVEL.temp)
        prefix = kwargs.get('prefix',True)
        if kwargs.get('symbol',True):
            if prefix: return "{:5s}".format(((level.symbol + ' ') if level.symbol else '  ')+level.name_str)
            else: return "{:5s}".format(level.name_str+((' ' + level.symbol) if level.symbol else '  '))
        else:
            return "{:3s}".format(level.name_str)

    @staticmethod
    def _token_thread(**kwargs):
        return "{:12s}".format(current_thread().name)

    @staticmethod
    def _token_file(**kwargs):
    
        frame = inspect.currentframe() 
        ignored_path_parts = (
            'og_log',
        )

        file_name , line_nb = "Logger", 0
        try:
            while frame:
                filename = frame.f_code.co_filename
                is_internal_logger_file = any(part in filename for part in ignored_path_parts)
                if not is_internal_logger_file:
                    file_name , line_nb =  os.path.relpath(frame.f_code.co_filename,kwargs.get('cwd','')), frame.f_lineno
                    break
                frame = frame.f_back
        except Exception as e:
            pass

        return "{}".format(file_name + ":" + str(line_nb))

    @staticmethod
    def _token_message(**kwargs):
        return kwargs.get('message','')
    
    @staticmethod
    def _token_text(**kwargs):      # for custom text in line format
        return kwargs.get('text','')

    def format_line(self,level,message):
        line = ""
        for tp,callback,kwargs in self.line_canvas:
            if tp == FormatCallbackType.level:
                line += callback(level=level,**kwargs)
            elif tp == FormatCallbackType.message:
                line += callback(message=message,**kwargs)
            elif tp == FormatCallbackType.standard or tp == FormatCallbackType.file:
                line += callback(**kwargs)
            elif tp == FormatCallbackType.text:
                line += callback(**kwargs)
        return line

Formatter.TOKENS = {
    '%date': (FormatCallbackType.standard,Formatter._token_date,{'format': '%Y-%m-%d %H:%M:%S.%f'}),
    '%date.us': (FormatCallbackType.standard,Formatter._token_date,{'format': '%Y-%m-%d %H:%M:%S.%f'}),
    '%date.ms': (FormatCallbackType.standard,Formatter._token_date,{'format': '%Y-%m-%d %H:%M:%S.%f', 'padding': -3}),
    '%date.s': (FormatCallbackType.standard,Formatter._token_date,{'format': '%Y-%m-%d %H:%M:%S.%f', 'padding': -7}),
    '%level' : (FormatCallbackType.level,Formatter._token_level,{}),
    '%level.short' : (FormatCallbackType.level,Formatter._token_level,{ 'symbol': False}),
    '%level.suffix' : (FormatCallbackType.level,Formatter._token_level,{ 'prefix': False}),
    '%level.prefix' : (FormatCallbackType.level,Formatter._token_level,{}),
    '%thread' : (FormatCallbackType.standard,Formatter._token_thread,{}),
    '%file' : (FormatCallbackType.file,Formatter._token_file,{}),
    '%message' : (FormatCallbackType.message,Formatter._token_message,{}),
}
