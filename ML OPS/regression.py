from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.model_selection import GridSearchCV, cross_val_score
from sklearn.preprocessing import StandardScaler, Imputer
from keras.wrappers.scikit_learn import KerasRegressor

import joblib
import sys

from helpers import *

sys.setrecursionlimit(5000)

# run_regression function
# This function defines the regression for this project
def run_regression(X_train, X_test, y_train, y_test, model_name, model, param_grid):
    print('training {}').format(model_name)

    # Set up pipeline
    pipe = Pipeline([('imputer', Imputer(strategy='mean')),
                     ('scaler', StandardScaler()),
                     ('regressor', model)])

    # Conduct grid search to tune parameters
    search = GridSearchCV(pipe, param_grid=param_grid, cv=10, scoring='mean_squared_error', verbose=1)
    search.fit(X_train, y_train)
    pd.DataFrame(search.cv_results_).to_csv(model_name + '_grid_search_results.csv', index=False)

    # Pickle the best estimator
    clf = search.best_estimator_
    pickle.dump(clf, open('best_pipeline_' + model_name + '.pkl', 'wb'))
    pickle.dump(clf.named_steps['regressor'], open('best_model_' + model_name + '.pkl', 'wb'))

    # Evaluate the results on the test set
    predict = clf.predict(X_test)
    score = mean_squared_error(y_test, predict)

    test_set = [{'score_on_test_set': score}]
    test_set = pd.DataFrame(test_set)
    test_set.to_csv(model_name + '_results_on_test_set.csv', index=False)
    return

# run_neural_network function
# This function does at is says and runs the neural network
def run_neural_network(X_train, X_test, y_train, y_test, model_name, model):
    print('training {}').format(model_name)

    # Set up pipeline
    pipe = Pipeline([('imputer', Imputer(strategy='mean')),
                     ('scaler', StandardScaler()),
                     ('regressor', KerasRegressor(build_fn=model, epochs=10, batch_size=500, verbose=1))])

    # Cross validate on the training set
    cv_scores = cross_val_score(pipe, X_train, y_train, cv=3)
    model_results_df = pd.DataFrame([{'mean_cv_scores': cv_scores.mean()}])
    mean_results = model_results_df.loc[model_results_df['mean_cv_scores'].idxmax()]
    mean_results.to_csv('mean_results_' + model_name + '.csv', index=False)

    # Make predictions on the test set
    pipe.fit(X_train, y_train)
    joblib.dump(pipe, 'pipeline_' + model_name + '.pkl')

    predict = pipe.predict(X_test)
    score = mean_squared_error(y_test, predict)
    test_set = pd.DataFrame([{'score_on_test_set': score}])
    test_set.to_csv(model_name + '_results_on_test_set.csv', index=False)
    return
