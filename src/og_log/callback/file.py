from pathlib import Path
from og_log.callbacks import LoggerCallback

class FileLoggerCallback(LoggerCallback):
    """Write logs to a file
    
    Args:
        filepath: Path to log file
        mode: 'a' (append) or 'w' (overwrite), default 'a'
        buffer_size: Buffer size in bytes, default 1 (line buffered)
        encoding: File encoding, default 'utf-8'
    """
    def init(self):
        self.filepath = self.kwargs['filepath']
        mode = self.kwargs.get('mode', 'a')
        buffer_size = self.kwargs.get('buffer_size', 1)
        encoding = self.kwargs.get('encoding', 'utf-8')
        
        # Create parent directory if needed
        Path(self.filepath).parent.mkdir(parents=True, exist_ok=True)
        
        self.file = open(self.filepath, mode, buffering=buffer_size, encoding=encoding)

        self.file = open(
            self.filepath, mode, 
            buffering=buffer_size, 
            encoding=encoding,
            errors='replace'
        )
    
    def __call__(self, log_str):
        self.file.write(log_str + '\n')
    
    def close(self):
        if hasattr(self, 'file') and not self.file.closed:
            self.file.close()

class RotatingFileLoggerCallback(LoggerCallback):
    """Write logs to a file with rotation when size exceeded
    
    Args:
        filepath: Path to log file
        max_bytes: Max file size before rotation, default 10MB
        backup_count: Number of backup files to keep, default 5
        buffer_size: Buffer size, default 1 (line buffered)
        encoding: File encoding, default 'utf-8'
    """
    def init(self):
        self.filepath = Path(self.kwargs['filepath'])
        self.max_bytes = self.kwargs.get('max_bytes', 10 * 1024 * 1024)
        self.backup_count = self.kwargs.get('backup_count', 5)
        self.buffer_size = self.kwargs.get('buffer_size', 1)
        self.encoding = self.kwargs.get('encoding', 'utf-8')
        
        self.filepath.parent.mkdir(parents=True, exist_ok=True)

        self.file = open(
            self.filepath, 'a', 
            buffering=self.buffer_size, 
            encoding=self.encoding,
            errors='replace'
        )

    def __call__(self, log_str):
        if self.file.tell() > self.max_bytes:
            self._rotate()
        
        self.file.write(log_str + '\n')
        self.file.flush() 
    
    def _rotate(self):
        self.file.close()
        
        # Rotate backup files (app.log.5 → deleted, app.log.4 → app.log.5, etc.)
        for i in range(self.backup_count - 1, 0, -1):
            src = Path(str(self.filepath) + f'.{i}')    
            dst = Path(str(self.filepath) + f'.{i+1}')  
            if src.exists():
                if dst.exists():
                    dst.unlink() 
                src.rename(dst)
        
        # Move current to .1 (app.log → app.log.1)
        if self.filepath.exists():
            backup = Path(str(self.filepath) + '.1') 
            if backup.exists():
                backup.unlink()
            self.filepath.rename(backup)
        
        # Reopen fresh file
        self.file = open(
            self.filepath, 'a', 
            buffering=self.buffer_size, 
            encoding=self.encoding,
            errors='replace'
        )
    
    def close(self):
        if hasattr(self, 'file') and not self.file.closed:
            self.file.close()
