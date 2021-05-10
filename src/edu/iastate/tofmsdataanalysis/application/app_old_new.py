import sys

from src.edu.iastate.tofmsdataanalysis.analysis import critical_value_analysis
from src.edu.iastate.tofmsdataanalysis.analysis.utility import utility
from src.edu.iastate.tofmsdataanalysis.application.config import config
from src.edu.iastate.tofmsdataanalysis.application.sis import sis
from src.edu.iastate.tofmsdataanalysis.application.cache import cache


def main(argv):
    print("Loading configuration file.")

    # Loads the configuration settings from a json file contain all the required parameters to run the application.
    config_file = config(argv[0])
    sis_file = sis(argv[1])
    cache_file = cache(config_file.cache_file_location)

    nominal_masses = []
    rates = []
    nominal_rate_mapping = {}
    results = []
    final_results = []

    for profile in sis_file.profiles:
        nominal_masses.append(profile["NominalMass"])
        rates.append(profile["Rate"])
        nominal_rate_mapping[str(profile["NominalMass"])] = profile["Rate"]

    for element_mapping in config_file.elements_isotope_mapping:
        s = ''.join(x for x in config_file.elements_isotope_mapping[element_mapping][0] if x.isdigit())
        results.append(utility.find_closest(int(s), nominal_masses))

    for i in results:
        q = float('inf')

        if i[1] == q:
            if config_file.rate_min < nominal_rate_mapping[str(i[0])] < config_file.rate_max:
                final_results.append(i)
        else:
            if config_file.rate_min < nominal_rate_mapping[str(i[0])] < config_file.rate_max \
                    and config_file.rate_min < nominal_rate_mapping[str(i[1])] < config_file.rate_max:
                final_results.append(i)

    for i in final_results:
        critical_values: list = [None] * len(config_file.alpha_values)  # type: List[float]

        critical_values = critical_value_analysis.CriticalValueAnalysis.calculate_critical_value(
            config_file,
            profile["Intensity"],
            profile["Frequency"],
            sis_file.average_sis,
            i,
            cache_file)


if __name__ == "__main__":
    main(sys.argv[1:])
