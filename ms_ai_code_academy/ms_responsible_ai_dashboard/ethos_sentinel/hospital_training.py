import pandas as pd
import numpy as np

from sklearn.compose import make_column_selector as selector, ColumnTransformer
from sklearn.linear_model import LogisticRegression
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import OneHotEncoder, StandardScaler

from ethos_sentinel import settings

# configure logging
import logging
from logging.config import dictConfig
dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger(__name__)


class ModelTraining:

    def __init__(self, target_column: str, training_datat_path: str, test_data_path: str):
        """
        :param target_column: the target column of the model
        :param training_datat_path: the training data set for the model
        :param test_data_path: the testing data set for the model
        """
        # initialize the sets
        self.target_column = target_column
        self.training_data = pd.read_parquet(training_datat_path)
        self.test_data = pd.read_parquet(test_data_path)

        # split the training / test data into features
        self.y_train = self.training_data[self.target_column]
        self.x_train = self.training_data.drop([self.target_column], axis=1)
        self.y_test = self.test_data[self.target_column]
        self.x_test = self.test_data.drop([self.target_column], axis=1)

    def clean_data(self) -> ColumnTransformer:
        """
        Function to clean the data for processing
        :return: a ColumnTransformer object as preprocessor
        """
        # transform string data into numeric one-hot vectors
        categorical_selector = selector(dtype_exclude=np.number)
        categorical_columns = categorical_selector(self.x_train)
        categorical_encoder = OneHotEncoder(handle_unknown='ignore')

        # Standardize numeric data by removing the mean and scaling to unit variance
        numerical_selector = selector(dtype_include=np.number)
        numerical_columns = numerical_selector(self.x_train)
        numerical_encoder = StandardScaler()

        # Create a preprocessor that will preprocess both numeric and categorical data
        preprocessor = ColumnTransformer([
            ('categorical-encoder', categorical_encoder, categorical_columns),
            ('standard_scaler', numerical_encoder, numerical_columns)])

        return preprocessor

    def train_model(self):
        """
        Function to train the model
        """
        clf = make_pipeline(self.clean_data(), LogisticRegression())

        logger.info('Training model...')
        model = clf.fit(self.x_train, self.y_train)
        logger.info(f'Accuracy score: {clf.score(self.x_test, self.y_test)}')
        return model


if __name__ == '__main__':
    trainer = ModelTraining(target_column='readmit_status',
                            training_datat_path='data/testing_data.parquet',
                            test_data_path='data/testing_data.parquet')
    logger.debug(trainer.training_data.head())
    hospital_readmission_model = trainer.train_model()
