import sys, os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()

LOG_FILE = r"./%s" % (os.getenv('LOG_FILE'))

def write_log(message):
    exc_type, exc_obj, exc_tb = sys.exc_info()
    fname = os.path.split(exc_tb.tb_frame.f_code.co_filename)[1]
    error = f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - File: {fname} - Line:{exc_tb.tb_lineno} - {message}'
    f = open(LOG_FILE, 'a')
    f.writelines(f'{error}\n')
    f.close()

def write_activity_log(message):
    log = f'{datetime.now().strftime("%d/%m/%Y %H:%M:%S")} - {message}'
    f = open(LOG_FILE, 'a')
    f.writelines(f'{log}\n')
    f.close()