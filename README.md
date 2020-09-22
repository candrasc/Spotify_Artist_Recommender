# Spotify_Song_Clustering_&_Recommendation

In this project, I use the Spotipy API to collect songs and their features. I have gathered both my streaming history as well as 5000 songs from a large Spotify playlist.

I have used the Spotipy API (https://spotipy.readthedocs.io/en/2.16.0/) to collect data on my streaming history as well as a collection of random songs.

At this phase in the project, I have only done some initial exploration and clustering of my personal streaming history to find out more about what I like. In the future, I am going to build a recommender so that I can recommend songs to myself from the 5000 song library.

-----------

## File 1: Spotify Song Collection

In this document, I outline how you can get access to your songs and others with the Spotipy API. The data comes in a json file format, so there is some work required to get it into a nice and pretty dataframe.

When you initially request your personal data from Spotify, the features of the songs are not actually included. We need to use the API, as I have outlined here, to retrieve this information and put it into one dataframe.

Useful resources for using the API that I would have been lost without are linked directly in the notebook.

## File 2: Spotify Data Exploration

### Feature Selection and Engineering
Here I start to dig into the songs and their features. At the bottom of this readme, and at the start of this file you can find the provided features and their discriptions.

The first important step I take is to define what songs I actually 'like'. I needed a broad criteria that I could apply to all of my songs as I don't want to manually rate all of my songs.

All of the information I had for my streaming history was the length of time I played the song each time I played it. I then created my own features called "Skip", "Play", and "Like" so that I could better assess my sentiment towards a given song.

"Skip" was defined as playing the song for less than a minute, while "Play" was defined as letting play for more than a minute. I then defined a "Like" as any song that had a 75% play rate.

### Clustering
The next step to take was to learn more about my data and song choice through clustering. (I have chosen KMeans to start, but it did not yield exceptional results in terms of the Elbow method or Silhouette score, so I will likely try another method soon).

The result was basically that only one of the clusters was significantly different than the others with a Silhouette score of 0.65, while the other clusters were scoring less than 0.3 for the most part.

The signficant cluster had high dancebility, high energy, and very low instrumentality. It also had a mean likes of 0.4 (not great). These songs are likely electronic dance music.

![](Images/s_score.png.PNG)

### Next steps:

1) Analyze my 5000 song playlist and see if similar clusters emerge.

2) Train a model on my streaming history and then apply it to the large playlist to predict if I will like certain songs.
     - Will potentially have to train multiple models for different genres (one for the Electronic Dance music, another for all others)

3) Create a recommender, where you can enter a song, and based on similarity of features, a song will be suggested for you.


### Feature Descriptions:
acousticness — how acoustic

danceability — self-explanatory

energy — how 'fast, loud an noisy'

instrumentalness — the less vocals, the higher

liveness — whether there is audience in the recording

loudness — self-explanatory

speechiness — the more spoken words, the higher

valence — whether the track sounds happy or sad

tempo — the bpm
