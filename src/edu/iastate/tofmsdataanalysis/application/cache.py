import json
import os

import numpy as np


class cache:
    cache_file = None
    mass_to_charges = None
    was_empty = False
    path = None

    def __init__(self, path):
        self.path = path

        if not os.path.exists(path):
            empty_obj = {"nominal_mass": {"test": {
                "alphas": [],
                "slope": [],
                "intercept": []
            }}}

            with open(path, 'w') as jsonFile:
                json.dump(empty_obj, jsonFile)
                self.was_empty = True

        with open(path, 'r') as jsonFile:
            cache_file = json.load(jsonFile)

        self.mass_to_charges = cache_file['nominal_mass']

    def is_cached(self, mass_charge):
        if os.path.exists(self.path):
            return str(mass_charge) in self.mass_to_charges

        return False

    def cache(self, mass_charge, alpha, reshaped_l_c, ct_rate_array, cache_file):
        slopes = [0] * len(alpha)
        intercepts = [0] * len(alpha)

        for i in range(len(reshaped_l_c)):
            slopes[i], intercepts[i] = np.polyfit(np.sqrt(ct_rate_array), reshaped_l_c[i], 1)

        with open(self.path) as json_file:
            data = json.load(json_file)

            json_obj = {
                str(mass_charge): {
                    "alphas": alpha,
                    "slopes": slopes,
                    "intercepts": intercepts
                }
            }

            data['nominal_mass'].update(json_obj)

        with open(self.path, 'w') as jsonFile:
            if self.was_empty:
                # TODO: Delete the empty JSON object.
                del data["nominal_mass"]["test"]

            json.dump(data, jsonFile)
