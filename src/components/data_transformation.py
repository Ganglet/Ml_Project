import sys
import os
from dataclasses import dataclass
import pandas as pd
import numpy as np
from sklearn.compose import ColumnTransformer
from sklearn.preprocessing import OneHotEncoder,StandardScaler
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline

# Get the absolute path of the project root directory
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../"))
sys.path.append(PROJECT_ROOT)

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class DataTransformationConfig:
    preprocessor_obj_file_path=os.path.join('artifact','preprocessor.pkl')

class DataTransformation:
    
    def __init__(self):
        self.data_transformation_config=DataTransformationConfig()

    def get_data_transformation_config(self):
        ''' This part is for data transformation '''

        try:
            numerical_features= ['reading score', 'writing score']
            categoriacal_features= ['gender', 'race/ethnicity', 'parental level of education', 'lunch', 'test preparation course']

            num_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='median')), # For handling missing values
                    ('scalar',StandardScaler()) # Standard Scaling
                ]
            )

            cat_pipeline=Pipeline(
                steps=[
                    ('imputer',SimpleImputer(strategy='most_frequent')),
                    ('one_hot_encoder',OneHotEncoder()),
                    ('Scalar',StandardScaler(with_mean=False))
                ]
            )

            logging.info('Numerical Cloumns',numerical_features)
            logging.info('Categorical Columns',categoriacal_features)

            preprocessor=ColumnTransformer(
                [
                    ('numerical_pipeline',num_pipeline,numerical_features),
                    ('cat_pipelines',cat_pipeline,categoriacal_features)
                ]
            )
            return preprocessor

        except Exception as e:
            raise CustomException(e,sys)

    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df=pd.read_csv(train_path)
            test_df=pd.read_csv(test_path)

            logging.info('Reading of the train and test data completed')
            logging.info('Obtaining preprcessor object')

            preprocessor_obj=self.get_data_transformation_config()

            target_column_name='math score'
            numerical_feature=['reading score', 'writing score']

            input_features_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_features_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]

            logging.info('Applying preprocessing object to train and test dataframe')

            input_feature_train_array=preprocessor_obj.fit_transform(input_features_train_df)
            input_feature_test_array=preprocessor_obj.transform(input_features_test_df)

            train_arr=np.c_[input_feature_train_array,np.array(target_feature_train_df)]
            test_arr=np.c_[input_feature_test_array,np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(
                file_path=self.data_transformation_config.preprocessor_obj_file_path,
                obj=preprocessor_obj
            )

            return(
                train_arr,
                test_arr,
                self.data_transformation_config.preprocessor_obj_file_path
            )


        except Exception as e:
            raise CustomException(e,sys)