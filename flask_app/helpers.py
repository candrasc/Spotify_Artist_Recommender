import pandas as pd
import numpy as np
import spotipy
import spotipy.util as util
from spotipy.oauth2 import SpotifyClientCredentials
import os, json, joblib
from sklearn.metrics.pairwise import cosine_similarity
from operator import itemgetter

class ArtistEvaluator:
    def __init__(self):
        self.artist_feats = pd.read_csv('MyData/artist_features.csv')
        self.sp = self._set_sp_creds()
        self.scaler = joblib.load('MyData/artist_feature_scaler.save')

    def _set_sp_creds(self):
        CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID')
        CLIENT_SECRET = os.environ.get('SPOTIFY_SECRET_ID')
        client_credentials_manager = SpotifyClientCredentials(CLIENT_ID, CLIENT_SECRET)
        sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)
        return sp

    def _get_artist_id(self, artist_name):
        try:
            results = self.sp.search(q='artist:' + artist_name, type='artist')
            items = results['artists']['items']
            artist_id = items[0]['id']
            artist_name = items[0]['name']

        except:
            print('Artist not found')
        return artist_id, artist_name



    def _get_top_tracks(self, artist_id):
        """
        Retrieve features for an artists top 10 tracks
        """

        top = self.sp.artist_top_tracks(artist_id, country='US')['tracks']
        top_tracks = []
        for track in top:
            top_tracks.append(track['id'])

        return top_tracks

    def _create_feature_df(self, features):
        """
        Helper for _get_song_features
        """
        df_temp = pd.DataFrame.from_dict(features, orient = 'index')[:11]
        df_temp = df_temp.unstack().to_frame().T[0]
        return df_temp

    def _get_song_features(self, songs):
        features = ["danceability", "energy", "key", "loudness", "mode", "speechiness",
                                 "instrumentalness", "liveness", "valence", "tempo"]
        df = pd.DataFrame(columns = features)
        for song in songs:
            spot_feats = self.sp.audio_features(song)[0]
            df_temp = self._create_feature_df(spot_feats)
            df = df.append(df_temp)

        df.drop(columns = ['key','mode'], inplace=True)
        return df

    def get_artist_song_feats(self, artist_name):
        """
        Aggregates these top 10 songs for mean song artist features
        """

        artist_id, artist_name = self._get_artist_id(artist_name)
        top_tracks = self._get_top_tracks(artist_id)
        df = self._get_song_features(top_tracks)
        artist_vector = df.mean().values
        artist_vector = self.scaler.transform([artist_vector])

        return artist_vector, artist_name

    def find_similar_artists(self, artist_name, number_recos = 5):
        """
        Called at runtime by the user to retrieve their artist recommendations
        Combines all of the above functions
        """
        artist_vector, artist_name = self.get_artist_song_feats(artist_name)

        similarity_dic = {}
        for i in range(len(self.artist_feats)):
            score = cosine_similarity(artist_vector,[self.artist_feats.iloc[i,3:].values])
            similarity_dic[self.artist_feats['artist_name'][i]] = score

        top_vals = dict(sorted(similarity_dic.items(), key = itemgetter(1), reverse = True)[:number_recos])
        return top_vals, artist_name
