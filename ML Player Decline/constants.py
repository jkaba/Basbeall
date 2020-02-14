from scipy.stats import uniform
from scipy.stats import randint

from sklearn.ensemble import ExtraTreesClassifier, AdaBoostClassifier, RandomForestClassifier, \
    GradientBoostingClassifier
from sklearn.linear_model import LogisticRegression


tree_param_grid = {'imputer__strategy': ['mean', 'most_frequent'],
                   'classifier__max_features': ['auto', 'sqrt', 'log2'],
                   'classifier__max_depth': randint(3, 10),
                   'classifier__class_weight': [None, 'balanced_subsample']}


gb_param_grid = {'imputer__strategy': ['mean', 'most_frequent'],
                 'classifier__learning_rate': uniform(scale=1),
                 'classifier__n_estimators': randint(10, 100),
                 'classifier__max_depth': randint(3, 10)}


ada_param_grid = {'imputer__strategy': ['mean', 'most_frequent'],
                  'classifier__learning_rate': uniform(scale=2),
                  'classifier__n_estimators': randint(10, 100)}


logreg_param_grid = {'imputer__strategy': ['mean', 'most_frequent'],
                     'classifier__C': uniform(scale=10),
                     'classifier__class_weight': [None, 'balanced'],
                     'classifier__fit_intercept': [True, False]}


voting_param_grid = {
    'classifier__weights': [
        [1, 1, 1, 1, 1],

        [1.25, 1, 1, 1, 1],
        [1, 1.25, 1, 1, 1],
        [1, 1, 1.25, 1, 1],
        [1, 1, 1, 1.25, 1],
        [1, 1, 1, 1, 1.25],

        [1.50, 1, 1, 1, 1],
        [1, 1.50, 1, 1, 1],
        [1, 1, 1.50, 1, 1],
        [1, 1, 1, 1.50, 1],
        [1, 1, 1, 1, 1.50],

        [2, 1, 1, 1, 1],
        [1, 2, 1, 1, 1],
        [1, 1, 2, 1, 1],
        [1, 1, 1, 2, 1],
        [1, 1, 1, 1, 2]
    ]
}


model_names = ['random_forest', 'extra_trees', 'ada_boost', 'logistic_regression',  'gradient_boosting',]


models = [RandomForestClassifier(n_estimators=100), ExtraTreesClassifier(n_estimators=100), AdaBoostClassifier(),
          LogisticRegression(solver='sag', penalty='l2'), GradientBoostingClassifier()]


param_grids = [tree_param_grid, tree_param_grid, ada_param_grid, logreg_param_grid, gb_param_grid]
