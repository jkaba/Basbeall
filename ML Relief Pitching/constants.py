from scipy.stats import uniform
from scipy.stats import randint


tree_param_grid = {'classifier__n_estimators': [20],
                   'classifier__verbose': [3],
                   'classifier__max_features': ['auto', 'sqrt', 'log2'],
                   'classifier__max_depth': randint(3, 10),
                   'classifier__class_weight': [None, 'balanced_subsample',
                                               {0: 1, 1: 2}, {0: 1, 1: 3}, {0: 1, 1: 4}]}


gb_param_grid = {'classifier__learning_rate': uniform(scale=1),
                 'classifier__n_estimators': [10, 25, 50, 75, 100],
                 'classifier__max_depth': randint(3, 10),
                 'classifier__verbose': [3]}


logreg_param_grid = {'classifier__solver': ['sag'],
                     'classifier__C': uniform(scale=1),
                     'classifier__class_weight': [None, 'balanced',
                                                 {0: 1, 1: 2}, {0: 1, 1: 3}, {0: 1, 1: 4}],
                     'classifier__penalty': ['l2'],
                     'classifier__verbose': [3],
                     'classifier__tol': [0.01],
                     'classifier__fit_intercept': [True, False]}


mlp_param_grid = {'classifier__activation': ['tanh', 'relu'],
                  'classifier__solver': ['sgd'],
                  'classifier__alpha': uniform(scale=1),
                  'classifier__learning_rate': ['invscaling', 'adaptive'],
                  'classifier__tol': [0.01],
                  'classifier__early_stopping': [True],
                  'classifier__verbose': [3]}

