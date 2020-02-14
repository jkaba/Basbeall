from db_config import *
from constants import *
from sql_queries import *
from classification import *
from descriptive_exploration import *

from sklearn.metrics import accuracy_score
import time

def main():
    print('Training Player Decline Models')
    players_df = pd.read_sql(lahman_query, conn)
    players_df.to_pickle('data/players_df_raw.pkl')

    players_df = clean_database_input(players_df)
    players_df = create_target(players_df)
    players_df.to_pickle('data/players_df_before_training.pkl')
    X_train, X_test, y_train, y_test = machine_learning_prep_classification(players_df, 'target')

    print('Training Models')
    for name, model, param_grid in zip(model_names, models, param_grids):
        run_classification(X_train, X_test, y_train, y_test, name, model, param_grid, 'accuracy',
                           accuracy_score, predict_probas_or_classes='classes')

    return

if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
