import joblib
import numpy as np

from sklearn.pipeline import Pipeline
from sklearn.model_selection import RandomizedSearchCV, GridSearchCV
from sklearn.preprocessing import MinMaxScaler, Imputer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import VotingClassifier

from helpers import *


def machine_learning_prep_classification(df, dependent_variable):
    df[dependent_variable] = df[dependent_variable].astype('int')
    y = df[dependent_variable]
    X = df.drop([dependent_variable], axis=1)
    X = pd.get_dummies(X)
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=19)

    X_train.to_csv('data/X_train.csv', index=False)
    y_train.to_csv('data/y_train.csv', index=False)
    X_test.to_csv('data/X_test.csv', index=False)
    y_test.to_csv('data/y_test.csv', index=False)

    X_train.to_pickle('data/X_train.pkl')
    y_train.to_pickle('data/y_train.pkl')
    X_test.to_pickle('data/X_test.pkl')
    y_test.to_pickle('data/y_test.pkl')
    return X_train, X_test, y_train, y_test


def run_classification(X_train, X_test, Y_train, Y_test, model_name, model, param_grid, cv_scorer, test_set_scorer,
                       predict_probas_or_classes='classes'):

    print('training {}').format(model_name)

    # Set up pipeline
    pipe = Pipeline([('imputer', Imputer()),
                     ('scaler', MinMaxScaler()),
                     ('classifier', model)])

    # Conduct randomized search to tune parameters
    search = RandomizedSearchCV(pipe, param_distributions=param_grid, cv=10, n_iter=50, scoring=cv_scorer, verbose=3)
    search.fit(X_train, Y_train)
    pd.DataFrame(search.cv_results_).to_csv('diagnostics/' + model_name + '_grid_search_results.csv', index=False)

    # Pickle the best estimator
    clf = search.best_estimator_
    joblib.dump(clf, 'models/best_pipeline_' + model_name + '.pkl')
    joblib.dump(clf.named_steps['classifier'], 'models/best_model_' + model_name + '.pkl')

    # Evaluate the results on the test set
    if predict_probas_or_classes == 'probas':
        predictions = clf.predict_proba(X_test)
        score = test_set_scorer(Y_test, predictions[:, 1])

    if predict_probas_or_classes == 'classes':
        predictions = clf.predict(X_test)
        score = test_set_scorer(Y_test, predictions)

    test_set = pd.DataFrame({'score_on_test_set': [score]})
    test_set.to_csv('diagnostics/' + model_name + '_results_on_test_set.csv', index=False)
    return


def run_classification_voting(X_train, X_test, Y_train, Y_test, model_name, param_grid, model_1, model_2, model_3,
                              model_4, model_5, cv_scorer, test_set_scorer, predict_probas_or_classes='classes'):
    print('running voting classifier')

    voting_estimators = [
        ('model_1', model_1), ('model_2', model_2), ('model_3', model_3), ('model_4', model_4), ('model_5', model_5)
    ]

    pipe = Pipeline([('imputer', Imputer()),
                     ('scaler', MinMaxScaler()),
                     ('classifier', VotingClassifier(estimators=voting_estimators, voting='soft'))])

    search = GridSearchCV(pipe, param_grid=param_grid, cv=5, scoring=cv_scorer, verbose=2)
    search.fit(X_train, Y_train)
    pd.DataFrame(search.cv_results_).to_csv('diagnostics/' + model_name + '_grid_search_results.csv', index=False)

    clf = search.best_estimator_
    joblib.dump(clf, 'models/best_pipeline_' + model_name + '.pkl')

    # Evaluate the results on the test set
    if predict_probas_or_classes == 'probas':
        predictions = clf.predict_proba(X_test)
        score = test_set_scorer(Y_test, predictions[:, 1])

    if predict_probas_or_classes == 'classes':
        predictions = clf.predict(X_test)
        score = test_set_scorer(Y_test, predictions)

    test_set = pd.DataFrame({'score_on_test_set': [score]})
    test_set.to_csv('diagnostics/' + model_name + '_results_on_test_set.csv', index=False)
    return


def build_proba_table(model, x_test_set, y_test_set, name):
    predictions = model.predict_proba(x_test_set)
    predictions = pd.DataFrame(predictions)
    predictions.columns = ['0_prob', '1_prob']
    result = pd.DataFrame(pd.concat([predictions, y_test_set], axis=1, ignore_index=True))
    result.columns = ['0_prob', '1_prob', 'actual_label']
    result.to_csv('diagnostics/' + name + '_test_set_predictions.csv', index=False)

    result.drop('0_prob', axis=1, inplace=True)
    result.reset_index(drop=True, inplace=True)

    result_bins = np.arange(0.0, 1.1, 0.05)
    result_bins_df = pd.DataFrame(result_bins)
    result['result_bins'] = pd.cut(result['1_prob'], bins=result_bins, right=False)

    proba_table_count = result.groupby('result_bins').agg({'actual_label': ['count']})
    proba_table_mean = result.groupby('result_bins').agg({'actual_label': ['mean']})

    proba_table = pd.concat([proba_table_count, proba_table_mean], axis=1)
    proba_table.columns = proba_table.columns.droplevel(0)
    proba_table.reset_index(inplace=True, drop=True)
    proba_table = pd.concat([result_bins_df, proba_table], axis=1)
    proba_table.columns = ['proba_bin', 'predictions', 'actual_rate']

    min_proba = pd.DataFrame(result_bins, columns=['min_proba'])
    max_bins = np.arange(0.0499, 0.999, 0.05)
    max_proba = pd.DataFrame(max_bins, columns=['max_proba'])

    proba_table = pd.concat([min_proba, max_proba, proba_table], axis=1)
    proba_table.to_csv('data/' + name + '_proba_table.csv', index=False)
    return
