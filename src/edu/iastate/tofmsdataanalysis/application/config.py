import json


# Loads the configuration JSON file and exposed the parameters.
class config:
    alpha_values = None
    num_ions = None
    elements_isotope_mapping = None
    elements_isotope_mapping = None
    sis_file_location = None
    signal_file_location = None
    cache_file_location = None
    output_file_location = None
    rate_min = None
    rate_max = None
    nominal_masses = None

    # Config constructor, loads each parameter value from the config file.
    def __init__(self, path):
        with open(path) as f:
            config_file = json.load(f)

        self.alpha_values: list = config_file['alpha_values']
        self.num_ions: int = config_file['num_ions']

        self.elements_isotope_mapping: dict = config_file['isotope_element_mapping']

        self.sis_file_location: str = config_file['sis_file_location']
        self.signal_file_location: str = config_file['signal_file_location']
        self.cache_file_location: str = config_file['cache_file_location']
        self.output_file_location: str = config_file['output_file_location']

        self.rate_min: float = config_file['rate']['min']
        self.rate_max: float = config_file['rate']['max']

        self.nominal_masses: list = config_file['nominal_masses']
