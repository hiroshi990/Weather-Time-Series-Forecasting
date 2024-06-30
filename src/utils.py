import pandas as pd 
from logger import logging
import sys
from exception import CustomException

def storing_data(obj,file_path):
    try:
        
        obj.to_csv(file_path,index=False)
        print("Data saved successfully")
    
        
    except Exception as e:
        raise CustomException(e,sys)