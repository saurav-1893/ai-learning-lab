from features import create_features
from pathlib import Path
import pandas as pd
from sklearn.pipeline import make_pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
import numpy as np

def main():

    data_path = Path(__file__).parent/'data'/'eur_usd_h1.csv'
    candles_df = pd.read_csv(data_path, parse_dates= ['timestamp'])
    engineered_df = create_features(candles_df)
    clustering_columns = ['candle_range', 'volume','rolling_volatilty_5' ]
    clustering_X = engineered_df[clustering_columns]
    clustering_X = clustering_X.dropna().copy()
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(clustering_X)

    results = []
    for k in range(2,5):
        model = KMeans(random_state=42, n_clusters= k, n_init=10)
        cluster_label = model.fit_predict(X_scaled)

        model_inertia = model.inertia_
 
        model_sil_score = silhouette_score(X_scaled, cluster_label)
        
        results.append({'k': k, 'Inertia' : model_inertia, 'Silhouette Score' : model_sil_score})

    results_df = pd.DataFrame(results)

    new_model = KMeans(n_clusters=2, random_state=42,n_init=10)
    k_2_label = new_model.fit_predict(X_scaled)
    clustering_X['cluster'] = k_2_label

    
    
    cluster_analysis = clustering_X.copy()

    cluster_analysis['target'] = engineered_df.loc[cluster_analysis.index, 'target']

    cluster_summary = cluster_analysis.groupby('cluster').agg(
        candles=('target', 'size'),
        up_frequency=('target', 'mean'),
        average_range=('candle_range', 'mean'),
        average_volume=('volume', 'mean'),
        average_volatility=('rolling_volatilty_5', 'mean')
    )

    print(f' K 2-4 Cluster report:\n{results_df.to_string(index=False)}')
    print(cluster_summary)
    


    # print(new_df)
    # print(new_model.cluster_centers_)
    # print(new_model.inertia_)
    # print(new_model.n_iter_)

if __name__ == '__main__':
    main()
