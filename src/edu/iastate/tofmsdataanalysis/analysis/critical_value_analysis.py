import time
import numpy as np
import matplotlib.pyplot as plt


# Contains the code for preform the critical analysis.
class CriticalValueAnalysis:
    @staticmethod
    def monte_carlo(intensity, frequency, cmpd_array, sis_array_norm, ct_rate_array, alpha):
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

        # x = sqrt_ct_rate_array
        # y = l_c_array
        #
        # reshaped_data = np.reshape(l_c_array, (-1, 10))
        #
        # for i in reshaped_data:
        #     plt.plot(x, reshaped_data[i])

    # Calculates a critical value from a alpha value, number of ion signals, and a file with the single ion signals.
    # This function returns an array with slope and intercept of the critical value.
    @staticmethod
    def calculate_critical_value(alpha, num_ions, intensity, frequency, sis_value):
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

        cts_array = np.random.poisson(lam=ct_rate_array, size=(int(num_ions), len(ct_rate_array)))
        cmpd_array = cts_array.transpose()

        monte_carlo_begin = time.perf_counter()

        CriticalValueAnalysis.monte_carlo(
            intensity, frequency, cmpd_array, sis_array_norm, ct_rate_array, alpha, sqrt_ct_rate_array)

        monte_carlo_end = time.perf_counter()

        print("Monte Carlo took " + str(monte_carlo_end - monte_carlo_begin) + " seconds.")
