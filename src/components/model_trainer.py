import sys
import os
from dataclasses import dataclass

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima.model import ARIMAResults

from src.exception import CustomException
from src.logger import logging
from src.utils import save_object

@dataclass
class ModelTrainerConfig:
    trained_model_file_path = "artifacts/models"

class ModelTrainer:
    def __init__(self) -> None:
        self.model_trainer_config = ModelTrainerConfig()

    def initiate_model_trainer(self, train_array, test_array):
        try:
            logging.info("Spliting the target for different products")

            number_of_products = train_array.shape[1]

            X_train, X_test = (
                train_array[:,0],
                test_array[:,0]
            )

            y_train, y_test = [], []
            for products in range(1,number_of_products):
                y_train.append(train_array[:,products].astype(int))
                y_test.append(test_array[:,products].astype(int))

            models = []
            os.makedirs(self.model_trainer_config.trained_model_file_path, exist_ok=True)
            for i in range(len(y_train)):
                model = ARIMA(endog= y_train[i], order=(1,1,1))
                model_fit = model.fit()

                model_name = "model"+f"{i}"
                path = os.path.join(self.model_trainer_config.trained_model_file_path, model_name)
                model_fit.save(path)
            
            print("Success...")



        except Exception as e:
            raise CustomException(e, sys)