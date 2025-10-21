# pyog-log
Simple python logger (multithreading capable)

## Installation :

pip install og-log [-U]

use -U for upgrade from previous version

## Usage (basic) :

```python
from og_log import LOG  
LOG.start()  
LOG.debug("Starting application")  
LOG.stop()  
```

There are 6 level of logging callable with LOG.xxx :  
debug,info,warning,error,fatal : standard lines (by priority)  
temp : for temporary lines (always visible, max priority, DEL tag to not commit)  

You can set priority (default is LEVEL.debug): 
```python 
LOG.start(level=LEVEL.warning)  # Show all traces >= LEVEL.warning , set at start  
LOG.level(LEVEL.error)          # Change the priority dynamically  
```

## Callbacks :

It works with one or more logging callbacks you can import.  
If none is defined at start the ConsoleCallback is default one (standard output display).  

### Built-in callbacks :  

Check code in /callback for constructor parameters

```python
from og_log import ColoredConsoleCallback
```

| Callback | Description | Key Parameters |
|----------|-------------|----------------|
| `ConsoleCallback` | Plain console output | `stream` (default: stdout) |
| `ColoredConsoleCallback` | ANSI colored console | `force_colors`, `stream` |
| `FileLoggerCallback` | Simple file logger | `filepath`, `mode`, `encoding` |
| `RotatingFileLoggerCallback` | Rotating file with size limit | `filepath`, `max_bytes`, `backup_count` , `encoding` |
| `UDPLoggerCallback` | Send logs via UDP | `host`, `port` |


### Custom callback example :

You can define your own callback inheriting from base class LoggerCallback (check callback dir for built-in examples)  

```python
from og_log import LoggerCallback

class EmailCallback(LoggerCallback):
    def init(self):
        self.recipient = self.kwargs['email']
    
    def __call__(self, log_str):
        if ' FTL ' in log_str:     # FATAL
            send_email(self.recipient, log_str)
    
    def close(self):
        pass

LOG.register_cb(EmailCallback(email='admin@example.com'))
```

### Registering/Unregistering callbacks :  

```python
LOG.start(callbacks=[ ColoredConsoleCallback() ]) # Set at start, accept single callback or list of callbacks
LOG.register_cb(ColoredConsoleCallback())         # Add one callback dynamically (return callback object reference)  
LOG.remove_cb(cb_obj_reference)                   # Remove one callback dynamically  
LOG.remove_all_cb()                               # Remove all callbacks  
```

## Screenshots :




