import numpy as np
import knn_gear as knn
import sys

if __name__ == '__main__':
    knn_obj = knn.KNN_GEAR_PREDICTOR()
    knn_obj.load_model(path='./knn_gear_model.joblib')
    fan_speed = knn_obj.predict(np.array([float(sys.argv[1]), float(sys.argv[2])])[np.newaxis,:]) #[temp,hum]
    f = open("model_results.txt", "w")
    f.write(str(fan_speed))
    f.close()

