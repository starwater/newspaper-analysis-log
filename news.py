#!/usr/bin/env python3
#
# A buggy web service in need of a database.

from flask import Flask, request, redirect, url_for

from newsdb import top_three, popular_author, bug_percentile

app = Flask(__name__)

# HTML template for the forum page
HTML_WRAP = '''\
<!DOCTYPE html>
<html>
  <head>
    <title>DB statistics</title>
    <style>
      h1, form { text-align: center; }
      textarea { width: 400px; height: 100px; }
      div.post { text-align:center;}
      div.t{text-align:center;}
    </style>
  </head>
  <body>
    <h1>Log statistics</h1>
    <!-- post content will go here -->
    <div class=t><strong>Top 3 articles</strong></div>
%s
<br>
    <div class=t><strong>Popular authors of all time</strong></div>
%s
<br>
    <div class=t><strong>Bugs</strong></div>
%s
<br>
  </body>
</html>
'''

# HTML template for an individual comment
TOP3 = '''\
    <div class=post>%s---%s votes</div>
'''

MOST_POP = '''\
    <div class=post>%s---%s views</div>
'''

BUGS = '''\
    <div class=post>%s---%s percentile errors</div>
'''


@app.route('/', methods=['GET'])
def main():
    # Main page of the forum.
    top3 = "".join(TOP3 % (title, num) for title, num in top_three())
    pop = "".join(MOST_POP % (name, total) for name, total in popular_author())
    bugs = "".join(BUGS % (date, bugs) for date, bugs in bug_percentile())
    html = HTML_WRAP % (top3, pop, bugs)
    return html


@app.route('/', methods=['POST'])
def post():
    # '''New post submission.'''
    message = request.form['content']
    add_post(message)
    return redirect(url_for('main'))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
