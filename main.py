# Copyright 2018 Google LLC
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import datetime

from flask import Flask, render_template
from google.cloud import ndb

from TimeStore import TimeStore


def ndb_wsgi_middleware(wsgi_app):
    def middleware(environ, start_response):
        client = ndb.Client()
        with client.context():
            return wsgi_app(environ, start_response)

    return middleware

app = Flask(__name__)
app.wsgi_app = ndb_wsgi_middleware(wsgi_app=app.wsgi_app)


def store_time(dt):
    entity = TimeStore(timestamp=dt)
    entity.put()


def fetch_times(limit):
    times = TimeStore.query().fetch(limit=limit)
    return times


@app.route("/")
def root():
    # Verify Firebase auth.
    store_time(datetime.datetime.now())
    times = fetch_times(10)

    return render_template(
        "index.html", times=times
    )

if __name__ == "__main__":
    # This is used when running locally only. When deploying to Google App
    # Engine, a webserver process such as Gunicorn will serve the app. This
    # can be configured by adding an `entrypoint` to app.yaml.

    # Flask's development server will automatically serve static files in
    # the "static" directory. See:
    # http://flask.pocoo.org/docs/1.0/quickstart/#static-files. Once deployed,
    # App Engine itself will serve those files as configured in app.yaml.
    app.run(host="127.0.0.1", port=8080, debug=True)
