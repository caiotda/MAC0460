import numpy as np
import matplotlib.pyplot as plt
from tensorflow.keras.datasets import mnist
from sklearn.model_selection import train_test_split

from sklearn.model_selection import RepeatedStratifiedKFold, GridSearchCV
import joblib

from sklearn.linear_model import LogisticRegression


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

lr = LogisticRegression(max_iter=1000)
solvers = ['newton-cg', 'lbfgs', 'liblinear']
penalty = ['l2']
c_values = [100, 10, 1.0, 0.1, 0.01]

grid = dict(solver=solvers,penalty=penalty,C=c_values)
cv = RepeatedStratifiedKFold(n_splits=4, n_repeats=1, random_state=np.random.randint(0, 100))

grid_search = GridSearchCV(estimator=lr, param_grid=grid, n_jobs=-1, cv=cv, scoring='accuracy',error_score=0, verbose=10)
grid_result = grid_search.fit(X_Dtrain, y_Dtrain)

score = grid_result.best_score_
c, penalty, solver = grid_result.best_params_
filename = f"logistic_regression_score={score}_C={C}_penalty={penalty}_solver={solver}.sav"
joblib.dump(grid_search, filename)