import sys
# from src.logger import logging
import os

# Get the absolute path of the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
sys.path.append(PROJECT_ROOT)

# Now import the logger module
from src.logger import logging


# Giving a custom error message
def error_message_detail(error,error_detail:sys):
    _,_,exc_tb=error_detail.exc_info() # gives the 3rd info (whcih is asked in _,_, format) and is stored in exc_tb
    file_name=exc_tb.tb_frame.f_code.co_filename # Creating file where exc_tb will be stored
    error_message="You have an error in python script [{0}], in line number [{1}], where error is: [{2}]".format(
        file_name,exc_tb.tb_lineno,str(error) # 0,1,2 respectively 
    )
    return error_message

# Integrating the message and replacing it with standard message
class CustomException(Exception):
    def __init__(self,error_message,error_detail:sys):
        super().__init__(error_message)
        self.error_message=error_message_detail(error_message,error_detail=error_detail)

    def __str__(self):
        return self.error_message
    