from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.entity.config_entity import TrainingPipelineConfig, DataIngestionConfig
import sys

if __name__ == "__main__":
    try:
        
        from networksecurity.entity.artifact_entity import DataIngestionArtifact
        
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config=training_pipeline_config)
        
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        logging.info(f"Initiate Data Ingestion")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        print(data_ingestion_artifact)
        
    except Exception as e:
        raise NetworkSecurityException(e, sys)