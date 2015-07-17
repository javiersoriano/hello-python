import os
import redis
import uuid
import json
from flask import Flask
app = Flask(__name__)
my_uuid = str(uuid.uuid1())
BLUE = "#AA99FF"
GREEN = "#33CC33"
rediscloud_service = json.loads(os.environ['VCAP_SERVICES'])['rediscloud'][0]
credentials = rediscloud_service['credentials']
POOL = redis.ConnectionPool(host=credentials['hostname'], port=credentials['port'], password=credentials['password'])

COLOR = BLUE

def getVariable(variable_name):
    my_server = redis.Redis(connection_pool=POOL)
    response = my_server.get(variable_name)
    return response

def setVariable(variable_name, variable_value):
    my_server = redis.Redis(connection_pool=POOL)
    my_server.set(variable_name, variable_value)

def incrVariable(variable_name):
    my_server = redis.Redis(connection_pool=POOL)
    my_server.incr(variable_name)

@app.route('/')
def hello():
	incrVariable('counter')
        counterVar = getVariable('counter')
	return """
	<html>
	<body bgcolor="{}">

	<center><h1><font color="white">Hi, I'm GUID:<br/>
	{}<br/>
	{}
	</center>

	</body>
	</html>
	""".format(COLOR,my_uuid,counterVar)


if __name__ == "__main__":
	app.run(host='0.0.0.0', port=int(os.getenv('VCAP_APP_PORT', '5000')))
