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
        """

        # Template
        self.s3_parameters_key = 's3_parameters.yaml'

        # Temporary storage area for the artefacts
        self.data_: str = os.path.join(os.getcwd(), 'data')
        self.artefacts_: str = os.path.join(self.data_, 'artefacts')

        # The self.__artefacts_ directory branch for the fundamental error matrix frequencies
        self.branch = os.path.join('prime', 'metrics', 'testing', 'fundamental.json')

        # Temporary storage area for the mathematical & business numerics
        self.warehouse = os.path.join(os.getcwd(), 'warehouse')
        self.numerics_ = os.path.join(self.warehouse, 'numerics')

        # Each architecture's prime artefacts are within the {architecture}/prime/ path
        self.prime_ = '/prime/'

        # Categories
        self.categories = { 'B-geo': 'GEO', 'B-gpe': 'GPE', 'B-org': 'ORG', 'B-per': 'PER', 'B-tim': 'TIM',
                            'I-geo': 'GEO', 'I-gpe': 'GPE', 'I-org': 'ORG', 'I-per': 'PER', 'I-tim': 'TIM',
                            'O': 'O'}
