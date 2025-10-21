import os,sys
from enum import Enum
from datetime import datetime
from threading import RLock,current_thread
from inspect import currentframe

from .callbacks import LoggerCallback
from .callback.console import ConsoleCallback

class LEVEL(Enum):
    debug = (10,None,"DBG")
    info = (20,None,"INF")
    warning = (30,"●","WRN")
    error = (40,"■","ERR")
    fatal = (50,"▲","FTL")
    temp = (99,"!","DEL")

    @property
    def priority(self):
        return self.value[0]
    
    @property
    def symbol(self):
        return self.value[1]
    
    @property
    def name_str(self):
        return self.value[2]
    
    def __str__(self):
        prefix = self.symbol + ' ' if self.symbol else '  '
        return f"{prefix}{self.name_str:3s}"    

class Logger():
    instance = None
    def __init__(self):
        if Logger.instance is not None:
            raise Exception("Logger singleton already exist")
        else:
            Logger.instance = self
            Logger.instance.dolog = False
            Logger.instance.level = LEVEL.debug
            Logger.instance.callbacks = []
            Logger.instance.lock = RLock()
            Logger.instance.cwd = os.getcwd().lower()

    @staticmethod
    def Get():
        if Logger.instance is None: Logger()
        return Logger.instance

    def _format_line(self,level,obj):
        frame = currentframe()
        if frame is not None:
            while frame.f_back is not None and frame.f_back.f_code.co_filename.find('log.py') != -1: frame = frame.f_back
            if frame.f_back is not None: frame = frame.f_back
            line_nb = str(frame.f_lineno)
            full_path = frame.f_code.co_filename.lower()
            if full_path.startswith(Logger.instance.cwd + os.sep): file_name = frame.f_code.co_filename[len(Logger.instance.cwd)+1:]
            else: file_name = frame.f_code.co_filename
        else:
            file_name = "Logger"
            line_nb = "0"
        return ("{:26} {:5s} {:12s} ").format(str(datetime.now()),level,current_thread().name) + file_name + ":" + line_nb + " " + str(obj).replace('\n','\\n')

    def _try_callback(self, cb, log_str):
        try:
            cb(log_str)
            return True
        except Exception as e:
            try:
                print("Logger : Exception in callback "+str(cb.__class__.__name__)+", unregistering. Exception : "+str(e),file=sys.stderr)
                sys.stderr.flush()
                cb.close()
            except: pass
            return False

    def log(self,level,obj):
        if Logger.instance.dolog and Logger.instance.level.priority <= level.priority:
            log_str = self._format_line(level,obj)
            with Logger.instance.lock:
                Logger.instance.callbacks = [ cb for cb in Logger.instance.callbacks if self._try_callback(cb, log_str) ]
                if len(Logger.instance.callbacks) == 0:
                    try:
                        print("Logger : All callback unregistered, logging disabled",file=sys.stderr)
                        sys.stderr.flush()
                    except: pass
                    Logger.instance.dolog = False             

            
class LOG():

    @staticmethod
    def register_cb(callback_object):
        if not isinstance(callback_object, LoggerCallback): raise Exception("callback_object must be of type LoggerCallback")
        Logger.Get().callbacks.append(callback_object)
        return callback_object

    @staticmethod
    def remove_cb(callback_object):
        if not isinstance(callback_object, LoggerCallback): raise Exception("callback_object must be of type LoggerCallback")
        if callback_object not in Logger.Get().callbacks: raise Exception("callback_object not registered")
        Logger.Get().callbacks.remove(callback_object)
        callback_object.close()

    @staticmethod
    def remove_all_cb():
        for cb in Logger.Get().callbacks[:]:
            try: cb.close()
            except: pass
        Logger.Get().callbacks.clear()        

    @staticmethod
    def start(**kwargs):
        Logger.Get().level = kwargs.get('level',LEVEL.debug)
        callbacks = kwargs.get('callbacks',[ ConsoleCallback() ])
        if not isinstance(callbacks, list): callbacks = [ callbacks ]
        if len(callbacks) == 0: callbacks = [ ConsoleCallback() ]
        Logger.Get().callbacks = callbacks
        Logger.Get().dolog = True
        return Logger.Get().callbacks

    @staticmethod
    def stop():
        Logger.Get().dolog = False

    @staticmethod
    def level(level):
        Logger.Get().level = level
    
    @staticmethod
    def debug(obj):
        Logger.Get().log(LEVEL.debug,obj)
    
    @staticmethod
    def info(obj):
        Logger.Get().log(LEVEL.info,obj)

    @staticmethod
    def warning(obj):
        Logger.Get().log(LEVEL.warning,obj)

    @staticmethod
    def error(obj):
        Logger.Get().log(LEVEL.error,obj)

    @staticmethod
    def fatal(obj):
        Logger.Get().log(LEVEL.fatal,obj)

    @staticmethod
    def temp(obj):
        Logger.Get().log(LEVEL.temp,obj)
