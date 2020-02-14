import pickle
import pandas as pd

from scipy.stats import uniform
from scipy.stats import randint

from sklearn.metrics import roc_auc_score
from sklearn.pipeline import Pipeline, make_pipeline
from sklearn.model_selection import cross_val_score, GridSearchCV, RandomizedSearchCV
from sklearn.preprocessing import MinMaxScaler, Imputer
from sklearn.model_selection import train_test_split

from sklearn.ensemble import VotingClassifier, BaggingClassifier, AdaBoostClassifier, RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from mlxtend.classifier import StackingClassifier

# machine_learning_prep_classification
# This function prepares the data and runs the ML models
def machine_learning_prep_classification(df, dependent_variable):

    df[dependent_variable]= df[dependent_variable].astype('int')
    Y = df[dependent_variable]

    X = df.drop([dependent_variable], axis=1)
    X = pd.get_dummies(X)
    X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.10, random_state=19)

    X_train.to_pickle('X_train.pkl')
    X_train.to_csv('X_train.csv', index=False)
    Y_train.to_pickle('Y_train.pkl')
    X_test.to_pickle('X_test.pkl')
    Y_test.to_pickle('Y_test.pkl')

    return X_train, X_test, Y_train, Y_test

# run_classification function
# This function is used to train the ML models
def run_classification(X_train, X_test, Y_train, Y_test, model_name, model, param_grid):

    print('training {}').format(model_name)

    # Set up pipeline
    pipe = Pipeline([('imputer', Imputer(strategy='most_frequent')),
                     ('scaler', MinMaxScaler()),
                     ('classifier', model)])

    # Conduct randomized search to tune parameters
    search = RandomizedSearchCV(pipe, param_distributions=param_grid, cv=5, n_iter=10, scoring='roc_auc')
    search.fit(X_train, Y_train)
    pd.DataFrame(search.cv_results_).to_csv(model_name + '_grid_search_results.csv', index=False)

    # Pickle the best estimator
    clf = search.best_estimator_
    pickle.dump(clf, open('best_pipeline_' + model_name + '.pkl', 'wb'))
    pickle.dump(clf.named_steps['classifier'], open('best_model_' + model_name + '.pkl', 'wb'))

    # Evaluate the results on the test set
    predict = clf.predict_proba(X_test)
    roc_auc = roc_auc_score(Y_test, predict[:, 1])

    test_set = pd.DataFrame({'roc_auc_score_on_test_set': roc_auc})
    test_set.to_csv(model_name + '_results_on_test_set.csv', index=False)
    return


# run_classification_bagging function
# This function is used to train for bagging classification
def run_classification_bagging(X_train, X_test, Y_train, Y_test, model_name, model):

    print('training bagging classification for {}').format(model_name)

    pipe = Pipeline([('imputer', Imputer(strategy='most_frequent')),
                     ('scaler', MinMaxScaler()),
                     ('classifier', BaggingClassifier())])

    bagging_param_grid = {'classifier__base_estimator': [model],
                          'classifier__n_estimators': [10],
                          'classifier__max_samples': uniform(scale=1),
                          'classifier__max_features': uniform(scale=1),
                          'classifier__boostrap': [True, False],
                          'classifier__bootstrap_features': [True, False],
                          'classifier__verbose': [3]}

    search = RandomizedSearchCV(pipe, param_distributions=bagging_param_grid, cv=5, n_iter=10, scoring='roc_auc')
    search.fit(X_train, Y_train)
    pd.DataFrame(search.cv_results_).to_csv(model_name + '_grid_search_results.csv', index=False)

    clf = search.best_estimator_
    pickle.dump(clf, open('best_pipeline_' + model_name + '.pkl', 'wb'))
    pickle.dump(clf.named_steps['classifier'], open('best_model_' + model_name + '.pkl', 'wb'))

    predict = clf.predict_proba(X_test)
    roc_auc = roc_auc_score(Y_test, predict[:, 1])

    test_set = pd.DataFrame({'roc_auc_score_on_test_set': roc_auc})
    test_set.to_csv(model_name + '_results_on_test_set.csv', index=False)
    return

