import os 
import sys 
from dataclasses import dataclass
 
import numpy as np
import pandas as pd
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import OneHotEncoder,StandardScaler

from src.exception import custom_exception
from src.logger import logging

from src.utils import save_object

@dataclass
class DataTransformerConfig:
    preprocessors_obj_file_path = os.path.join("artifacts","preprocessors.pkl")
    
class DataTransformation:
    def __init__(self):
        self.data_transformation_config =DataTransformerConfig()
        
    def get_data_transformation_object(self):
        try:
            numerical_columns = ["math score","reading score"]
            categorical_columns = ["gender","race/ethnicity",
                                  "parental level of education",
                                  "lunch","test preparation course"]
            
            num_pipeline = Pipeline(
                 steps=[
                ("imputer",SimpleImputer(strategy="median")),
                ("scaler",StandardScaler())
                    ]
            )
            
            cat_pipeline = Pipeline(
                steps=[
                ("imputer",SimpleImputer(strategy="most_frequent")),
                ("one_hot_encoder",OneHotEncoder()),
                ("scaler",StandardScaler(with_mean=False))
                ]
            )
            
            logging.info("Categorical Columns :{categorical_columns}")
            logging.info("Numerical Columns :{numerical_columns}")
            logging.info("Numerical columns standard scaling completed.")
            
            logging.info("Categorical Columns encoding completed.")
            
            preprocessors = ColumnTransformer(
                [
                ("num_pipeline",num_pipeline,numerical_columns),
                ("cat_pipelines",cat_pipeline,categorical_columns)

                ]


            )
            return preprocessors
        
        
        
        except Exception as e:
            raise custom_exception(e,sys)
        
        
    def initiate_data_transformation(self,train_path,test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)
                        
            logging.info("Read train and test data completed")
            
            logging.info("Obtaining Preprocessors Object")
            
            preprocessors_obj = self.get_data_transformation_object()
            
            target_column_name = "writing score"
            numerical_columns = ["math score","reading score"]

            input_feature_train_df=train_df.drop(columns=[target_column_name],axis=1)
            target_feature_train_df=train_df[target_column_name]

            input_feature_test_df=test_df.drop(columns=[target_column_name],axis=1)
            target_feature_test_df=test_df[target_column_name]
            
            logging.info("Applying preprocessing object on training dataframe and testing dataframe.")
        
            input_feature_train_arr = preprocessors_obj.fit_transform(input_feature_train_df)
            input_feature_test_arr = preprocessors_obj.transform(input_feature_test_df)
            
            train_arr = np.c_[input_feature_train_arr, np.array(target_feature_train_df)]
            
            test_arr = np.c_[input_feature_test_arr, np.array(target_feature_test_df)]

            logging.info(f"Saved preprocessing object.")

            save_object(

                file_path=self.data_transformation_config.preprocessors_obj_file_path ,
                obj=preprocessors_obj

            )
            return train_arr,test_arr,self.data_transformation_config.preprocessors_obj_file_path
                
        except Exception as e:
            raise custom_exception(e,sys)