from src.exception import CustomException
from src.logger import logging

import sys
import os
from dataclasses import dataclass

import numpy as np
import pandas as pd

class DataTransformation:
    def initiate_data_transformation(self, train_path, test_path):
        try:
            train_df = pd.read_csv(train_path)
            test_df = pd.read_csv(test_path)

            logging.info('Train and Test Data read succesfully')

            input_feature_train_df = train_df.iloc[:,0]
            target_features_train_df = train_df.iloc[:,1:]

            input_feature_test_df = test_df.iloc[:,0]
            target_features_test_df = test_df.iloc[:,1:]

            logging.info('Converting to np arrays')

            train_arr = np.c_[
                np.array(input_feature_train_df), np.array(target_features_train_df)
                ]

            test_arr = np.c_[
                np.array(input_feature_test_df), np.array(target_features_test_df)
            ]

            return(
                train_arr,
                test_arr
            )


        except Exception as e:
            raise CustomException(e, sys)