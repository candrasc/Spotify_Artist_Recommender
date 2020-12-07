from flask import Flask, render_template, request
import pandas as pd
from ArtistRecommender import ArtistEvaluator
import os
import numpy as np
from form_classes import SubmissionForm

application = Flask(__name__)

application.config['SECRET_KEY'] = os.environ.get('SPOTIFY_SECRET_ID')

@application.after_request
def add_header(response):
    """
    Clear cache to reset displayed values
    """
    response.headers['X-UA-Compatible'] = 'IE=Edge,chrome=1'
    response.headers['Cache-Control'] = 'public, max-age=0'
    return response

@application.route('/')
def open_form():
    return render_template('submit_form.html')

@application.route('/', methods=['GET', 'POST'])
def get_recos():
    ae = ArtistEvaluator()
    artist_name, num_recos = get_info()
    top_vals, artist_name = ae.find_similar_artists(artist_name, num_recos)
    top_vals = [(k, np.round(float(v),3)) for k, v in top_vals.items()]

    return render_template('results_good.html', name = 'results',
                            recos = top_vals, artist_name = artist_name)


def get_info():
    artist_name = request.form['artist_name']
    num_recos = int(request.form['num_recos'])
    return artist_name, num_recos

if __name__ == '__main__':
	application.run(debug=True, host= '0.0.0.0', port=8080)
