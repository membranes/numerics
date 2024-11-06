"""config.py"""
import os


class Config:
    """
    Config
    """

    def __init__(self) -> None:
        """
        Constructor<br>
        -----------<br>

        Variables denoting a path - including or excluding a filename - have an underscore suffix; this suffix is
        excluded for names such as warehouse, storage, depository, etc.<br><br>

        The variable <b>self.s3_parameters_template_</b> points to a template of
        Amazon S3 (Simple Storage Service) parameters & arguments.
        """

        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
        self.artefacts_ = os.path.join(self.warehouse, 'artefacts')
        self.s3_parameters_template_ = 'https://raw.githubusercontent.com/membranes/configurations/refs/heads/master/data/s3_parameters.yaml'
        self.architectures = ['bert', 'distil', 'roberta', 'electra']
