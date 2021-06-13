import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os, joblib
from sklearn.metrics.pairwise import cosine_similarity
from operator import itemgetter
from .data_retriever import FeatureFinder


class ArtistRecommender:
    def __init__(self):
        my_dir = os.path.dirname(__file__)
        parent_directory = os.path.split(my_dir)[0]

        feat_dir = os.path.join(parent_directory, 'MyData', 'artist_features.csv')
        self.artist_feats = pd.read_csv(feat_dir)

        scaler_dir = os.path.join(parent_directory, 'MyData', 'artist_feature_scaler.save')
        self.scaler = joblib.load(scaler_dir)

        CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
        CLIENT_SECRET = os.environ.get('SPOTIFY_SECRET_ID')
        self.FF = FeatureFinder(CLIENT_ID, CLIENT_SECRET)
        self.sp = self.FF.sp


    def _get_artist_id(self, artist_name):
        try:
            results = self.sp.search(q='artist:' + artist_name, type='artist')
            items = results['artists']['items']
            artist_id = items[0]['id']
            artist_name = items[0]['name']
            url = items[0]["external_urls"]["spotify"]
            return artist_id, artist_name, url

        except:
            raise ValueError(f'Artist not found: {artist_name}')

    def find_similar_artists(self, artist_name, number_recos=5):
        """
        Called at runtime by the user to retrieve their artist recommendations
        Combines all of the above functions

        """
        artist_id, artist_name, og_url = self._get_artist_id(artist_name)
        artist_vector = self.FF.get_artist_song_feats(artist_id)
        artist_vector = self.scaler.transform([artist_vector])

        scaled = self.artist_feats.copy()


        scaled['cosine_sim'] = scaled.iloc[:, 3:].apply(lambda row: cosine_similarity(artist_vector, [row])[0][0],
                                                        axis=1)
        scaled = scaled.sort_values(by=['cosine_sim'], ascending=False)

        top_vals = {}
        for i in range(number_recos):
            row = scaled.iloc[i]
            artist = row['artist_name']
            url = row['url']
            sim = row['cosine_sim']
            top_vals[artist] = {'url': url,
                           'sim': sim}

        scaled.drop(columns=['cosine_sim'], inplace=True)

        return top_vals, artist_name, og_url