# run_classification_boosting function
# This function is used for boosting classifier training
def run_classification_boosting(X_train, X_test, Y_train, Y_test, model_name, model):

    print('training boosting classification for {}').format(model_name)

    pipe = Pipeline([('imputer', Imputer(strategy='most_frequent')),
                     ('scaler', MinMaxScaler()),
                     ('classifier', AdaBoostClassifier())])

    boosting_param_grid = {'classifier__base_estimator': [model],
                           'classifier__learning_rate': uniform(scale=10),
                           'classifier__n_estimators': randint(0, 100)}

    search = RandomizedSearchCV(pipe, param_distributions=boosting_param_grid, cv=5, n_iter=10, scoring='roc_auc')
    search.fit(X_train, Y_train)
    pd.DataFrame(search.cv_results_).to_csv(model_name + '_grid_search_results.csv', index=False)

    clf = search.best_estimator_
    pickle.dump(clf, open('best_pipeline_' + model_name + '.pkl', 'wb'))
    pickle.dump(clf.named_steps['classifier'], open('best_model_' + model_name + '.pkl', 'wb'))

    predict = clf.predict_proba(X_test)
    roc_auc = roc_auc_score(Y_test, predict[:, 1])

    test_set = pd.DataFrame({'roc_auc_score_on_test_set': roc_auc})
    test_set.to_csv(model_name + '_results_on_test_set.csv', index=False)
    return

# run_classification_voting function
# This function is used to create groups of ML models, and trains for voting classification
def run_classification_voting(X_train, X_test, Y_train, Y_test, model_name, param_grid, model_1, model_2, model_3, model_4):

    print('running voting classifier')

    voting_estimators = [
        ('model_1', model_1), ('model_2', model_2), ('model_3', model_3), ('model_4', model_4)
    ]

    pipe = Pipeline([('imputer', Imputer(strategy='most_frequent')),
                     ('scaler', MinMaxScaler()),
                     ('classifier', VotingClassifier(estimators=voting_estimators, voting='soft'))])

    search = GridSearchCV(pipe, param_grid=param_grid, cv=3, scoring='roc_auc')
    search.fit(X_train, Y_train)
    pd.DataFrame(search.cv_results_).to_csv(model_name + '_grid_search_results.csv', index=False)

    clf = search.best_estimator_
    pickle.dump(clf, open('best_pipeline_' + model_name + '.pkl', 'wb'))

    predict = clf.predict_proba(X_test)
    roc_auc = roc_auc_score(Y_test, predict[:, 1])

    test_set = pd.DataFrame({'roc_auc_score_on_test_set': roc_auc})
    test_set.to_csv(model_name + '_results_on_test_set.csv', index=False)
    return

# run_classification_stacking function
# This function is used for training a stacking classifier
def run_classification_stacking(X_train, X_test, Y_train, Y_test, model_name, model_1, model_2, model_3, model_4, meta_classifier_choice='log_reg'):

    print('running stacked classifier')

    stacking_estimators = [model_1, model_2, model_3, model_4]

    if meta_classifier_choice == 'log_reg':
        model = LogisticRegression(solver='sag')
    elif meta_classifier_choice == 'random_forest':
        model = RandomForestClassifier(n_estimators=20)

    pipe = Pipeline([('imputer', Imputer(strategy='most_frequent')),
                     ('scaler', MinMaxScaler()),
                     ('classifier', StackingClassifier(classifiers=stacking_estimators, meta_classifier=model))])

    param_grid = {'classifier__use_probas': [True],
                  'classifier__average_probas': [False]}

    search = GridSearchCV(pipe, cv=3, param_grid= param_grid, scoring='roc_auc')
    search.fit(X_train, Y_train)
    pd.DataFrame(search.cv_results_).to_csv(model_name + '_grid_search_results.csv', index=False)

    clf = search.best_estimator_
    pickle.dump(clf, open('best_pipeline_' + model_name + '.pkl', 'wb'))

    predict = clf.predict_proba(X_test)
    roc_auc = roc_auc_score(Y_test, predict[:, 1])

    test_set = pd.DataFrame({'roc_auc_score_on_test_set': roc_auc})
    test_set.to_csv(model_name + '_results_on_test_set.csv', index=False)
    return
