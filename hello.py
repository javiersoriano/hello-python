import os
import redis
import uuid
from flask import Flask
app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#AA99FF"
GREEN = "#33CC33"
counter = 0
POOL = redis.ConnectionPool(host='pub-redis-17697.us-east-1-2.3.ec2.garantiadata.com', port=17697, db=0)

COLOR = BLUE

def getVariable(variable_name):
    my_server = redis.Redis(connection_pool=POOL)
    response = my_server.get(variable_name)
    return response

def setVariable(variable_name, variable_value):
    my_server = redis.Redis(connection_pool=POOL)
    my_server.set(variable_name, variable_value)

@app.route('/')
def hello():
	global counter
	counterVar = getVariable(counter)
	counterVar += 1 
	setVariable(counter,counterVar)
	return """
	<html>
	<body bgcolor="{}">

	<center><h1><font color="white">Hi, I'm GUID:<br/>
	{}<br/>
	{}
	</center>

	</body>
	</html>
	""".format(COLOR,my_uuid,counter)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
