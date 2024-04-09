import numpy as np

def log_2_function(df, y):
    # add th plus 1
    return np.log2(df[y] + 1)


def log_2_function_lists(array):
    # add th plus 1
    values_plus_one = np.array(array) + 1
    return np.log2(values_plus_one)

def log_2(x):
    return np.log2(x)