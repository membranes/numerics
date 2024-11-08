"""config.py"""
import os


class Config:
    """
    Config
    """

    def __init__(self) -> None:
        """
        Constructor<br>
        ------------<br>

        Variables denoting a path - including or excluding a filename - have an underscore suffix; this suffix is
        excluded for names such as warehouse, storage, depository, etc.<br><br>

        The variable <b>self.s3_parameters_template_</b> points to a template of
        Amazon S3 (Simple Storage Service) parameters & arguments.
        """

        # Template
        self.s3_parameters_template_ = 'https://raw.githubusercontent.com/membranes/configurations/refs/heads/master/data/s3_parameters.yaml'

        # Temporary storage area for the artefacts
        self.data_: str = os.path.join(os.getcwd(), 'data')
        self.artefacts_: str = os.path.join(self.data_, 'artefacts')

        # Temporary storage area for the mathematical & business numerics
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
        self.numerics_ = os.path.join(self.warehouse, 'numerics')

        # Each architecture's prime model artefacts are within the {architecture}/prime/model path
        self.architectures = ['bert', 'distil', 'roberta', 'electra']
        self.prime_model_anchor = '/prime/model'
