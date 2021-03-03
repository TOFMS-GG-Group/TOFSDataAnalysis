import sys

from src.edu.iastate.tofmsdataanalysis.analysis import critical_value_analysis
from src.edu.iastate.tofmsdataanalysis.application.config import config
from src.edu.iastate.tofmsdataanalysis.application.sis import sis


def main(argv):
    print("Loading configuration file.")

    # Loads the configuration settings from a json file contain all the required parameters to run the application.
    config_file = config(argv[0])
    sis_file = sis(argv[1])

    for profile in sis_file.profiles:
        nominal_mass = profile["NominalMass"]

        if (config_file.rate_min < profile["Rate"] < config_file.rate_max) and (nominal_mass in config_file.nominal_masses):
            critical_values: list = [None] * len(config_file.alpha_values)  # type: List[float]

            print(str(profile["NominalMass"]) + "\n")

            # Loops through all the alpha values and calculates the critical values.
            # TODO: Fix average_sis
            for i in range(len(config_file.alpha_values)):
                critical_values[i] = critical_value_analysis.CriticalValueAnalysis.calculate_critical_value_json(
                    config_file.alpha_values[i],
                    config_file.num_ions,
                    profile["Intensity"],
                    profile["Frequency"],
                    profile["AverageSis"])


if __name__ == "__main__":
    main(sys.argv[1:])
