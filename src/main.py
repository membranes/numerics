"""Module main.py"""
import datetime
import logging
import os
import sys

import boto3


def main():
    """
    Entry Point

    :return:
    """

    logger: logging.Logger = logging.getLogger(__name__)
    logger.info('Starting: %s', datetime.datetime.now().isoformat(timespec='microseconds'))

    # Set up
    setup: bool = src.setup.Setup(service=service, s3_parameters=s3_parameters).exc()
    if not setup:
        src.functions.cache.Cache().exc()
        sys.exit('No Executions')

    # Data
    src.data.interface.Interface(service=service, s3_parameters=s3_parameters).exc()

    # Model
    tags = src.tags.Tags(s3_parameters=s3_parameters).exc()
    model = src.model.Model().exc(tags=tags)
    logger.info(model.derivations)

    # Analytics
    src.analytics.interface.Interface(s3_parameters=s3_parameters).exc(derivations=model.derivations, tags=tags)
    src.abstracts.interface.Interface().exc(architecture=model.architecture, tags=tags)

    # Transfer
    src.transfer.interface.Interface(service=service, s3_parameters=s3_parameters).exc()

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

    # Classes
    import src.abstracts.interface
    import src.analytics.interface
    import src.data.interface
    import src.functions.service
    import src.functions.cache
    import src.model
    import src.s3.s3_parameters
    import src.setup
    import src.tags
    import src.transfer.interface

    # S3 S3Parameters, Service Instance
    connector = boto3.session.Session()
    s3_parameters = src.s3.s3_parameters.S3Parameters(connector=connector).exc()
    service = src.functions.service.Service(connector=connector, region_name=s3_parameters.region_name).exc()

    main()
