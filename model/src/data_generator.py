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

save_results_to = '../../aws_server/'

# np.save('path/to/file',file)

def ObjectId(t):
    return t

def get_data_from_text():
    #examine data will change later
    '''data = [
            { "_id" : ObjectId("60650f1b4df28e2843e115c7"), "temp (C)" : 25.6, "hum" : 30.6, "Power (W)" : 0, "time" : 670550939, "RPM" : 0 },
            { "_id" : ObjectId("60650f2c4df28e2843e115c8"), "temp (C)" : 25.6, "hum" : 30.8, "Power (W)" : 0, "time" : 670550955, "RPM" : 0 },
            { "_id" : ObjectId("60650f3b4df28e2843e115c9"), "temp (C)" : 25.6, "hum" : 30.9, "Power (W)" : 0, "time" : 670550970, "RPM" : 0 },
            { "_id" : ObjectId("60650f4b4df28e2843e115ca"), "temp (C)" : 25.6, "hum" : 30.9, "Power (W)" : 0, "time" : 670550986, "RPM" : 0 },
            { "_id" : ObjectId("60650f6d4df28e2843e115cb"), "temp (C)" : 25.6, "hum" : 30.8, "Power (W)" : 0, "time" : 670551020, "RPM" : 0 },
            { "_id" : ObjectId("60650fb34df28e2843e115cc"), "temp (C)" : 25.6, "hum" : 30.7, "Power (W)" : 0, "time" : 670551090, "RPM" : 0 },
            { "_id" : ObjectId("6065231c777609e8f1858237"), "temp (C)" : 23.9, "hum" : 33.8, "Power (W)" : 0, "time" : 670556059, "RPM" : 0 },
            { "_id" : ObjectId("6065234f777609e8f1858238"), "temp (C)" : 24, "hum" : 35.3, "Power (W)" : 0, "time" : 670556110, "RPM" : 0 },
            { "_id" : ObjectId("60652427777609e8f1858239"), "temp (C)" : 24.3, "hum" : 39.8, "Power (W)" : 0, "time" : 670556326, "RPM" : 0 },
            { "_id" : ObjectId("606528cf777609e8f185823a"), "temp (C)" : 21.8, "hum" : 38.8, "Power (W)" : 0, "time" : 670557518, "RPM" : 0 },
            { "_id" : ObjectId("60652d7b777609e8f185823b"), "temp (C)" : 19.2, "hum" : 46.8, "Power (W)" : 50, "time" : 670558715, "RPM" : 1100 },
            { "_id" : ObjectId("606536d6aa4ccee346742b60"), "temp (C)" : 17.8, "hum" : 49.8, "Power (W)" : 50, "time" : 670561109, "RPM" : 1100 },
            { "_id" : ObjectId("60653b83aa4ccee346742b61"), "temp (C)" : 17.5, "hum" : 51.2, "Power (W)" : 50, "time" : 670562306, "RPM" : 1100 },
            { "_id" : ObjectId("606544ddda55366ed390f301"), "temp (C)" : 17.1, "hum" : 52.4, "Power (W)" : 50, "time" : 670564701, "RPM" : 1100 },
            { "_id" : ObjectId("6065498cdd5bde9fd1b757bc"), "temp (C)" : 17, "hum" : 52.3, "Power (W)" : 50, "time" : 670565900, "RPM" : 1100 },
            { "_id" : ObjectId("60654e3add5bde9fd1b757bd"), "temp (C)" : 16.9, "hum" : 52.7, "Power (W)" : 50, "time" : 670567097, "RPM" : 1100 },
            { "_id" : ObjectId("606552e91d4f780e36a1b90b"), "temp (C)" : 16.7, "hum" : 52.8, "Power (W)" : 50, "time" : 670568296, "RPM" : 1100 },
            { "_id" : ObjectId("606557971d4f780e36a1b90c"), "temp (C)" : 16.6, "hum" : 53.8, "Power (W)" : 50, "time" : 670569494, "RPM" : 1100 },
            { "_id" : ObjectId("60655c441d4f780e36a1b90d"), "temp (C)" : 16.2, "hum" : 52.5, "Power (W)" : 50, "time" : 670570691, "RPM" : 1100 },
            { "_id" : ObjectId("606560f11d4f780e36a1b90e"), "temp (C)" : 15.8, "hum" : 51.6, "Power (W)" : 50, "time" : 670571888, "RPM" : 1100 },
            { "_id" : ObjectId("606565a01d4f780e36a1b90f"), "temp (C)" : 15.4, "hum" : 51.2, "Power (W)" : 50, "time" : 670573087, "RPM" : 1100 },
            { "_id" : ObjectId("60656a4c1d4f780e36a1b910"), "temp (C)" : 15, "hum" : 51.2, "Power (W)" : 50, "time" : 670574283, "RPM" : 1100 },
            { "_id" : ObjectId("60656ef91d4f780e36a1b911"), "temp (C)" : 14.6, "hum" : 50.5, "Power (W)" : 50, "time" : 670575480, "RPM" : 1100 },
            { "_id" : ObjectId("606573a71d4f780e36a1b912"), "temp (C)" : 14.1, "hum" : 50.3, "Power (W)" : 50, "time" : 670576678, "RPM" : 1100 },
            { "_id" : ObjectId("606578551d4f780e36a1b913"), "temp (C)" : 13.7, "hum" : 50.5, "Power (W)" : 50, "time" : 670577876, "RPM" : 1100 },
            { "_id" : ObjectId("60657d021d4f780e36a1b914"), "temp (C)" : 13.2, "hum" : 50.3, "Power (W)" : 50, "time" : 670579073, "RPM" : 1100 },
            { "_id" : ObjectId("606581b01d4f780e36a1b915"), "temp (C)" : 12.8, "hum" : 50.1, "Power (W)" : 50, "time" : 670580271, "RPM" : 1100 },
            { "_id" : ObjectId("6065865d1d4f780e36a1b916"), "temp (C)" : 12.3, "hum" : 49.60001, "Power (W)" : 50, "time" : 670581468, "RPM" : 1100 },
            { "_id" : ObjectId("60658b0a1d4f780e36a1b917"), "temp (C)" : 11.9, "hum" : 49.2, "Power (W)" : 50, "time" : 670582665, "RPM" : 1100 },
            { "_id" : ObjectId("60658fb81d4f780e36a1b918"), "temp (C)" : 11.5, "hum" : 50.1, "Power (W)" : 50, "time" : 670583863, "RPM" : 1100 },
            { "_id" : ObjectId("606594661d4f780e36a1b919"), "temp (C)" : 11.1, "hum" : 49.7, "Power (W)" : 50, "time" : 670585061, "RPM" : 1100 },
            { "_id" : ObjectId("606599141d4f780e36a1b91a"), "temp (C)" : 10.8, "hum" : 49.5, "Power (W)" : 50, "time" : 670586259, "RPM" : 1100 },
            { "_id" : ObjectId("60659dc21d4f780e36a1b91b"), "temp (C)" : 10.5, "hum" : 50.3, "Power (W)" : 50, "time" : 670587457, "RPM" : 1100 },
            { "_id" : ObjectId("6065a2701d4f780e36a1b91c"), "temp (C)" : 10.2, "hum" : 50.2, "Power (W)" : 50, "time" : 670588655, "RPM" : 1100 },
            { "_id" : ObjectId("6065a71d1d4f780e36a1b91d"), "temp (C)" : 9.900001, "hum" : 50.1, "Power (W)" : 50, "time" : 670589852, "RPM" : 1100 },
            { "_id" : ObjectId("6065abcb1d4f780e36a1b91e"), "temp (C)" : 9.7, "hum" : 50.7, "Power (W)" : 50, "time" : 670591050, "RPM" : 1100 },
            { "_id" : ObjectId("6065b0781d4f780e36a1b91f"), "temp (C)" : 9.400001, "hum" : 51.4, "Power (W)" : 50, "time" : 670592247, "RPM" : 1100 },
            { "_id" : ObjectId("6065b5251d4f780e36a1b920"), "temp (C)" : 9.2, "hum" : 51.7, "Power (W)" : 50, "time" : 670593445, "RPM" : 1100 },
            { "_id" : ObjectId("6065b9d31d4f780e36a1b921"), "temp (C)" : 9, "hum" : 52, "Power (W)" : 50, "time" : 670594642, "RPM" : 1100 },
            { "_id" : ObjectId("6065be811d4f780e36a1b922"), "temp (C)" : 8.900001, "hum" : 52, "Power (W)" : 50, "time" : 670595840, "RPM" : 1100 },
            { "_id" : ObjectId("6065c32f1d4f780e36a1b923"), "temp (C)" : 8.900001, "hum" : 52.3, "Power (W)" : 50, "time" : 670597038, "RPM" : 1100 },
            { "_id" : ObjectId("6065c7dd1d4f780e36a1b924"), "temp (C)" : 8.8, "hum" : 52.5, "Power (W)" : 50, "time" : 670598236, "RPM" : 1100 },
            { "_id" : ObjectId("6065cc8c1d4f780e36a1b925"), "temp (C)" : 8.900001, "hum" : 53, "Power (W)" : 50, "time" : 670599435, "RPM" : 1100 },
            { "_id" : ObjectId("6065d1391d4f780e36a1b926"), "temp (C)" : 8.8, "hum" : 53.1, "Power (W)" : 50, "time" : 670600633, "RPM" : 1100 },
            { "_id" : ObjectId("6065d5e81d4f780e36a1b927"), "temp (C)" : 8.7, "hum" : 53.8, "Power (W)" : 50, "time" : 670601831, "RPM" : 1100 },
            { "_id" : ObjectId("6065da961d4f780e36a1b928"), "temp (C)" : 8.8, "hum" : 53.6, "Power (W)" : 50, "time" : 670603030, "RPM" : 1100 },
            { "_id" : ObjectId("6065df441d4f780e36a1b929"), "temp (C)" : 8.8, "hum" : 53.2, "Power (W)" : 50, "time" : 670604227, "RPM" : 1100 },
            { "_id" : ObjectId("6065e3f31d4f780e36a1b92a"), "temp (C)" : 8.8, "hum" : 53, "Power (W)" : 50, "time" : 670605426, "RPM" : 1100 },
            { "_id" : ObjectId("6065e8a11d4f780e36a1b92b"), "temp (C)" : 8.8, "hum" : 52.9, "Power (W)" : 50, "time" : 670606624, "RPM" : 1100 },
            { "_id" : ObjectId("6065ed4e1d4f780e36a1b92c"), "temp (C)" : 8.8, "hum" : 52.7, "Power (W)" : 50, "time" : 670607821, "RPM" : 1100 },
            { "_id" : ObjectId("6065f1fd1d4f780e36a1b92d"), "temp (C)" : 8.900001, "hum" : 52.5, "Power (W)" : 50, "time" : 670609020, "RPM" : 1100 },
            { "_id" : ObjectId("6065f6ab1d4f780e36a1b92e"), "temp (C)" : 9, "hum" : 52.4, "Power (W)" : 50, "time" : 670610218, "RPM" : 1100 },
            { "_id" : ObjectId("6065fb591d4f780e36a1b92f"), "temp (C)" : 9.2, "hum" : 52, "Power (W)" : 50, "time" : 670611416, "RPM" : 1100 },
            { "_id" : ObjectId("606600081d4f780e36a1b930"), "temp (C)" : 9.7, "hum" : 52.10001, "Power (W)" : 50, "time" : 670612615, "RPM" : 1100 },
            { "_id" : ObjectId("606604b71d4f780e36a1b931"), "temp (C)" : 10.5, "hum" : 52.4, "Power (W)" : 50, "time" : 670613814, "RPM" : 1100 },
            { "_id" : ObjectId("606609671d4f780e36a1b932"), "temp (C)" : 11.6, "hum" : 49.8, "Power (W)" : 50, "time" : 670615014, "RPM" : 1100 },
            { "_id" : ObjectId("60660e171d4f780e36a1b933"), "temp (C)" : 12.9, "hum" : 48.8, "Power (W)" : 50, "time" : 670616215, "RPM" : 1100 },
            { "_id" : ObjectId("606612c81d4f780e36a1b934"), "temp (C)" : 14.7, "hum" : 48.1, "Power (W)" : 50, "time" : 670617416, "RPM" : 1100 },
            { "_id" : ObjectId("606617791d4f780e36a1b935"), "temp (C)" : 16.7, "hum" : 48.6, "Power (W)" : 50, "time" : 670618617, "RPM" : 1100 },
            { "_id" : ObjectId("60661c2a1d4f780e36a1b936"), "temp (C)" : 18.6, "hum" : 51.3, "Power (W)" : 50, "time" : 670619817, "RPM" : 1100 },
            { "_id" : ObjectId("606620da1d4f780e36a1b937"), "temp (C)" : 20.3, "hum" : 48.4, "Power (W)" : 50, "time" : 670621017, "RPM" : 1100 },
            { "_id" : ObjectId("606625891d4f780e36a1b938"), "temp (C)" : 21.7, "hum" : 50.8, "Power (W)" : 50, "time" : 670622216, "RPM" : 1100 },
            { "_id" : ObjectId("60662a3a1d4f780e36a1b939"), "temp (C)" : 22.9, "hum" : 47.7, "Power (W)" : 50, "time" : 670623418, "RPM" : 1100 },
            { "_id" : ObjectId("60662ee91d4f780e36a1b93a"), "temp (C)" : 23.8, "hum" : 45.1, "Power (W)" : 50, "time" : 670624617, "RPM" : 1100 },
            { "_id" : ObjectId("606633971d4f780e36a1b93b"), "temp (C)" : 23.9, "hum" : 42.4, "Power (W)" : 0, "time" : 670625814, "RPM" : 0 },
            { "_id" : ObjectId("606638451d4f780e36a1b93c"), "temp (C)" : 23.5, "hum" : 37.9, "Power (W)" : 0, "time" : 670627012, "RPM" : 0 },
            { "_id" : ObjectId("60663cf11d4f780e36a1b93d"), "temp (C)" : 23.1, "hum" : 36.1, "Power (W)" : 0, "time" : 670628208, "RPM" : 0 },
            { "_id" : ObjectId("606641a11d4f780e36a1b93e"), "temp (C)" : 22.3, "hum" : 35.6, "Power (W)" : 0, "time" : 670629408, "RPM" : 0 },
            { "_id" : ObjectId("6066464e1d4f780e36a1b93f"), "temp (C)" : 21.7, "hum" : 35.1, "Power (W)" : 0, "time" : 670630605, "RPM" : 0 },
            { "_id" : ObjectId("60664afb1d4f780e36a1b940"), "temp (C)" : 21.3, "hum" : 34.6, "Power (W)" : 0, "time" : 670631802, "RPM" : 0 },
            { "_id" : ObjectId("60664fa71d4f780e36a1b941"), "temp (C)" : 20.3, "hum" : 33.9, "Power (W)" : 0, "time" : 670632998, "RPM" : 0 },
            { "_id" : ObjectId("606654531d4f780e36a1b942"), "temp (C)" : 18.8, "hum" : 33.7, "Power (W)" : 0, "time" : 670634194, "RPM" : 0 },
            { "_id" : ObjectId("606658ff1d4f780e36a1b943"), "temp (C)" : 17.6, "hum" : 32.6, "Power (W)" : 0, "time" : 670635390, "RPM" : 0 },
            { "_id" : ObjectId("60665dab1d4f780e36a1b944"), "temp (C)" : 16.3, "hum" : 33.4, "Power (W)" : 0, "time" : 670636587, "RPM" : 0 },
            { "_id" : ObjectId("606662581d4f780e36a1b945"), "temp (C)" : 15.1, "hum" : 33.7, "Power (W)" : 0, "time" : 670637783, "RPM" : 0 },
            { "_id" : ObjectId("606667041d4f780e36a1b946"), "temp (C)" : 13.9, "hum" : 32.3, "Power (W)" : 0, "time" : 670638979, "RPM" : 0 },
            { "_id" : ObjectId("60666bb11d4f780e36a1b947"), "temp (C)" : 12.9, "hum" : 33.7, "Power (W)" : 0, "time" : 670640176, "RPM" : 0 },
            { "_id" : ObjectId("6066705d1d4f780e36a1b948"), "temp (C)" : 12, "hum" : 33.7, "Power (W)" : 0, "time" : 670641373, "RPM" : 0 },
            { "_id" : ObjectId("6066750a1d4f780e36a1b949"), "temp (C)" : 11.2, "hum" : 33.5, "Power (W)" : 0, "time" : 670642569, "RPM" : 0 },
            { "_id" : ObjectId("606679b71d4f780e36a1b94a"), "temp (C)" : 10.3, "hum" : 33.6, "Power (W)" : 0, "time" : 670643766, "RPM" : 0 },
            { "_id" : ObjectId("60667e661d4f780e36a1b94b"), "temp (C)" : 9.6, "hum" : 35.4, "Power (W)" : 0, "time" : 670644965, "RPM" : 0 },
            { "_id" : ObjectId("606683121d4f780e36a1b94c"), "temp (C)" : 8.900001, "hum" : 36.1, "Power (W)" : 0, "time" : 670646161, "RPM" : 0 },
            { "_id" : ObjectId("606687bf1d4f780e36a1b94d"), "temp (C)" : 8.2, "hum" : 36.1, "Power (W)" : 0, "time" : 670647358, "RPM" : 0 },
            { "_id" : ObjectId("60668c6d1d4f780e36a1b94e"), "temp (C)" : 7.6, "hum" : 35.4, "Power (W)" : 0, "time" : 670648556, "RPM" : 0 },
            { "_id" : ObjectId("6066911b1d4f780e36a1b94f"), "temp (C)" : 7, "hum" : 36.8, "Power (W)" : 0, "time" : 670649755, "RPM" : 0 },
            { "_id" : ObjectId("606695c91d4f780e36a1b950"), "temp (C)" : 6.5, "hum" : 37.3, "Power (W)" : 0, "time" : 670650952, "RPM" : 0 },
            { "_id" : ObjectId("60669a761d4f780e36a1b951"), "temp (C)" : 6, "hum" : 37.4, "Power (W)" : 0, "time" : 670652149, "RPM" : 0 },
            { "_id" : ObjectId("60669f231d4f780e36a1b952"), "temp (C)" : 5.7, "hum" : 38.4, "Power (W)" : 0, "time" : 670653346, "RPM" : 0 },
            { "_id" : ObjectId("6066a3d11d4f780e36a1b953"), "temp (C)" : 5.3, "hum" : 38.9, "Power (W)" : 0, "time" : 670654545, "RPM" : 0 },
            { "_id" : ObjectId("6066a87e1d4f780e36a1b954"), "temp (C)" : 4.9, "hum" : 39.7, "Power (W)" : 0, "time" : 670655741, "RPM" : 0 },
            { "_id" : ObjectId("6066ad2b1d4f780e36a1b955"), "temp (C)" : 4.6, "hum" : 40.4, "Power (W)" : 0, "time" : 670656939, "RPM" : 0 },
            { "_id" : ObjectId("6066b1d91d4f780e36a1b956"), "temp (C)" : 4.2, "hum" : 40.6, "Power (W)" : 0, "time" : 670658137, "RPM" : 0 },
            { "_id" : ObjectId("6066b6871d4f780e36a1b957"), "temp (C)" : 3.8, "hum" : 40.6, "Power (W)" : 0, "time" : 670659334, "RPM" : 0 },
            { "_id" : ObjectId("6066bb351d4f780e36a1b958"), "temp (C)" : 3.5, "hum" : 41.1, "Power (W)" : 0, "time" : 670660532, "RPM" : 0 },
            #{ "_id" : ObjectId("60674d801d4f780e36a1b959"), "temp (C)" : 0, "hum" : 0, "Power (W)" : 0, "time" : 670697983, "RPM" : 0 },
            { "_id" : ObjectId("60675ac8a9aef9ce38764881"), "temp (C)" : 3.2, "hum" : 41.1, "Power (W)" : 0, "time" : 670701383, "RPM" : 0 },
            { "_id" : ObjectId("6067c7b27706c5c90f5f810b"), "temp (C)" : 26.1, "hum" : 31.4, "Power (W)" : 0, "time" : 670729266, "RPM" : 0 },
            ]'''
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




    #import pdb; pdb.set_trace()


def main():
    # Yin: Here is how you use my data conversion:
    #data = do.get_data("fan", ["temp (C)", "hum", "time"], "tuple")
    #print("Data in array of tuples:")
    #print(data)
    #print()
    # OR:
    #data = do.get_data("fan", ["temp (C)", "hum", "time"], "array")
    #print("Data in array of arrays:")
    #print(data)
    #print()
    # OR:
    #print("Data in array of hashes:")
    #data = do.get_data("fan", ["temp (C)", "hum", "time"], "hash")
    #print(data)
    #print()

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

    ### define a model that can learn from data to explore targeted relationship


if __name__ == '__main__':
    main()
