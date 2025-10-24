import sys
from threading import RLock,Lock

from .callbacks import LoggerCallback
from .callback.console import ConsoleCallback
from .level import LEVEL
from .formatter import Formatter

class Logger():
    _init_lock = Lock()
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
            Logger.instance.formatter = Formatter()

    @staticmethod
    def Get():
        if Logger.instance is None:
            with Logger._init_lock:
                if Logger.instance is None: Logger()
        return Logger.instance

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
            log_str = self.formatter.format_line(level,obj)
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
    def set_format(line):
        Logger.Get().formatter.set_format(line)

    @staticmethod
    def start(**kwargs):
        Logger.Get().level = kwargs.get('level',LEVEL.debug)
        callbacks = kwargs.get('callbacks',[ ConsoleCallback() ])
        if not isinstance(callbacks, list): callbacks = [ callbacks ]
        if len(callbacks) == 0: callbacks = [ ConsoleCallback() ]
        Logger.Get().callbacks = callbacks
        format = kwargs.get('format',None)
        if format is not None: Logger.Get().set_format(format)
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



