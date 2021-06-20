# Spotify_Artist_Recommender
--- 
#### Check out the application here: http://spotifyartistrecommender-v2.eba-mnhqin2v.us-east-2.elasticbeanstalk.com/
---
## Summary

In this project, I use the Spotipy library to access Spotify's developer web endpoints to collect songs and their features. I have gathered both my streaming history as well as 5000 songs from a large Spotify playlist (https://spotipy.readthedocs.io/en/2.16.0/)

I then take all of the artists (1700+) in these playlists and retrieve their top 10 songs. I also retrieve the features for each song and aggregate them by artist to find each artists' mean song features.

Each artists' features are normalized with sklearn StandardScaler and stored in a csv. The scaler is also pickled and stored for use in the application. In the future, i will set up a database rather than just having a quick and dirty csv to store my data.

When accessing the front end of the application, you can input any Spotify artist, their features for their top songs will be retrieved, aggregated, and normalized. The requested artist will then be compared to every artist in the 1700+ artist data set I have created to find the most similar and provide you recommendations based on cosine similarity between artist vectors. You can then click on the recommended artists to be directed to their spotify page. 

The application backend is built with Flask and is hosted on AWS Elastic Beastalk.

## Results of Recommender:
The recommendations are not perfect, but they are definitely better than random! You will notice that high level attributes such as genre are picked up on fairly well even though they are not explicitly given as features. 

Of course, if I had access to other users's data and streaming history, I could build a much more comprehensive recommender, but I hope you enjoy what I have created for now :) 

-----------
## More

The scope and direction of this project changed a few times, so not all of the notebooks are directly related to the Song Recommender. If you want to see some visualization and exploratory analysis such as clustering, check out the Spotify Data Exploration File. 

#### However, everything related to the main project can be found in the flask_app directory


### Bonus Notebook: Spotify Data Exploration

#### Feature Selection and Engineering
Here I start to dig into the songs and their features. At the bottom of this readme, and at the start of this notebook you can find the provided features and their descriptions.

The first important step I take is to define what songs I actually 'like'. I needed a broad criteria that I could apply to all of my songs as I don't want to manually rate all of my songs.

All of the information I had for my streaming history was the length of time I played the song for each time that I played it. I then created my own features called "Skip", "Play", and "Like" so that I could better assess my sentiment towards a given song.

"Skip" was defined as playing the song for less than a minute, while "Play" was defined as letting play for more than a minute. I then defined a "Like" as any song that had a 75% play rate.

This feature engineering was a product of my first idea to create a recommender just for myself.

#### Clustering
The next step to take was to learn more about my data and song choice through clustering. (I have chosen KMeans to start, but it did not yield exceptional results in terms of the Elbow method or Silhouette score, so I will likely try another method soon).

The result was basically that only one of the clusters was significantly different than the others with a Silhouette score of 0.65, while the other clusters were scoring less than 0.3 for the most part.

The signficant cluster had high dancebility, high energy, and very low instrumentality. It also had a mean likes of 0.4 (not great). These songs are likely electronic dance music.

![](readme_images/s_score.png.PNG)


### Feature Descriptions:
acousticness — how acoustic

danceability — self-explanatory

energy — how 'fast, loud and noisy'

instrumentalness — the less vocals, the higher

liveness — whether there is audience in the recording

loudness — self-explanatory

speechiness — the more spoken words, the higher

valence — whether the track sounds happy or sad

tempo — the bpm
