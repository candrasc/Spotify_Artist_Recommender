from sklearn.preprocessing import StandardScaler
from utils.data_retriever import FeatureFinder
import os, joblib
import pandas as pd


playlist_uris = ["spotify:playlist:7bLzIyyGRUJw78eHtUZItf"]



def main():
    """
    This script is used to create our artist data that we can make recommendations from.
    We also save our scaler so that we can scale retrieved artist features that the user inputs

    """

    CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
    CLIENT_SECRET = os.environ.get('SPOTIFY_SECRET_ID')

    FF = FeatureFinder(CLIENT_ID, CLIENT_SECRET)

    artist_df = FF.create_artist_df_with_features(playlist_uris)

    SS = StandardScaler()

    SS.fit(artist_df.iloc[:, 3:])
    artist_df.iloc[:, 3:] = SS.transform(artist_df.iloc[:, 3:])

    joblib.dump(SS, "MyData/artist_feature_scaler.save")
    pd.read_csv("MyData/artist_features.csv")

if __name__ == '__main__':
    main()