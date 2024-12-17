import logging
import sys

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)  # set the minimum logging level

# create a console handler and set its level
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.DEBUG)

# create a formatter
formatter = logging.Formatter('%(asctime)s:%(filename)s:%(funcName)s:%(levelname)s :%(message)s')

# add the formatter to the console handler
console_handler.setFormatter(formatter)
logger.addHandler(console_handler)

access_log = logging.getLogger("tornado.access")
app_log = logging.getLogger("tornado.application")
gen_log = logging.getLogger("tornado.general")

access_log.addHandler(console_handler)
app_log.addHandler(console_handler)
gen_log.addHandler(console_handler)