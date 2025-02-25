import os
import sys

# Get the absolute path of the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(PROJECT_ROOT)

from src.exception import CustomException
from src.logger import logging
import pandas as pd

from sklearn.model_selection import train_test_split
from dataclasses import dataclass

from src.components.data_transformation import DataTransformation
from src.components.data_transformation import DataTransformationConfig

@dataclass
class DataIngestionConfig:
    train_path:str = os.path.join('artifact','train.csv')
    test_path:str = os.path.join('artifact','test.csv')
    raw_path:str = os.path.join('artifact','data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config=DataIngestionConfig
    
    def initiate_data_ingestion(self):
        logging.info('You Have Entered DataIngestion method or component')
        try:
            df=pd.read_csv('notebook/data/StudentsPerformance.csv')
            logging.info('Read the dataset using pandas')

            os.makedirs(os.path.dirname(self.ingestion_config.train_path),exist_ok=True)

            df.to_csv(self.ingestion_config.raw_path,index=False,header=True)

            logging.info('Train-Test Split')
            train_split,test_split=train_test_split(df,test_size=.30,random_state=2)

            train_split.to_csv(self.ingestion_config.train_path,index=False, header=True)
            test_split.to_csv(self.ingestion_config.test_path,index=False, header=True)

            logging.info('Data Ingestion Process Completed')

            return(
                self.ingestion_config.train_path,
                self.ingestion_config.test_path
            )
        
        except Exception as e:
            raise CustomException(e,sys)

if __name__=="__main__":
    obj=DataIngestion()
    train_data,test_data=obj.initiate_data_ingestion()
    
    data_transformation=DataTransformation()
    train_arr,test_arr,_=data_transformation.initiate_data_transformation(train_data,test_data)