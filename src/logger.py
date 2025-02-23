import logging
from datetime import datetime
import os

FILE=f"{datetime.now().strftime('%m_%d_%y_%H_%M_%S')}.log"
path=os.path.join(os.getcwd(),'logs',FILE)
os.makedirs(path,exist_ok=True)

FILE_PATH=os.path.join(path,FILE)

logging.basicConfig(
    filename=FILE_PATH,
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level=logging.INFO,
)
