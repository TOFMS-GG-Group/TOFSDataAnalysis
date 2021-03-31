import json
import os

import numpy as np


class cache:
    cache_file = None
    mass_to_charges = None

    def __init__(self, path):
        if not os.path.exists(path):
            # TODO: Create Empty JSON.
            print("Empty JSON")
        else:
            with open(path) as f:
                cache_file = json.load(f)

        self.mass_to_charges = cache_file['nominal_mass']

    @staticmethod
    def is_cached(mass_charge, file_path, cache_file):
        if os.path.exists(file_path):
            return str(mass_charge) in cache_file.mass_to_charges

        return False

    @staticmethod
    def cache(mass_charge, alpha, reshaped_l_c, ct_rate_array, cache_file):
        slopes = [0] * len(alpha)
        intercepts = [0] * len(alpha)

        for i in range(len(reshaped_l_c)):
            slopes[i], intercepts[i] = np.polyfit(np.sqrt(ct_rate_array), reshaped_l_c[i], 1)

        value = "{" + \
                "\"nominal_mass\":" + \
                    "{" + \
                        "\"" + str(mass_charge) + "\":" + \
                        "{" + \
                            "\"" + "alphas" + "\":" + str(alpha) + "," + \
                            "\"" + "slope" + "\":" + str(slopes) + "," + \
                            "\"" + "intercept" + "\":" + str(intercepts) +\
                        "}" + \
                    "}" + \
                "}"

        print("")
