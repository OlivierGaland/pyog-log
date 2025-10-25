# pyog-log

[![PyPI version](https://badge.fury.io/py/og-log.svg)](https://pypi.org/project/og-log/)
[![Python 3.7+](https://img.shields.io/badge/python-3.7+-blue.svg)](https://www.python.org/downloads/)

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
from og_log import LOG,LEVEL
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
LOG.start(callbacks=[ ColoredConsoleCallback() ]) # Set at start, accept single callback or list of callbacks (return list of callback object references)
hdl = LOG.register_cb(ColoredConsoleCallback())   # Add one callback dynamically (return callback object reference)  
LOG.remove_cb(hdl)                                # Remove one callback dynamically  
LOG.remove_all_cb()                               # Remove all callbacks  
```

## Customize display format :

You can customize the log line format using tokens. The default format is:
```python
"%date %level %thread %file %message"
```

### Setting custom format:
```python
from og_log import LOG

# At start
LOG.start(format="%date.ms %level.short [%thread] %file - %message")

# Or dynamically
LOG.set_format("%date.s %level %message")
```

### Available tokens:

| Token | Description | Example Output |
|-------|-------------|----------------|
| `%date` | Full date with microseconds | `2025-10-25 14:30:45.123456` |
| `%date.us` | Date with microseconds (same as %date) | `2025-10-25 14:30:45.123456` |
| `%date.ms` | Date with milliseconds | `2025-10-25 14:30:45.123` |
| `%date.s` | Date with seconds | `2025-10-25 14:30:45` |
| `%level` | Level with symbol prefix | `  DBG` / `● WRN` |
| `%level.short` | Level name only (3 chars) | `DBG` / `WRN` |
| `%level.prefix` | Level with symbol prefix (same as %level) | `  DBG` / `● WRN` |
| `%level.suffix` | Level with symbol suffix | `DBG  ` / `WRN ●` |
| `%thread` | Thread name (12 chars padded) | `MainThread` |
| `%file` | Relative file path and line number | `src/main.py:42` |
| `%message` | The log message | Your log message |

### Format examples:
```python
# Minimal format
LOG.set_format("%level.short %message")
# Output: DBG Starting application

# Detailed format with milliseconds
LOG.set_format("%date.ms [%thread] %level %file - %message")
# Output: 2025-10-25 14:30:45.123 [MainThread] ● DBG src/main.py:42 - Starting application

# Custom text with tokens
LOG.set_format("[%date.s] <%level.short> %message")
# Output: [2025-10-25 14:30:45] <DBG> Starting application
```

**Note:** You can add custom text between tokens. The formatter will preserve spacing and special characters.


## Screenshots :

### Colored console
<img width="636" height="106" alt="image" src="https://github.com/user-attachments/assets/6ec0c154-7a97-4960-88b4-c3a0c2a416a9" />



