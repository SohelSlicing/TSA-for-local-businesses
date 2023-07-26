import os
import sys
import csv

from src.logger import logging
from src.exception import CustomException
from src.database.cashregister import cashRegister

from dataclasses import dataclass
from sklearn.model_selection import train_test_split

import pandas as pd


@dataclass
class DataIngestionConfig:
    train_data_path: str = os.path.join('artifacts', 'train.csv')
    test_data_path: str = os.path.join('artifacts', 'test.csv')
    raw_data_path: str = os.path.join('artifacts', 'data.csv')

class DataIngestion:
    def __init__(self):
        self.ingestion_config = DataIngestionConfig()
        self.databaseObject = cashRegister()
        self.saleRecords = []

    def initiate_data_ingestion(self):
        try:
            logging.info('Starting data Ingestion ...')

            logging.info('Retrieving data from db ...')
            product_info_from_db = self.databaseObject.get_product_idname()
            productDict = {}
            for pns in product_info_from_db:
                productDict[pns[0]] = pns[1] 

            Sales_from_db = self.databaseObject.get_sales()
            
            feildnames = ['date'] + list(productDict.values())

            
            logging.info('Creating rows for csv ...')
            prevDate = "a"
            csvRow = {i : 0 for i in feildnames}
            for sales in Sales_from_db:
                if sales[1] != prevDate:
                    self.saleRecords.append(csvRow)
                    prevDate = sales[1]
                    csvRow = {i : 0 for i in feildnames}
                    csvRow['date'] = sales[1]
                
                csvRow[productDict[sales[2]]] += sales[3]
            
            self.saleRecords.append(csvRow)

            logging.info('Writing rows to csv ...')
            with open(self.ingestion_config.raw_data_path, 'w', newline='') as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=feildnames)
                
                writer.writeheader()    
                for recs in range(1, len(self.saleRecords)):
                    writer.writerow(self.saleRecords[recs])

            df = pd.read_csv(self.ingestion_config.raw_data_path)

            logging.info("train test split initiated")
            train_set, test_set = train_test_split(df, test_size = 0.2, random_state = 2002)

            train_set.to_csv(self.ingestion_config.train_data_path, index= False, header= True)
            test_set.to_csv(self.ingestion_config.test_data_path, index= False, header= True)

            logging.info("Data ingestion completed")

            return(
                self.ingestion_config.train_data_path,
                self.ingestion_config.test_data_path
            )

        except Exception as e:
            raise CustomException(e,sys)
        
if __name__ == "__main__":
    data_ingestion_obj = DataIngestion()
    train_df, test_df = data_ingestion_obj.initiate_data_ingestion()