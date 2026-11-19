import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA

data = pd.DataFrame({
    'range': [5, 10, 15, 20],
    'volume': [1000, 2000, 3000, 4000],
    'volatility': [0.0003, 0.0006, 0.0009, 0.0012]
})
X = data[['range', 'volume', 'volatility']]

scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

pca = PCA(n_components=1)

X_pca = pca.fit_transform(X_scaled)

print(f'Princial comonent weights : {pca.components_}')
print(f'Explained variance ratio : {pca.explained_variance_ratio_}')

print(f'Transformed data: \n{X_pca}')
print(f'Original shape: {X_scaled.shape}')
print(f'Transformed shape: {X_pca.shape}')
