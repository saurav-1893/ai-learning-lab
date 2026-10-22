from fetch_data import fetch_candles

def create_features(df):
    features_df = df.copy()

    # 1. Create absolute_body
    features_df['absolute_body'] = abs(features_df['close'] - features_df['open'])
    # 2. Create signed_body
    features_df['signed_body'] = (features_df['close'] - features_df['open'])
    # 3. Create candle_range
    features_df['candle_range'] = (features_df['high'] - features_df['low'])

    features_df['next_close'] = features_df['close'].shift(-1)
    features_df = features_df.dropna(subset=['next_close']).copy()
    features_df['target'] = (features_df['next_close'] > features_df['close']).astype(int)
    features_df['current_return'] = (features_df['close'].pct_change())
    features_df['previous_return'] = (features_df['current_return'].shift(1))
    features_df['moving_average_5'] = features_df['close'].rolling(5).mean()
    features_df['rolling_volatilty_5'] = features_df['current_return'].rolling(5).std()

    required_features = ['current_return', 'previous_return', 'moving_average_5', 'rolling_volatilty_5']
    features_df = features_df.dropna(subset= required_features).copy()
    features_df = features_df.reset_index(drop=True)

    return features_df

if __name__ == '__main__':

    candles_df = fetch_candles()


    features_df = create_features(candles_df)

    print(features_df.head(10))