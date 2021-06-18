from flask import Flask, render_template, request
from utils.artist_recommender import ArtistRecommender
import os
import numpy as np

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
    ae = ArtistRecommender()
    artist_name, num_recos = get_info()
    #try:
    top_vals, artist_name, artist_url = ae.find_similar_artists(artist_name, num_recos)
    for key in top_vals.keys():
        if key == artist_name:
            top_vals, artist_name, _ = ae.find_similar_artists(artist_name, num_recos+1)
            top_vals.pop(key, None)

    top_vals_list = [(k, np.round(float(v['sim']), 3)) for k, v in top_vals.items()]
    links = [val['url'] for val in top_vals.values()]

    return render_template('results_good.html', name = 'results',
                            recos=top_vals_list, artist_name=artist_name, artist_link=artist_url,
                            links=links)

    # except:
    #     print(artist_name)
    #     return render_template('error_page.html', name = 'error')


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
