import os
from dotenv import load_dotenv
from datetime import datetime

from azure.ai.ml import MLClient
from azure.ai.ml.entities import ComputeInstance, AmlCompute, Workspace
from azure.identity import DefaultAzureCredential

from ms_ai_code_academy import settings

# configure logging
import logging
from logging.config import dictConfig
dictConfig(settings.LOG_CONFIG)
logger = logging.getLogger(__name__)

load_dotenv()


class AzureMLClient:

    def __init__(self):
        self.ml_client = MLClient(
            credential=DefaultAzureCredential(),
            subscription_id=os.getenv('AZURE_SUBSCRIPTION_ID'),
            resource_group_name=os.getenv('AZURE_RESOURCE_GROUP')
        )

    def initiate_compute_instance(self, instance_name: str, instance_type: str = "STANDARD_DS3_v2"):
        """
        Create a Azure Compute instance
        :param instance_name: the name of the Azure Compute instance
        :param instance_type: the Type / size of the Azure Compute instance
        :return:
        """
        try:
            instance = ComputeInstance(
                name=instance_name,
                type=instance_type
            )
            instance_status = self.ml_client.begin_create_or_update(instance).result()
            logger.debug(f'Compute instance {instance_name} created with status = {instance_status}!')
        except Exception as e:
            logger.error(e)

    def initiate_compute_cluster(self, cluster_name: str, cluster_type: str = "amlcompute",
                                 cluster_size: str = "STANDARD_DS3_v2"):
        """
        Create a Azure Compute cluster
        :param cluster_name: the name of the Azure Compute cluster
        :param cluster_type: the type of the Azure Compute cluster
        :param cluster_size: the size of the Azure Compute cluster
        :return:
        """
        try:
            cluster = AmlCompute(
                name=cluster_name,
                type=cluster_type,
                size=cluster_size,
                location=os.getenv('AZURE_LOCATION'),
                min_instances=0,
                max_instances=2,
                idle_time_before_scale_down=120,
                tier='low_priority'
            )
            cluster_status = self.ml_client.begin_create_or_update(cluster).result()
            logger.debug(f'Compute cluster {cluster_name} created with status = {cluster_status}!')
        except Exception as e:
            logger.error(e)

    def initiate_ml_workspace(self, workspace_name: str, workspace_description: str = 'Workspace for Azure ML'):
        """
        Create a Azure ML workspace
        :param workspace_name: the name of the Azure ML workspace
        :param workspace_description: the description of the Azure ML workspace
        :return:
        """
        try:
            ws_basic = Workspace(
                name=workspace_name,
                location=os.getenv('AZURE_LOCATION'),
                display_name=workspace_name,
                description=workspace_description,
                hbi_workspace=False,
                tags=dict(purpose="demo")
            )
            # TODO - resolve issue related to "(Invalid) Missing dependent resources in workspace json"
            ws_basic = self.ml_client.workspaces.begin_create(ws_basic).result()
            logger.debug(f'Workspace {workspace_name} created with status = {ws_basic}!')
        except Exception as e:
            logger.error(e)


if __name__ == '__main__':
    # initialize the AzureMLClient object
    azure_ml_client = AzureMLClient()

    # create a new Azure ML workspace
    azure_ml_client.initiate_ml_workspace(workspace_name=f'mlw-dp100-labs-{datetime.now().strftime("%Y%m%d%H%M%S")}')

