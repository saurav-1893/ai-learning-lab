import pandas as pd
import numpy as np
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import silhouette_score

dataset = {
    'candle': ['A', 'B', 'C', 'D', 'E', 'F'],
    'range': [4, 5, 6, 20, 22, 19],
    'volume': [1000, 1200, 1100, 8000, 8500, 7800]
}

data = pd.DataFrame(dataset)
features = ['range', 'volume']
X = data[features]
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)
model = KMeans(n_clusters=2, random_state=42)
new_cluster = model.fit_predict(X_scaled)
new_inertia = model.inertia_

data['cluster'] = new_cluster
zero_cluster_data = data[data['cluster']==0]

k_values = [1, 2, 3, 4, 5]

inertia_results = []

for k in range(1,6):
    model = KMeans(
        n_clusters=k,
        random_state=42,
        n_init=10
    )

    # Fit model using X_scaled
    cluster_labels = model.fit_predict(X_scaled)

    # Read model.inertia_
    k_inertia= model.inertia_
    
    if k>= 2:
        sil_score = silhouette_score(X_scaled, cluster_labels)
    else:
        sil_score = np.nan
    # Append k and inertia to inertia_results 
    inertia_results.append({'k': k, 'inertia': k_inertia, 'silhouette score': sil_score })

inertia_df = pd.DataFrame(inertia_results)
# print(zero_cluster_data)
# print(f'Zero cluster data Range mean: {(zero_cluster_data['range']).mean()}')
# print(f'Zero cluster data Volume mean: {(zero_cluster_data['volume']).mean()}')
# print(data.groupby('cluster')[['range', 'volume']].mean())
# print('\nCluster assignments:')
# print(data)
# print('\nCluster centres (scaled):')
# print(model.cluster_centers_)
# print('\nCluster centres (original units):')
# print(scaler.inverse_transform(model.cluster_centers_))

print([new_inertia])
print(inertia_df)
