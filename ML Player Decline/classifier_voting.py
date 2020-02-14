from classification import run_classification_voting
from constants import voting_param_grid
import pandas as pd
import joblib
from sklearn.metrics import accuracy_score

if __name__ == "__main__":
    X_train = pd.read_pickle('data/X_train.pkl')
    y_train = pd.read_pickle('data/y_train.pkl')
    X_test = pd.read_pickle('data/X_test.pkl')
    y_test = pd.read_pickle('data/y_test.pkl')

    random_forest = joblib.load('models/best_model_random_forest.pkl')
    extra_trees = joblib.load('models/best_model_extra_trees.pkl')
    ada_boost = joblib.load('models/best_model_ada_boost.pkl')
    gradient_boosting = joblib.load('models/best_model_gradient_boosting.pkl')
    logistic_regression = joblib.load('models/best_model_logistic_regression.pkl')

    run_classification_voting(X_train, X_test, y_train, y_test, 'voting_classifier', voting_param_grid, random_forest, extra_trees, ada_boost, gradient_boosting, logistic_regression, 'accuracy', accuracy_score, predict_probas_or_classes='classes')
