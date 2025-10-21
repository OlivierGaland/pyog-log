# https://packaging.python.org/en/latest/guides/distributing-packages-using-setuptools/
# https://packaging.python.org/en/latest/tutorials/packaging-projects/
#
# https://pypi.org/classifiers/
#
# build : python -m build
# upload :
# twine check dist/*

import os,sys
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'src'))
from og_log import LOG,LEVEL,LoggerCallback,ColoredConsoleCallback,FileLoggerCallback,ConsoleCallback,RotatingFileLoggerCallback
    
class TestLoggerCallback(LoggerCallback):

    def init(self):
        pass

    def __call__(self, log_str):
        if not self.kwargs.get('exception',False):
            print("==> Test Callback : call : "+str(log_str))
        else:
            raise Exception("test exception")

    def close(self):
        print("==> Test Callback : closed")

def test_logger():
    LOG.debug("this is a debug log")
    LOG.info("this is a info log")
    LOG.warning("this is a warning log")
    LOG.error("this is a error log")
    LOG.fatal("this is a fatal log")
    LOG.temp("this is a temp log")

if __name__ == '__main__':

    [ console ] = LOG.start(callbacks=ConsoleCallback())

    test_logger()

    test1 = LOG.register_cb(TestLoggerCallback(filepath='/tmp/app.log'))
    test_logger()

    test2 = LOG.register_cb(TestLoggerCallback(filepath='/tmp/app.log',exception=True))
    LOG.remove_cb(test1)
    LOG.remove_cb(console)    
    colored_console = LOG.register_cb(ColoredConsoleCallback())
    test_logger()

    LOG.remove_all_cb()
    LOG.register_cb(RotatingFileLoggerCallback(filepath='app.log',max_bytes=1000))
    for _ in range(10):
        test_logger()

    LOG.stop()







