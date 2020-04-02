from flask import Flask

app = Flask(__name__)
app.secret_key = 'xzGkV2GUaG6wzJN4wFeFzseWDnY3GkjYdVibeH7CE3w'

from gothonweb import planisphere, routes