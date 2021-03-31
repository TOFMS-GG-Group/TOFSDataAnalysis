import sys

from src.edu.iastate.tofmsdataanalysis.analysis import critical_value_analysis
from src.edu.iastate.tofmsdataanalysis.application.config import config
from src.edu.iastate.tofmsdataanalysis.application.sis import sis
from src.edu.iastate.tofmsdataanalysis.application.cache import cache


def main(argv):
    print("Loading configuration file.")

    # Loads the configuration settings from a json file contain all the required parameters to run the application.
    config_file = config(argv[0])
    sis_file = sis(argv[1])
    cache_file = cache(config_file.cache_file_location)

    for profile in sis_file.profiles:
        nominal_mass = profile["NominalMass"]

        if (config_file.rate_min < profile["Rate"] < config_file.rate_max) and (nominal_mass in config_file.nominal_masses):
            critical_values: list = [None] * len(config_file.alpha_values)  # type: List[float]

            print(str(profile["NominalMass"]) + "\n")

            critical_values = critical_value_analysis.CriticalValueAnalysis.calculate_critical_value(
                config_file,
                profile["Intensity"],
                profile["Frequency"],
                sis_file.average_sis,
                nominal_mass,
                cache_file)


if __name__ == "__main__":
    main(sys.argv[1:])
