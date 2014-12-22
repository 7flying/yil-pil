from app import app
from app import manager

manager.populate_test2()
app.run(host='0.0.0.0', debug = True, port=5000)
