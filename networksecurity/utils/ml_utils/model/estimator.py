'''
this file contains the Estimator class, which is a wrapper around a machine learning model.
to create NeteorkModel
'''
import os
import sys

from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkModel:
    """
    A class to encapsulate a machine learning model with methods for training, prediction, and evaluation.
    """
    def __init__(self,preprocessor, model):
        """
        Initializes the NetworkModel with a preprocessor and a model.
        """
        try:
          self.preprocessor = preprocessor
          self.model = model
        except Exception as e:
          raise NetworkSecurityException(e, sys)
    def predict(self,x):
        """
        Predicts the target variable for the given input data.
        
        :param x: Input data for prediction.
        :return: Predicted values.
        """
        try:
            x_transform = self.preprocessor.transform(x) # using transform and not fit_transform as we are not training the model here(preventing data leakage)
            y_hat = self.model.predict(x_transform)
            return y_hat
        except Exception as e:
            raise NetworkSecurityException(e, sys)
