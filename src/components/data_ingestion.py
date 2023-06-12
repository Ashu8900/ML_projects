import os
import sys
from src.exception import custom_exception
import logging
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split as tts
from dataclasses import dataclass


@dataclass
class dataingestionconfig:
    train_data_path: str = os.path.join('artifacts','train.csv')
    test_data_path: str = os.path.join('artifacts','test.csv')
    raw_data_path: str = os.path.join('artifacts','raw.csv')
    

class dataingestion:
    def __init__(self):
        self.ingestion_config = dataingestionconfig()
        
    def initiate_data_ingestion(self):
        logging.info('Enter the data ingestion method or component')
        try:
            data = pd.read_csv("notebook\data\StudentsPerformance.csv")
            logging.info("Read the dataset as dataframe")
            
            os.makedirs(os.path.dirname(self.ingestion_config.train_data_path),exist_ok=True)
            
            data.to_csv(self.ingestion_config.raw_data_path,index=False,header=True)
            
            logging.info("Train test split initiated successfully")
            
            train_set,test_set = tts(data,test_size=0.2,random_state=50)
            
            train_set.to_csv(self.ingestion_config.train_data_path,index=False,header=True)
            
            test_set.to_csv(self.ingestion_config.test_data_path,index=False,header=True)
            
            logging.info("Ingestion of data is completed successfully")
            
            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )
        except Exception as e:
            return custom_exception(e,sys)
        
        
if __name__ == "__main__":  
    obj=dataingestion()
    obj.initiate_data_ingestion()