import logging
import os
import sys

import torch


def main():
    """
    Entry Point

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)

    # Set up
    setup: bool = src.setup.Setup(service=service, s3_parameters=s3_parameters).exc()
    if not setup:
        src.functions.cache.Cache().exc()
        sys.exit('No Executions')

    # Device Selection: Setting a graphics processing unit as the default device
    device = 'cuda' if torch.cuda.is_available() else 'cpu'
    logger.info('Device: %s', device)

    # Analytics
    src.analytics.interface.Interface(service=service, s3_parameters=s3_parameters).exc()

    # Delete Cache Points
    src.functions.cache.Cache().exc()


if __name__ == '__main__':

    # Paths
    root = os.getcwd()
    sys.path.append(root)
    sys.path.append(os.path.join(root, 'src'))

    # Logging
    logging.basicConfig(level=logging.INFO,
                        format='\n\n%(message)s\n%(asctime)s.%(msecs)03d',
                        datefmt='%Y-%m-%d %H:%M:%S')

    # Activate graphics processing units
    os.environ['CUDA_VISIBLE_DEVICES']='0'
    os.environ['TOKENIZERS_PARALLELISM']='true'
    os.environ['RAY_USAGE_STATS_ENABLED']='0'
    os.environ['HF_HOME']='/tmp'

    # Classes
    import src.analytics.interface
    import src.functions.service
    import src.functions.cache
    import src.s3.s3_parameters
    import src.setup

    # S3 S3Parameters, Service Instance
    s3_parameters = src.s3.s3_parameters.S3Parameters().exc()
    service = src.functions.service.Service(region_name=s3_parameters.region_name).exc()

    main()
