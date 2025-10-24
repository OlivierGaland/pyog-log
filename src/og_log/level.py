from enum import Enum

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

