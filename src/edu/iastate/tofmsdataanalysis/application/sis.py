import json


class sis:
    date_time = None
    spectrum_count = None
    min_rate = None
    max_rate = None
    average_sis = None
    filtered_rate = None
    frequency = None
    intensity = None
    profiles = None

    def __init__(self, path):
        with open(path) as f:
            sis_file = json.load(f)

        self.date_time: str = sis_file["DateTime"]
        self.spectrum_count: int = sis_file["SpectrumCount"]
        self.min_rate: float = sis_file["MinRate"]
        self.max_rate: float = sis_file["MaxRate"]
        self.average_sis: float = sis_file["AverageSis"]
        self.filtered_rate: float = sis_file["FilteredRate"]

        self.frequency: list = sis_file["Frequency"]
        self.intensity = sis_file["Intensity"]
        self.profiles = sis_file["Profiles"]
