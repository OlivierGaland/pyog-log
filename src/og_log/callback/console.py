import sys
from og_log.callbacks import LoggerCallback

class ConsoleCallback(LoggerCallback):
    """Plain console output (no colors) - compatible with old terminals"""
    
    def init(self):
        self.stream = self.kwargs.get('stream', sys.stdout)
    
    def __call__(self, log_str):
        print(log_str, file=self.stream)
        self.stream.flush()
    
    def close(self):
        pass
    
class ColoredConsoleCallback(LoggerCallback):
    """ANSI colored console output for modern terminals"""

    COLORS = {
        'DBG': '\033[37m',    # Blanc dim (gris moyen)
        'INF': '\033[97m',      # Blanc normal
        'WRN': '\033[33m',      # Jaune (attention)
        'ERR': '\033[38;5;208m', # Orange (problème sérieux)
        'FTL': '\033[91m',      # Rouge vif (critique)
        'DEL': '\033[96;1m',    # Cyan vif + BOLD (temporaire)
        'RESET': '\033[0m'
    }

    def init(self):
        self.stream = self.kwargs.get('stream', sys.stdout)
        self.force_colors = self.kwargs.get('force_colors', True)
        
        # Auto-detect if terminal supports colors
        self.use_colors = self.force_colors or (
            hasattr(self.stream, 'isatty') and 
            self.stream.isatty() and 
            sys.platform != 'win32'  # Or check for Windows Terminal
        )
    
    def __call__(self, log_str):
        if not self.use_colors:
            print(log_str, file=self.stream)
        else:
            # Find level in log string
            colored = log_str
            for level, color in self.COLORS.items():
                if f' {level} ' in log_str:
                    colored = f"{color}{log_str}{self.COLORS['RESET']}"
                    break
            print(colored, file=self.stream)
        
        self.stream.flush()
    
    def close(self):
        pass

