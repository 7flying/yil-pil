from app import app

@app.route('/')
def root():
    """ Return the app index. """
    return app.send_static_file('index.html')
