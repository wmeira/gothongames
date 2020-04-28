from gothonweb import app
from sys import argv

if __name__ == "__main__":
    if len(argv) >= 2 and argv[1] == 'dev':
        app.run(debug=True)
    else:
        app.run()
