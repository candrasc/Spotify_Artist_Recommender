"""

We can use 'external_urls': {'spotify': 'https://open.spotify.com/artist/17mBFWKyCyp506a3n6XUWA'} to open an artist in the web player

https://stackoverflow.com/questions/29534725/how-to-dynamically-create-table-in-html-with-certain-constraints
for dynamic links
"""
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pandas as pd
from typing import List, Dict
import os


FEATURES = ["danceability", "energy", "key", "loudness", "mode", "speechiness", "acousticness",
            "instrumentalness", "liveness", "valence", "tempo"]

class FeatureFinder:


    def __init__(self, client_id, client_secret):
        self.sp = self.__create_spt_connection(client_id, client_secret)

    def __create_spt_connection(self, client_id, client_secret):
        token = spotipy.oauth2.SpotifyClientCredentials(client_id=client_id, client_secret=client_secret)
        cache_token = token.get_access_token()
        sp = spotipy.Spotify(cache_token)

        return sp

    # Authenticate to Spotify
    def authenticate(self, cliend_id: str, client_secret: str) -> spotipy.client.Spotify:
        sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=cliend_id,
                client_secret=client_secret
            )
        )

        return sp

    # Number of tracks available in the playlist
    def __get_pl_length(self, pl_uri: str) -> int:
        return self.sp.playlist_items(
            pl_uri,
            offset=0,
            fields="total"
        )["total"]


    def _get_artist_info(self, pl_tracks):
    # input is from sp_instance.playlist_tracks()
        feats = []
        for pl_item in pl_tracks["items"]:
            # Get dict in list
            try:
                feat_dic = pl_item["track"]["artists"][0]
                feat_dic['image_url'] = pl_item['track']['album']['images'][0]['url']
                feat_dic["preview_url"] = pl_item['track']['preview_url']
                feats.extend([feat_dic])
            except Exception as e:
                print(e)
        
        return feats

    # Get all the artist info about each track of the playlist.
    def get_tracks_artist_info(self, pl_uri: str) -> List[Dict]:
        artists_info = list()
        # Start retrieving tracks from the beginning of the playlist
        offset = 0
        pl_length = self.__get_pl_length(pl_uri)

        # Playlist track retrieval only fetches 100 tracks at a time, hence\
        # the loop to keep retrieving until we reach the end of the playlist
        while offset != pl_length:
            # Get the next batch of tracks
            pl_tracks = self.sp.playlist_tracks(
                pl_uri,
                offset=offset,
                fields="items.track"
            )

            # Get the list with the info about the artists of each track from the\
            # latest batch and append it to the running list
            feats = self._get_artist_info(pl_tracks)
            artists_info.extend(feats)

            # Update the offset
            offset += len(pl_tracks["items"])

        return artists_info


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

        df = pd.DataFrame(columns = FEATURES)
        for song in songs:
            spot_feats = self.sp.audio_features(song)[0]
            df_temp = self._create_feature_df(spot_feats)
            df = df.append(df_temp)
        # drop categorical features
        df.drop(columns=['mode', 'key'], inplace=True)
        return df

    def get_artist_song_feats(self, artist_id):
        """
        Aggregates these top 10 songs for mean song artist features
        """

        top_tracks = self._get_top_tracks(artist_id)
        df = self._get_song_features(top_tracks)
        artist_vector = df.mean().values

        return artist_vector

    def create_artist_df_no_features(self, pl_uri):

        artist_info = self.get_tracks_artist_info(pl_uri)
        
        
        df = pd.DataFrame(columns = ["artist", "artist_id", "url", "image_url", "preview_url"])
        for feats in artist_info:
            try:
                artist = feats["name"]
                art_id = feats["id"]
                url = feats["external_urls"]["spotify"]
                image_url = feats["image_url"]
                preview_url = feats["preview_url"]
                df.loc[len(df), :] = [artist, art_id, url, image_url, preview_url]
            except:
                print(feats["name"])
            
        df = df.drop_duplicates(subset=['artist_id']).reset_index(drop=True)
        
        return df

    def create_artist_df_with_features(self, playlist_uris: str):
        """

        Args:
            playlist_uris: playist ID

        Returns: df of all artists in the playlist and their aggregated features for their top 10 songs

        """

        artist_df_og = self.create_artist_df_no_features(playlist_uris)
        artist_ids = artist_df_og['artist_id']

        art_feats = []
        unknown_artists = []
        for i in artist_ids:
            try:
                feats = self.get_artist_song_feats(i)
                art_feats.append(feats)
            except:
                print(f'{i} cannot be found')
                unknown_artists.append(i)
        artist_df_og = artist_df_og.drop(artist_df_og[artist_df_og['artist_id'].isin(unknown_artists)].index)
                
        feat_df = pd.DataFrame(art_feats, columns = ["danceability", "energy", "loudness", "speechiness", "acousticness",
                     "instrumentalness", "liveness", "valence", "tempo"])

        assert len(artist_df_og) == len(feat_df)

        final_df = pd.concat([artist_df_og, feat_df], axis=1)
        final_df.dropna(inplace=True)
        final_df.reset_index(inplace=True, drop=True)

        return final_df