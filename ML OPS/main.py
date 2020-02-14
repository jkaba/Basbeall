# Import Statements
from sklearn.preprocessing import FunctionTransformer
from data_in import *
from neural_nets import *
from db_config import conn

# Main Method
def main():
    print('Running Player Projection Analysis')

    # Take in the data
    print('Ingesting Data')
    players_df = pd.read_sql(lahman_master_query, conn)
    awards_df = pd.read_sql(awards_query, conn)
    all_stars_df = pd.read_sql(all_star_query, conn)

    players_df.to_pickle('players_df.pkl')
    awards_df.to_pickle('awards_df.pkl')
    all_stars_df.to_pickle('all_stars.pkl')

    # Perform pre-processing
    # For pre-processing 2 pipleines are used for this project
    # 1. Directly below
    # 2. Run Regression Function
    # These pipelines are seperated as most of the pre-processing is a result of how data is stored
    
    print('Pre-processing Data')
    pre_processing_pipe = Pipeline([('dupe_dropper', FunctionTransformer(drop_duplicates, validate=False)), ('perform_cleaning', FunctionTransformer(perform_cleaning, validate=False)), ('clean_awards', FunctionTransformer(clean_award_variables, validate=False, kw_args={'awards_df': awards_df, 'all_stars_df': all_stars_df})), ('create_target', FunctionTransformer(create_target, validate=False)), ('column_dropper', FunctionTransformer(drop_columns, validate=False)), ('create_lags', FunctionTransformer(create_lagged_variables, validate=False))])

    players_df = pre_processing_pipe.transform(players_df)
    players_df.to_pickle('players_df_pre_processed.pkl')
    pickle.dump(pre_processing_pipe, open('pre_processing_pipe.pkl', 'wb'))
    X_train, X_test, y_train, y_test = machine_learning_prep(players_df, 'target')

    # Train Models
    print('Training Models')
    for name, model, param_grid in zip(model_names, models, param_grids):
        run_regression(X_train, X_test, y_train, y_test, name, model, param_grid)

    return

if __name__ == "__main__":
    main()
    train_neural_nets()
