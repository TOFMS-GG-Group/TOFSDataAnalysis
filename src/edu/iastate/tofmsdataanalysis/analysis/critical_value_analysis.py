import numpy as np
import matplotlib.pyplot as plt


# Contains the code for preform the critical analysis.
class CriticalValueAnalysis:
    @staticmethod
    def monte_carlo(intensity, frequency, cmpd_array, sis_array, ct_rate_array, alpha, sqrt_ct_rate_array, average_sis):
        monte_carlo_data_results = []
        monte_carlo_sum_results = []

        count = 0

        if len(intensity) == 0 or len(frequency) == 0:
            return

        with np.nditer(cmpd_array, flags=['multi_index'], op_flags=['readwrite']) as it:
            for x in it:
                x[...] = sum(np.random.choice(sis_array, x))/average_sis
                count += 1

        l_c_array = np.array([])

        for i in range(0, len(ct_rate_array)):
            OneLambdaArray = cmpd_array[i]
            avg_OneLambdaArray = np.mean(OneLambdaArray)
            s_c = np.quantile(OneLambdaArray, (1 - float(alpha)))
            l_c = s_c - avg_OneLambdaArray
            l_c_array = np.append(l_c_array, l_c)

        x = sqrt_ct_rate_array
        y = l_c_array
        np.polyfit(x, y, 1)

        plt.plot(x, y)
        plt.show()

        return np.polyfit(x, y, 1)

    # Calculates a critical value from a alpha value, number of ion signals, and a file with the single ion signals.
    # This function returns an array with slope and intercept of the critical value.
    @staticmethod
    def calculate_critical_value_json(alpha, num_ions, intensity, frequency, average_sis):
        sis_array = []

        for i in range(len(frequency)):
            if float(intensity[i] >= float(0.0)):
                for j in range(frequency[i]):
                    sis_array.append(float(intensity[i]))

        # TODO: This is wrong
        sis_value = np.average(sis_array)
        sis_array_norm = np.true_divide(sis_array, sis_value)

        # SqRtCrRateArray is the a linearly space (Lambda)^0.5 values used for creating the Poisson Dist.
        # CtRateArray is the array of lambda values for determining the cmpd Poisson distribution.
        sqrt_ct_rate_array = np.linspace(0.5, 5, num=50)
        ct_rate_array = sqrt_ct_rate_array ** 2

        cts_array = np.random.poisson(lam=ct_rate_array, size=(int(num_ions), len(ct_rate_array)))
        cmpd_array = cts_array.transpose()

        # below: all count rates from the array poisson-distributed count rates are indexed
        # and the sum of the a random draw for each Poisson count is taken from the SIS_Array_Norm
        # and then these random draws are summed together and stored in the cmpd_array, which
        # is the array of Cmpd_Poisson Values for all lambda values tested.
        test = CriticalValueAnalysis.monte_carlo(
            intensity, frequency, cmpd_array, sis_array, ct_rate_array, alpha, sqrt_ct_rate_array, average_sis)
