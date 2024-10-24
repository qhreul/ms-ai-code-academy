from pandas import DataFrame

from ethos_sentinel import settings
from ethos_sentinel.hospital_training import ModelTraining

# ignore warnings if present
import warnings

# configure logging
import logging
from logging.config import dictConfig
dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger(__name__)

warnings.filterwarnings("ignore")


class Dashboard:

    def __init__(self, target_column: str, training_datat_path: str, test_data_path: str):
        """
        :param target_column: the target column of the model
        :param training_datat_path: the training data set for the model
        :param test_data_path: the testing data set for the model
        """
        self.target_column = target_column
        self.model_trainer = ModelTraining(self.target_column, training_datat_path, test_data_path)
        self.model = self.model_trainer.train_model()

    def get_categorical_numerical_data(self, dataset: DataFrame):
        """
        Get the categorical and numerical columns of the dataset
        :param dataset: the dataset to be used for comparison
        :return: the list of categorical and numerical features
        """
        dataset = dataset.drop([self.target_column], axis=1)
        categorical = []
        for col, value in dataset.iteritems():
            if value.dtype == 'object' or value.dtype == 'bool':
                categorical.append(col)
        numerical = dataset.columns.difference(categorical)
        return categorical, numerical


if __name__ == '__main__':
    dashboard = Dashboard(target_column='readmit_status',
                          training_datat_path='data/training_data.parquet',
                          test_data_path='data/testing_data.parquet')
    hospital_readmission_model = dashboard.model
    categorical, numerical = dashboard.get_categorical_numerical_data(dashboard.model_trainer.training_data)
    logger.debug(f'Categorical columns: {categorical}')
    logger.debug(f'Numerical columns: {numerical}')
