import os 
import sys
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constant.training_pipeline import TARGET_COLUMN , DATA_TRANSFORMATION_IMPUTER_PARAMS

from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)

from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utils.utils import save_numpy_array_data, save_object

class DataTransformation:
  def __init__(self,data_validation_artifact:DataValidationArtifact,
               data_transformation_config:DataTransformationConfig):
    try:
      self.data_validation_artifact:DataValidationArtifact=data_validation_artifact
      self.data_transformation_config:DataTransformationConfig=data_transformation_config

    except Exception as e:
      raise NetworkSecurityException(e, sys)
  def read_data(file_path: str) -> pd.DataFrame:
    """
    Reads a CSV file and returns it as a pandas DataFrame.
    
    :param file_path: Path to the CSV file.
    :return: DataFrame containing the data from the CSV file.
    :raises NetworkSecurityException: If there is an error reading the file.
    """
    try:
      return pd.read_csv(file_path)
    except Exception as e:
      raise NetworkSecurityException(e, sys)
    
  def get_data_transformer_object(cls) -> Pipeline:
    '''
    It initiates the KNN Imputer and returns a pipeline object.
    parameter are speciofied in the constant file.
    :return: Pipeline object with KNN Imputer as first step

    Args : 
    cls: DataTranmsformation 

    Returns:
    Pipeline object with KNN Imputer as first step
    '''
    logging.info(f"Entered the get_data_transformer_object method of DataTransformation class")
    try:
      imputer:KNNImputer=KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS) ## ** is used to unpack the dictionary in form of key value pairs
      logging.info(f"Initialized KNNImputert with parameters: {DATA_TRANSFORMATION_IMPUTER_PARAMS}")
      processor:Pipeline=Pipeline(steps=[("Imputer", imputer)]) ## Pipeline is used to chain multiple transformers together
      return processor
    except Exception as e:
      raise NetworkSecurityException(e, sys)




  def initiate_data_transformation(self) -> DataTransformationArtifact:
    logging.info(f"Entered the initiate_data_transformation method of DataTransformation class")  
    try:
      logging.info("Starting Data Tranmsformation")
      train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
      test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
      
      ## training dataframe
      input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
      target_feature_train_df = train_df[TARGET_COLUMN]
      target_feature_train_df = target_feature_train_df.replace(-1,0)

      ## testing dataframe
      input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
      target_feature_test_df = test_df[TARGET_COLUMN]
      target_feature_test_df = target_feature_test_df.replace(-1,0)

      ## KNN Imputer
      preprocessor= self.get_data_transformer_object()

      preprocessor_object = preprocessor.fit(input_feature_train_df)
      transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
      transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)

      train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
      test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]

      ## save numpy array data
      save_numpy_array_data(file_path=self.data_transformation_config.transformed_train_file_path, array=train_arr,)
      save_numpy_array_data(file_path=self.data_transformation_config.transformed_test_file_path, array=test_arr,)
      save_object(file_path=self.data_transformation_config.transformed_object_file_path, obj=preprocessor_object,)

      ## preparing artifact
      data_transformation_artifact = DataTransformationArtifact(
        transformed_object_file_path=self.data_transformation_config.transformed_object_file_path,
        transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
        transformed_test_file_path=self.data_transformation_config.transformed_test_file_path
      )
      return data_transformation_artifact

    except Exception as e:
      raise NetworkSecurityException(e, sys)

