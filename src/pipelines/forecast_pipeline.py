import sys
import os
import pandas as pd

from src.exception import CustomException
from src.logger import logging

from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.arima.model import ARIMAResults

class ForecastPipeline:
    def __init__(self) -> None:
        pass

    def forecast(self, modelno: int ,no_of_days: int = 1):
        try:
            model_name = 'model'+f'{modelno}'
            model_path = os.path.join('artifacts\models', model_name)
            loaded_model = ARIMAResults.load(model_path)
            yhat = loaded_model.forecast(steps=no_of_days)
            return yhat
        
        except Exception as e:
            raise CustomException(e, sys)

if __name__ == "__main__":
    fp = ForecastPipeline()
    print(fp.forecast(modelno= 0, no_of_days= 1))
    print("done")