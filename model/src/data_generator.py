'''
Data generator for Attic Fan project
E -- energy consumption
Phi -- Rotation Speed of Fan
T -- temperature in the house. (around sensor)
delta_T -- temperature that makes people feel comfort
'''

import numpy as np
import os
import matplotlib.pyplot as plt
import data_obtainer as do


def main():
    # Yin: Here is how you use my data conversion:
    data = do.get_data("fan", ["temp (C)", "hum"], "tuple")
    print("Data in array of tuples:")
    print(data)
    print()
    # OR:
    data = do.get_data("fan", ["temp (C)", "hum"], "array")
    print("Data in array of arrays:")
    print(data)
    print()
    # OR:
    print("Data in array of hashes:")
    data = do.get_data("fan", ["temp (C)", "hum"], "hash")
    print(data)
    print()

    ### generate relationship between T and Phi
    X=np.linspace(1,1000,200,endpoint=True)
    f_T_phi = np.power(X,-0.2)
    plt.figure('relationship between T and Phi')
    plt.title('relationship between T and Phi')
    plt.xlabel('Phi')
    plt.ylabel('T')

    plt.plot(f_T_phi)
    # plt.show()
    ### import pdb; pdb.set_trace()

    ### generate relationship between E and Phi*t
    t = np.linspace(1,900,900,endpoint=True)
    phi = [0,100,200,300,400]

    phi_list = []
    for each_phi in phi:
        # import pdb; pdb.set_trace()
        phi_list.append(t+each_phi)

    phi_arr = np.asarray(phi_list)


    plt.figure('relationship between E and Phi*t')
    plt.title('relationship between E and Phi*t')
    plt.xlabel('Different phi * t')
    plt.ylabel('Energy Consumption')

    for each_rela in phi_arr:
        plt.plot(t, each_rela)
    plt.show()

    import pdb; pdb.set_trace()


    ### define a model that can learn from data to explore targeted relationship


if __name__ == '__main__':
    main()
