import json
import time

import numpy as np
import matplotlib.pyplot as plt


# Contains the code for preform the critical analysis.
class CriticalValueAnalysis:
    @staticmethod
    def monte_carlo(intensity, frequency, cmpd_array, sis_array_norm, ct_rate_array, alpha, nominal_mass, cache):
        if not cache.is_cached(nominal_mass):
            if len(intensity) == 0 or len(frequency) == 0:
                return

            with np.nditer(cmpd_array, flags=['multi_index'], op_flags=['readwrite']) as it:
                for x in it:
                    x[...] = np.sum(np.random.choice(sis_array_norm, x))

            l_c_array = np.array([])

            for i in range(len(alpha)):
                for j in range(0, len(ct_rate_array)):
                    OneLambdaArray = cmpd_array[j]
                    avg_OneLambdaArray = np.mean(OneLambdaArray)
                    s_c = np.quantile(OneLambdaArray, (1 - float(alpha[i])))
                    l_c = s_c - avg_OneLambdaArray
                    l_c_array = np.append(l_c_array, l_c)

            reshaped_l_c = np.reshape(l_c_array, (7, 10))

            cache.cache(nominal_mass, alpha, reshaped_l_c, ct_rate_array, cache)

            print("Plotting l_c")

            for l_c in reshaped_l_c:
                x = np.sqrt(ct_rate_array)
                y = l_c
                m, b = np.polyfit(x, y, 1)
                plt.plot(x, y, 'o', color='black')
                plt.plot(x, m * x + b)
                plt.show()
        else:
            with open(cache.path) as json_file:
                data = json.load(json_file)

            alphas = data["nominal_mass"][str(nominal_mass)]["alphas"]
            slopes = data["nominal_mass"][str(nominal_mass)]["slopes"]
            intercepts = data["nominal_mass"][str(nominal_mass)]["intercepts"]

            print(str(alphas) + "\n")
            print(str(slopes) + "\n")
            print(str(intercepts) + "\n")

            for i in range(len(slopes)):
                x = np.sqrt(ct_rate_array)
                plt.plot(x, slopes[i] * x + intercepts[i])
                plt.show()

        print("Monte Carlo Finished!\n")

    # Calculates a critical value from a alpha value, number of ion signals, and a file with the single ion signals.
    # This function returns an array with slope and intercept of the critical value.
    @staticmethod
    def calculate_critical_value(config, intensity, frequency, sis_value, nominal_mass, cache):
        sis_array = []

        for i in range(len(frequency)):
            if float(intensity[i] >= float(0.0)):
                for j in range(frequency[i]):
                    sis_array.append(float(intensity[i]))

        sis_array_norm = np.true_divide(sis_array, sis_value)

        # SqRtCrRateArray is the a linearly space (Lambda)^0.5 values used for creating the Poisson Dist.
        # CtRateArray is the array of lambda values for determining the cmpd Poisson distribution.
        sqrt_ct_rate_array = np.linspace(1, 5, num=10)
        ct_rate_array = sqrt_ct_rate_array ** 2

        cts_array = np.random.poisson(lam=ct_rate_array, size=(int(config.num_ions), len(ct_rate_array)))
        cmpd_array = cts_array.transpose()

        is_cached = cache.is_cached(nominal_mass)

        monte_carlo_begin = time.perf_counter()

        CriticalValueAnalysis.monte_carlo(
            intensity, frequency, cmpd_array, sis_array_norm, ct_rate_array, config.alpha_values, nominal_mass, cache)

        monte_carlo_end = time.perf_counter()

        monte_carlo_elapsed_time = monte_carlo_end - monte_carlo_begin

        print(f"Monte Carlo took {monte_carlo_elapsed_time:0.4f} seconds")
