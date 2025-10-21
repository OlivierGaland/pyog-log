import socket
from og_log.callbacks import LoggerCallback

class UDPLoggerCallback(LoggerCallback):
    """Send logs via UDP (e.g., to syslog, remote console)
    
    Args:
        host: Target hostname or IP
        port: Target port
    """
    def init(self):
        self.host = self.kwargs['host']
        self.port = self.kwargs['port']
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    
    def __call__(self, log_str):
        self.sock.sendto(log_str.encode('utf-8'), (self.host, self.port))
    
    def close(self):
        if hasattr(self, 'sock'):
            self.sock.close()
