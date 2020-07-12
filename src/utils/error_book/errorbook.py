from src.main.skulk_objects import SkulkObject as sb
import sys
sys.path.append(sb.skulk_path)

Log = None
class ErrorBook:
    def __init__(self):
        global log
        log = sb.log

    def handle(self, *args):
        log.error("*************************** ERROR **************************************")
        log.error("Error Statement {}".format(str(args[0])))
        log.error("Error Trade {}".format(str(args[1])))
        log.error("Funtion Parameter's:")
        log.error(args[2::])
        log.error("***************************** End **************************************")