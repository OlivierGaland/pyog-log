class LoggerCallback:
    def __init__(self,**kwargs):
        self.kwargs = kwargs
        self.init()

    def init(self):
        raise NotImplementedError
    
    def __call__(self, log_str):
        raise NotImplementedError
    
    def close(self):
        raise NotImplementedError
    
