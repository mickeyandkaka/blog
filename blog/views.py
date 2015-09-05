# -*- coding: utf-8 -*-

from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
@app.route("/index")
def hello():
    user = {'nickname': 'mickey'}
    posts = [  # fake array of posts
            {
                'author': {'nickname': 'John'},
                'body': 'Beautiful day in Portland!'
            },
            {
                'author': {'nickname': 'Susan'},
                'body': 'The Avengers movie was so cool!'
            }
        ]
    return render_template('index.html',
                           title='home',
                           user=user,
                           posts=posts
            )
