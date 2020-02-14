# Import Statements
from constants import *
from regression import *

# train_neural_nets function
# This function trains the neural nets
def train_neural_nets():
    print('training neural nets')

    # Load pre-processed data
    players_df = pd.read_pickle('players_df_pre_processed.pkl')

    # Create training and testing data
    X_train, X_test, y_train, y_test = machine_learning_prep(players_df, 'target')

    X_train = X_train.values
    X_test = X_test.values
    y_train = y_train.values
    y_test = y_test.values

    # Train neural nets
    print('training the models')
    for name, model in zip(nn_names, nn_models):
        run_neural_network(X_train, X_test, y_train, y_test, name, model)

    return

