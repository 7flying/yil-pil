from app.yilpil import app as app
from app import manager
import os

manager.populate_test2()
PORT = int(os.environ.get('PORT', 33507))
app.run(host='0.0.0.0', debug=True, port=PORT)
