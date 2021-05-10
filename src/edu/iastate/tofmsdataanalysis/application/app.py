import json
from json import JSONDecodeError

from PyQt5 import QtWidgets
from PyQt5.QtWidgets import QPushButton
import sys

from edu.iastate.tofmsdataanalysis.analysis import critical_value_analysis
from edu.iastate.tofmsdataanalysis.analysis.utility import utility
from edu.iastate.tofmsdataanalysis.application.cache import cache
from edu.iastate.tofmsdataanalysis.application.config import config
from edu.iastate.tofmsdataanalysis.application.sis import sis
from edu.iastate.tofmsdataanalysis.application.ui.TOFMSDataAnalysisUI import Ui_TOFMSDataAnalysis


class MainWindowUIClass(Ui_TOFMSDataAnalysis):
    def __init__(self):
        super().__init__()

    def setupUi(self, MW):
        super().setupUi(MW)

        self.computeValues.clicked.connect(self.computeValuesOnClick)
        self.loadJSON.clicked.connect(self.loadJSONOnClick)

    def computeValuesOnClick(self):
        print("Alpha Values : " + self.alphaValues.toPlainText() + "\n")
        print("Number of Ions : " + self.numberOfIons.toPlainText() + "\n")
        print("Isotope Mappings : " + self.isotopeMappings.toPlainText() + "\n")
        print("Rate Minimum : " + self.rateMinimum.toPlainText() + "\n")
        print("Rate Maximum : " + self.rateMaximum.toPlainText() + "\n")
        print("Nominal Mass : " + self.nominalMasses.toPlainText() + "\n")

        alpha_value_array = self.alphaValues.toPlainText().replace(' ', '').split(',')
        nominal_masses_array = self.nominalMasses.toPlainText().replace(' ', '').split(',')

        for i in range(len(alpha_value_array)):
            alpha_value_array[i] = float(alpha_value_array[i])

        for i in range(len(nominal_masses_array)):
            nominal_masses_array[i] = int(nominal_masses_array[i])

        number_ions = self.numberOfIons.toPlainText()
        isotope_element_mapping = self.isotopeMappings.toPlainText().split('\n')
        rate_min = self.rateMinimum
        rate_max = self.rateMaximum
        sis_file_location = self.sisFilePath
        signal_file_location = self.signalFilePath
        cache_file_location = self.cacheFileLocation
        output_file_location = self.outputFilePath

        config_json = {"alpha_values": alpha_value_array, "num_ions": int(number_ions), "isotope_element_mapping": {
            "test": ["test", "test"]
        }, "rate": {
            "min": float(rate_min.toPlainText()),
            "max": float(rate_max.toPlainText())
        },
                       "nominal_masses": nominal_masses_array,
                       "sis_file_location": sis_file_location.toPlainText(),
                       "signal_file_location": signal_file_location.toPlainText(),
                       "cache_file_location": cache_file_location.toPlainText(),
                       "output_file_location": output_file_location.toPlainText()}

        for line in isotope_element_mapping:
            element = line.split(':')[0]
            isotopes = line.split(':')[1].split(",")

            # TODO: This is not working.
            for isotope in isotopes:
                isotope.replace(' ', '')

            obj = {
                str(element): isotopes
            }

            config_json['isotope_element_mapping'].update(obj)

        del config_json['isotope_element_mapping']['test']

        out_file = ""

        try:
            out_file = open(str(output_file_location.toPlainText() + "/input.json"), "w")
        except IOError:
            print("Unable to create the file " + str(output_file_location.toPlainText() + "/input.json"))

        try:
            json.dump(config_json, out_file, indent=4)
            out_file.close()
        except JSONDecodeError:
            print("An Error Occurred Trying to Create JSON File!")

        print("Loading configuration file.")

        try:
            # Loads the configuration settings from a json file contain all the required parameters to run the
            # application.
            config_file = config((output_file_location.toPlainText() + "/input.json"))
            sis_file = sis(config_file.sis_file_location)
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
        except Exception as e:
            print("Error " + str(e) + " Calculating Monte Carlo!")

    def loadJSONOnClick(self):
        try:
            # Loads the configuration settings from a json file contain all the required parameters to run the
            # application.
            config_file = config((self.outputFilePath.toPlainText() + "/input.json"))
            sis_file = sis(config_file.sis_file_location)
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

            print(results)

            for i in final_results:
                critical_values: list = [None] * len(config_file.alpha_values)  # type: List[float]

                critical_values = critical_value_analysis.CriticalValueAnalysis.calculate_critical_value(
                    config_file,
                    profile["Intensity"],
                    profile["Frequency"],
                    sis_file.average_sis,
                    i,
                    cache_file)
        except Exception as e:
            print("Error " + str(e) + " Calculating Monte Carlo!")

def main():
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()

    ui = MainWindowUIClass()
    ui.setupUi(MainWindow)

    MainWindow.show()
    sys.exit(app.exec_())


main()
