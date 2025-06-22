from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig , DataValidationConfig
from networksecurity.entity.artifact_entity import DataIngestionArtifact
from networksecurity.components.data_validation import DataValidation
import sys

if __name__ == "__main__":
    try:
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconifg = DataIngestionConfig(training_pipeline_config=trainingpipelineconfig)
        data_ingestion = DataIngestion(data_ingestion_config=dataingestionconifg)
        logging.info("Initiating data ingestion process")
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        logging.info(f"Data ingestion completed successfully. Artifact.")
        print(dataingestionartifact)
        data_validation_config = DataValidationConfig(trainingpipelineconfig)
        data_validation = DataValidation(data_ingestion_artifact=dataingestionartifact, data_validation_config=data_validation_config)
        logging.info("Data validation process initiated")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info(f"Data validation completed successfully. Artifact")
        print(data_validation_artifact)
    except Exception as e:
        raise NetworkSecurityException(e, sys)