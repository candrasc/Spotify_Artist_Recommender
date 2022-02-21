from flask import Flask, render_template, request
from utils.artist_recommender import ArtistRecommender
import os
import numpy as np

application = Flask(__name__)

application.config['SECRET_KEY'] = os.environ.get('SPOTIFY_SECRET_ID')


@application.route('/')
def open_form():
    return render_template('submit_form.html')

@application.route('/', methods=['GET', 'POST'])
def get_recos():
    ae = ArtistRecommender()
    artist_name, num_recos = get_info()
    #try:
    payload = ae.find_similar_artists(artist_name, num_recos)
    top_results = payload['top_results']
    artist_info = payload['og_artist_info']

    return render_template('results_grid.html', name = 'results',
                            recos=top_results, artist_name=artist_info['artist'], og_url=artist_info['url'])


def get_info():
    artist_name = request.form['artist_name']
    num_recos = request.form['num_recos'].replace(" ", "")
    if num_recos == "":
        num_recos = 5
    else:
        num_recos = int(num_recos)
    return artist_name, num_recos

if __name__ == '__main__':
	application.run(debug=True)
