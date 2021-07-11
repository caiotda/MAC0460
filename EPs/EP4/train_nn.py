import numpy as np
from tensorflow.keras.datasets import mnist
from sklearn.model_selection import train_test_split

from sklearn.model_selection import StratifiedKFold, GridSearchCV
import joblib

from sklearn.neural_network import MLPClassifier

np.random.seed(42)

(X_train_ori, y_train_ori), (X_test_ori, y_test_ori) = mnist.load_data()

print(f"X_train_ori: {X_train_ori.shape}")
print(f"X_test_ori: {X_test_ori.shape}")

X_train = np.array([image[::2, 1::2] for image in X_train_ori])
X_test  = np.array([image[::2, 1::2] for image in X_test_ori])

y_train = y_train_ori
y_test = y_test_ori

print("Before reshaping:")
print(f"X_train: {X_train.shape}")
print(f"X_test: {X_test.shape}")
print(f"y_train: {y_train.shape}")
print(f"y_test: {y_test.shape}")

X_train = (X_train/255.0).astype('float32').reshape((60000,14*14))
X_test = (X_test/255.0).astype('float32').reshape((10000,14*14))

print("After reshaping:")

print(X_train.dtype)
print(X_test.dtype)

print("\nShape of X_train: ", X_train.shape)
print("Shape of X_test: ", X_test.shape)

print("\nMinimum value in X_train:", np.amin(X_train))
print("Maximum value in X_train:", np.amax(X_train))

print("\nMinimum value in X_test:", np.amin(X_test))
print("Maximum value in X_test:", np.amax(X_test))

X_Dtrain, X_Dval, y_Dtrain, y_Dval = train_test_split(X_train,
                                                      y_train, 
                                                      test_size=0.30,
                                                      random_state=np.random.randint(0, 100),
                                                      stratify=y_train)

print(f"X_Dtrain: {X_Dtrain.shape}")
print(f"X_Dval: {X_Dval.shape}")
print(f"y_Dtrain: {y_Dtrain.shape}")
print(f"y_Dval: {y_Dval.shape}")

mlp = MLPClassifier()

hl_sizes = [
    (32,64,64),
    (128,128),
    (256,64),
    (128,)
]
activation = ["relu", "tanh"]
solver = ["adam", "sgd"]


grid = dict(hidden_layer_sizes=hl_sizes, activation=activation, solver=solver)
cv = StratifiedKFold(n_splits=5)
grid_search = GridSearchCV(
    estimator=mlp,
    param_grid=grid, 
    n_jobs=-1, 
    cv=cv, 
    verbose=3,
    scoring='accuracy',
    error_score=0)

grid_result = grid_search.fit(X_Dtrain, y_Dtrain)
print("Best: %f using %s" % (grid_result.best_score_, grid_result.best_params_))
score = grid_result.best_score_
hl, act, solver = grid_result.best_params_
filename = f"neural_net_score={score}_hl_sizes={hl}_activation={act}_solver={solver}.sav"
joblib.dump(grid_search, filename)

