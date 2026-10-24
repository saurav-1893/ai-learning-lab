import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, precision_score, recall_score, confusion_matrix, f1_score  
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.dummy import DummyClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier


from pathlib import Path
from features import create_features

def build_model():
    model = make_pipeline(
        StandardScaler(),
        LogisticRegression(max_iter=1000)
    )
    return model

def build_tree_model():
    return DecisionTreeClassifier(max_depth=3, random_state=42)

def train_model(model, X_train, y_train):
    model.fit(X_train, y_train)
    return model

def build_forest_model():
    return RandomForestClassifier(max_depth=5, n_estimators=100, min_samples_leaf=5, random_state=42, n_jobs=1)
    

def evaluate_model(model, X_eval, y_eval):
    predictions = model.predict(X_eval)
    results = {
        'accuracy' : accuracy_score(y_eval, predictions),
        'precision' : precision_score(y_eval, predictions, zero_division=0),
        'recall' : recall_score(y_eval, predictions, zero_division=0),
        'F1': f1_score(y_eval, predictions, zero_division=0)
     }
    return results

def main():

    # Step 1: Fetch historical candles

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

    # Step 6: Build and Train the model

    raw_model = build_model()
    engineered_model = build_model()

    baseline_model = DummyClassifier(strategy='most_frequent')
    baseline_model_combo = DummyClassifier(strategy='most_frequent')
    

    raw_tree_model = build_tree_model()
    engineered_tree_model = build_tree_model()
    tree_model_combo = build_tree_model()

    raw_forest_model = build_forest_model()
    engineered_forest_model =build_forest_model()
    forest_model_combo =build_forest_model()
    
    raw_model = train_model(raw_model, X_train, y_train)
    engineered_model = train_model(engineered_model, X1_train, y_train)
    baseline_model = train_model(baseline_model, X_train, y_train)
    baseline_model_combined = train_model(baseline_model_combo, X2_train, y_train)

    tree_model_raw = train_model(raw_tree_model,X_train,y_train)
    tree_model_engineered = train_model(engineered_tree_model,X1_train,y_train)
    tree_model_combined = train_model(tree_model_combo, X2_train, y_train)

    forest_model_raw = train_model(raw_forest_model, X_train,y_train)
    forest_model_engineered = train_model(engineered_forest_model, X1_train, y_train)
    forest_model_combined = train_model(forest_model_combo, X2_train, y_train)

    # predictions = model.predict(X_test)

    # Step 7: Predict and evaluate

    raw_validation_results = evaluate_model(raw_model, X_val, y_val)
    # raw_results = evaluate_model(raw_model, X_test, y_test)
    
    engineered_validation_results = evaluate_model(engineered_model, X1_val, y_val)
    # engineered_results = evaluate_model(engineered_model, X1_test, y_test)

    baseline_validation_results = evaluate_model(baseline_model, X_val, y_val)

    baseline_validation_combined_results = evaluate_model(baseline_model_combined, X2_val, y_val)

    raw_tree_validation_results = evaluate_model(tree_model_raw, X_val, y_val)

    engineered_tree_validation_results = evaluate_model(tree_model_engineered, X1_val, y_val)

    tree_validation_combined_results = evaluate_model(tree_model_combined, X2_val, y_val)

    raw_forest_validation_results = evaluate_model(forest_model_raw, X_val, y_val)

    engineered_forest_validation_results = evaluate_model(forest_model_engineered, X1_val, y_val)

    forest_validation_combined_results = evaluate_model(forest_model_combined, X2_val, y_val)

    
    comparison = pd.DataFrame({
        'Baseline_validation': baseline_validation_results,

        'Raw_validation':raw_validation_results,
        # 'Raw' : raw_results,
        'Engineered_validation': engineered_validation_results,
        # 'Engineered' : engineered_results

        'Baseline_Combined': baseline_validation_combined_results,

        'Raw_Tree_validation': raw_tree_validation_results,

        'Engineered_Tree_validation': engineered_tree_validation_results,

        'Tree_Combined': tree_validation_combined_results,

        'Raw_Forest_validation': raw_forest_validation_results,

        'Engineered_Forest_validation': engineered_forest_validation_results,

        'Forest_combined': forest_validation_combined_results        
    })

    # print(f'Total rows trained : {len(X_train)}')
    # print(f'Total rows validated : {len(X_val)}')
    # print(f'Total rows tested : {len(X_test)}')
    # print('Training class distribution')
    # print(y_train.value_counts())
    # print('Baseline predicted class')
    # print(baseline_model.classes_)
    # print(baseline_model.predict(X_val[:5]))

    # print(f'Comparison in percentage: \n{comparison*100}')
    # print("Rows:", len(candles_df))
    # print("First candle:", candles_df['timestamp'].min())
    # print("Last candle:", candles_df['timestamp'].max())

    # depth_results = []

    # for depth in [2,3,5,10,20]:
        
    #     tree = DecisionTreeClassifier(max_depth= depth, random_state= 42)

    #     tree.fit(X1_train, y_train)

    #     predictions = tree.predict(X1_val)

    #     train_metrics = evaluate_model(tree, X1_train, y_train)

    #     validation_metrics = evaluate_model(tree, X1_val, y_val)

    #     depth_results.append({
    #         'depth' :depth,
    #         'train_accuracy':train_metrics['accuracy'],
    #         'validation_accuracy':validation_metrics['accuracy'],
    #         'train_F1':train_metrics['F1'],
    #         'validation_F1':validation_metrics['F1']
    #     })

    # depth_df = pd.DataFrame(depth_results)
    # print(depth_df)
        # print(f'Depth : {depth}')
        # print(confusion_matrix(y_val, predictions, labels=[0,1]))

    feature_set = {
        'Raw' : X_train,
        'Engineered': X1_train,
        'Combined': X2_train
        }

    validation_set = {
        "Raw": X_val,
        "Engineered": X1_val,
        "Combined": X2_val
        }
    
    model_builders = {
        'Logistic Regression' : build_model,
        'Tree Model' : build_tree_model,
        'Random Forest' : build_forest_model
        }

    total_results = {}

    for model_name, builder in model_builders.items():
        for feature_name, train_features in feature_set.items():

            validation_feature = validation_set[feature_name]

            model = builder()
            # model = model.fit(train_features, y_train)

            model = train_model(model, train_features, y_train)

            results = evaluate_model(model, validation_feature, y_val)

            total_results[f'{model_name} {feature_name}'] = results



    total_results = pd.DataFrame(total_results)
    print(total_results)


    output_path = Path(__file__).parent/'model_testing'/'model_results.csv'
    output_path.parent.mkdir(parents=True, exist_ok=True)
    total_results.to_csv(output_path, index= False)
    




if __name__ == '__main__':
    main()