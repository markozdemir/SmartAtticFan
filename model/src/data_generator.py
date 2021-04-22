'''
Data generator for Attic Fan project
E -- energy consumption
Phi -- Rotation Speed of Fan
T -- temperature in the house. (around sensor)
delta_T -- temperature that makes people feel comfort
'''
#import Image
import numpy as np
import os
import matplotlib.pyplot as plt
import data_obtainer as do
from sklearn import metrics

save_results_to = '../../aws_server/model'

# np.save('path/to/file',file)

def ObjectId(t):
    return t

def get_data_from_text():
    #get mongo data
    data = do.get_data("fan", ["temp (C)", "hum", "Power (W)", "time", "RPM"], "hash")
    temp=[]
    hum=[]
    power=[]
    time=[]
    rpm=[]
    for ind, each_data in enumerate(data):

        if ind>40:
            continue

        if (each_data.get('Power (W)') == 0):
            continue

        if ind == 0:
            temp.append(each_data.get('temp (C)'))
            hum.append(each_data.get('hum'))
            power.append(each_data.get('Power (W)'))
            time.append(each_data.get('time'))
            rpm.append(each_data.get('RPM'))
        else:
            if (each_data.get('time')-data[ind-1].get('time') < 1500) :
                # print(each_data.get('time')-data[ind-1].get('time') )

                temp.append(each_data.get('temp (C)'))
                hum.append(each_data.get('hum'))
                power.append(each_data.get('Power (W)'))
                time.append(each_data.get('time'))
                rpm.append(each_data.get('RPM'))


    # import pdb; pdb.set_trace()
    time = np.asarray(time)
    X_train = (time-time[0])[:,np.newaxis]
    y_train = np.asarray(temp)[:,np.newaxis]

    from sklearn.neighbors import KNeighborsRegressor

    print('Temp Prediction')
    # import pdb; pdb.set_trace()
    modelKNN_temp = KNeighborsRegressor( n_neighbors= 3).fit(X_train, y_train)
    knn_y_pred_temp = modelKNN_temp.predict(X_train)
    print(f'Temp MAE KNN: {metrics.mean_absolute_error(y_train, knn_y_pred_temp)}')

    plt.figure()
    plt.plot(y_train,'r',label='Label')
    plt.plot(knn_y_pred_temp,'b',label='Pred')
    plt.savefig(save_results_to + 'knn_pred_temp.png')

    # from sklearn.linear_model import LogisticRegression
    # logisticRegr = LogisticRegression().fit(X_train, y_train)
    # lr_y_pred_temp = logisticRegr.predict(X_train)
    # print(f'Temp MAE LOGI_REGRESSION: {metrics.mean_absolute_error(y_train, lr_y_pred_temp)}')

    from sklearn.linear_model import LinearRegression
    linearReg = LinearRegression().fit(X_train, y_train)
    linearR_y_pred_temp = linearReg.predict(X_train)
    print(f'Temp MAE LINEAR_REGRESSION: {metrics.mean_absolute_error(y_train, linearR_y_pred_temp)}')


    plt.figure()
    plt.plot(y_train,'r',label='Label')
    plt.plot(linearR_y_pred_temp,'b',label='Pred')
    #plt.savefig('testplot1.png')
    plt.savefig(save_results_to + 'linearR_pred_temp.png')


    plt.show()

    #import pdb; pdb.set_trace()

    plt.plot(temp,'-*',label='temp')
    plt.plot(hum,'-*',label='hum')
    plt.plot(power,'-*',label='power')
    # plt.plot(rpm,'-*',label='rpm')
    plt.legend()
    plt.savefig(save_results_to + 'relationship.png')
    plt.show()


def main():

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

    #import pdb; pdb.set_trace()
    get_data_from_text()

if __name__ == '__main__':
    main()
