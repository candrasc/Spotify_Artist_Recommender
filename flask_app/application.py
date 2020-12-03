from flask import Flask, render_template, request
import pandas as pd
from helpers import   ArtistEvaluator
import os
from form_classes import SubmissionForm

application = Flask(__name__)

application.config['SECRET_KEY'] = os.environ.get('SPOTIFY_SECRET_ID')

@application.route('/', methods=['GET', 'POST'])
def register():
    form = SubmissionForm(request.form)
    return render_template('submit_form.html', form=form)



if __name__ == '__main__':
	application.run(debug=True, host= '0.0.0.0', port=8080)
