import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from sklearn.model_selection import train_test_split

from sklearn.model_selection import RepeatedStratifiedKFold, GridSearchCV
import joblib

from sklearn.svm import SVC

(X_train_ori, y_train_ori), (X_test_ori, y_test_ori) = mnist.load_data()

X_train = np.array([image[::2, 1::2] for image in X_train_ori])
X_test  = np.array([image[::2, 1::2] for image in X_test_ori])

y_train = y_train_ori
y_test = y_test_ori

X_Dtrain, X_Dval, y_Dtrain, y_Dval = train_test_split(X_train,
                                                      y_train, 
                                                      test_size=0.30,
                                                      random_state=np.random.randint(0, 100),
                                                      stratify=y_train)

svm = SVC()

kernel = ['poly', 'rbf', 'sigmoid']
C = [50, 10, 1.0, 0.1, 0.01]
gamma = ['scale']


grid = dict(kernel=kernel,C=C,gamma=gamma)
cv = RepeatedStratifiedKFold(n_splits=5, random_state=1)
grid_search = GridSearchCV(
    estimator=svm, 
    param_grid=grid, 
    n_jobs=-1, 
    cv=cv, 
    scoring='accuracy',
    error_score=0)
grid_result = grid_search.fit(X_Dtrain, y_Dtrain)
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
score = grid_result.best_score_
ker, c, g = grid_result.best_params_
filename = f"SVM_score={score}_C={c}_kernel={ker}_gamma={g}.sav"
joblib.dump(grid_search, filename)