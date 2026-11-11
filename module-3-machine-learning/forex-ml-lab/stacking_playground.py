import pandas as pd
import numpy as np
from pathlib import Path
from features import create_features
from sklearn.model_selection import TimeSeriesSplit
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from sklearn.pipeline import make_pipeline
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix, brier_score_loss

def build_meta_model():
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000)
    )
    return model

def build_base_model():
    return {
        'logistic': make_pipeline(
            StandardScaler(),
            LogisticRegression(max_iter=1000)),
        'tree': DecisionTreeClassifier(
            max_depth=3,
            random_state=42),
        'forest': RandomForestClassifier(
            n_estimators=100,
            max_depth=5,
            min_samples_leaf=5,
            random_state=42,
            n_jobs=1)
    }

def main():

    data_path = Path(__file__).parent/'data'/'eur_usd_h1.csv'
    candles_df = pd.read_csv(data_path, parse_dates=['timestamp'])

    # Step 2: Create engineered features

    features_df = create_features(candles_df)

    # Step 3: Create the classification target

    raw_features = ["open", "high", "low", "close", "volume"]

    engineered_features = ['absolute_body', 'candle_range', 'volume', 'current_return', 'previous_return', 'moving_average_5', 'rolling_volatilty_5']

    combined_features = list(dict.fromkeys(raw_features + engineered_features))

    # Step 4: Define X and y / Features and Target

    X = features_df[raw_features]
    X1 = features_df[engineered_features]
    X2 = features_df[combined_features]
    y = features_df['target']

    # Step 5: Split chronologically

    train_end = int(len(features_df)*0.6)
    validation_end = int(len(features_df)*0.8)

    X_train = X.iloc[:train_end - 1]
    X1_train = X1.iloc[:train_end - 1]
    X2_train = X2.iloc[:train_end-1]
    y_train = y.iloc[:train_end - 1]
    
    X_val = X.iloc[train_end:validation_end-1]
    X1_val = X1.iloc[train_end:validation_end-1]
    X2_val = X2.iloc[train_end:validation_end-1]
    y_val = y.iloc[train_end:validation_end-1]

    X_test = X.iloc[validation_end:]
    X1_test = X1.iloc[validation_end:]
    X2_test = X2.iloc[validation_end:]
    y_test = y.iloc[validation_end:]

    tscv = TimeSeriesSplit(
        n_splits=3,
        gap=1
    )

    oof_results = []

    for fold , (train_index, val_index) in enumerate(tscv.split(X2_train), start=1):

        fold_X_train = X2_train.iloc[train_index]
        fold_y_train = y_train.iloc[train_index]

        fold_X_val = X2_train.iloc[val_index]
        fold_y_val = y_train.iloc[val_index]

        models = build_base_model()

        fold_results = pd.DataFrame(index=fold_y_val.index)

        fold_results['fold'] = fold

        for model_name, model in models.items():

            model.fit(fold_X_train, fold_y_train)

            probabilities = model.predict_proba(fold_X_val)[:, 1]

            fold_results[f'{model_name}_probability'] = probabilities

        fold_results['actual_target'] = fold_y_val.to_numpy()

        oof_results.append(fold_results)

    oof_df = pd.concat(oof_results).sort_index()

    meta_features = ['logistic_probability', 'tree_probability', 'forest_probability']
    meta_X = oof_df[meta_features]
    meta_y = oof_df['actual_target']

    meta_model = build_meta_model()
    meta_model = meta_model.fit(meta_X, meta_y)

    meta_coeff = meta_model.named_steps['logisticregression'].coef_
    meta_intercept = meta_model.named_steps['logisticregression'].intercept_

    final_base_models = build_base_model()

    stacking_val_X = pd.DataFrame(index= X2_val.index)

    for model_name, model in final_base_models.items():
        model.fit(X2_train, y_train)
        probabilities = model.predict_proba(X2_val)[:,1]
        stacking_val_X[f'{model_name}_probability'] = probabilities

    
    stacking_prediction = meta_model.predict(stacking_val_X[meta_features])

    stacking_evaluation = {
        'Accuracy' : accuracy_score(y_val, stacking_prediction),
        'Precision' : precision_score(y_val, stacking_prediction, zero_division=0),
        'Recall' : recall_score(y_val, stacking_prediction, zero_division=0),
        'F1 score' : f1_score(y_val, stacking_prediction, zero_division=0),
        'Confusion Matrix' : confusion_matrix(y_val, stacking_prediction, labels=[0,1])
        }

    stacking_probabilities = meta_model.predict_proba(stacking_val_X[meta_features])[:,1]

    brier = brier_score_loss(y_val, stacking_probabilities)

    baseline_probability = y_train.mean()
    baseline_probabilities = np.full(len(y_val), baseline_probability)

    baseline_brier = brier_score_loss(y_val, baseline_probabilities)


    # print(oof_df.head())
    # print('OOF rows:', len(oof_df))
    # print(meta_coeff)
    # print(meta_intercept)

    # print('Stacking val X')
    # print(stacking_val_X.head())
    # print('Stacking evaluation')
    # for x,y in stacking_evaluation.items():
    #     print(f'{x}: \n {y}')
    # print("OOF probability summary:")
    # print(meta_X.describe())

    # print("Validation probability summary:")
    # print(stacking_val_X.describe())

    print(f'Brier Score Loss: {brier:.4f}')
    print(f'Baseline Brier Score Loss: {baseline_brier:.4f}')
if __name__ =='__main__':
    main()