import os
import sys
sys.path.append(os.getcwd()[:os.getcwd().find("Skulk")+len("Skulk")])

log = None
class ErrorBook:

    def __init__(self, logger):
        global log
        log = logger

    def handle(self, *args):
        log.error("*************************** ERROR **************************************")
        log.error("Error Statement {}".format(str(args[0])))
        log.error("Error Trace {}".format(str(args[1])))
        log.error("Funtion Parameter's:")
        log.error(args[2::])
        log.error("***************************** End **************************************")