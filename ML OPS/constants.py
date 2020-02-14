# Import Statements
from sklearn.linear_model import LinearRegression, Ridge, Lasso, ElasticNet, SGDRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor

from keras.models import Sequential
from keras.layers import Dense
from keras.layers import Dropout

# Parameter grids for parameter tuning
ols_params = {
    'regressor__fit_intercept': [True, False]
}

ridge_and_lasso_params = {
    'regressor__alpha': [0.01, 0.1, 1, 10]
}

elastic_net_params = {
    'regressor__alpha': [0.01, 0.1, 1, 10],
    'regressor__l1_ratio': [0.25, 0.50, 0.75]
}

sgd_param_grid = {
    'regressor__penalty': ['l1', 'l2', 'elasticnet'],
    'regressor__alpha': [0.0001, 0.001, 0.01, 0.1, 1],
    'regressor__learning_rate': ['constant', 'invscaling']
}

random_forest_param_grid = {
    'regressor__max_features': ['auto', 'sqrt', 'log2'],
    'regressor__max_depth': [None, 3, 5, 7]
}

gradient_boosting_param_grid = {
    'regressor__learning_rate': [0.1, 1, 10],
    'regressor__n_estimators': [50, 75, 100],
    'regressor__max_depth': [None, 3, 5, 7]
}

# Lists for iteration
model_names = ['ols', 'ridge', 'lasso', 'elastic_net', 'sgd', 'random_forest', 'gradient_boosting']

models = [LinearRegression(), Ridge(), Lasso(), ElasticNet(), SGDRegressor(), RandomForestRegressor(n_estimators=50), GradientBoostingRegressor()]

param_grids = [ols_params, ridge_and_lasso_params, ridge_and_lasso_params, elastic_net_params, sgd_param_grid, random_forest_param_grid, gradient_boosting_param_grid]

# Keras models
def baseline_neural_net():
    model = Sequential()
    model.add(Dense(50, input_dim=148, kernel_initializer='normal', activation='relu'))
    model.add(Dense(25, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def expanded_neural_net():
    model = Sequential()
    model.add(Dense(50, input_dim=148, kernel_initializer='normal', activation='relu'))
    model.add(Dense(25, kernel_initializer='normal', activation='relu'))
    model.add(Dense(10, kernel_initializer='normal', activation='relu'))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

def expanded_neural_net_dropout():
    model = Sequential()
    model.add(Dense(50, input_dim=148, kernel_initializer='normal', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(25, kernel_initializer='normal', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(10, kernel_initializer='normal', activation='relu'))
    model.add(Dropout(0.2))
    model.add(Dense(1, kernel_initializer='normal'))
    model.compile(loss='mean_squared_error', optimizer='adam')
    return model

# More lists for iteration
nn_names = ['baseline_nn', 'expanded_nn', 'expanded_nn_with_dropout']
nn_models = [baseline_neural_net, expanded_neural_net, expanded_neural_net_dropout]
