import numpy as np
from sklearn.neighbors import KNeighborsClassifier
from joblib import dump, load

class KNN_GEAR_PREDICTOR(object):
    """docstring for KNN_GEAR_PREDICTOR."""

    def __init__(self):
        super(KNN_GEAR_PREDICTOR, self).__init__()
        self.knn = KNeighborsClassifier(n_neighbors=3)


    def load_model(self,path='./knn_gear_model.joblib'):

        self.knn = load(path)

    def predict(self, input):
        # try:
        # print(f'Make sure input has size (1,2)!')
        return int(self.knn.predict(input))


if __name__ == '__main__':

     cur_temp = 50
     cur_hum = 45
     knn_gear = KNN_GEAR_PREDICTOR()
     knn_gear.load_model(path='./knn_gear_model.joblib')
     result = knn_gear.predict(np.array([cur_temp, cur_hum])[np.newaxis,:]) #[temp,hum]
     print(result)
