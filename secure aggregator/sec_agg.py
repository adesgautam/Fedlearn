from flask import Flask, request
import requests, json
import ast
from fl_agg import model_aggregation

app = Flask(__name__)

@app.route('/')
def hello():
	return "Secure Aggregator running !"
		
@app.route('/cmodel', methods=['POST'])
def getmodel():
	if request.method == 'POST':
		file = request.files['model'].read()
		fname = request.files['json'].read()
		# cli = request.files['id'].read()

		fname = ast.literal_eval(fname.decode("utf-8"))
		cli = fname['id']+'\n'
		fname = fname['fname']

		# with open('clients.txt', 'a+') as f:
		# 	f.write(cli)
		
		print(fname)
		wfile = open("client_models/"+fname, 'wb')
		wfile.write(file)
			
		return "Model received!"
	else:
		return "No file received!"

@app.route('/aggregate_models')
def perform_model_aggregation():
	model_aggregation()
	return 'Model aggregation done!\nGlobal model written to persistent storage.'

@app.route('/send_model_secagg')
def send_agg_to_mainserver():
	# clients = ''
	# with open('clients.txt', 'r') as f:
	# 	clients = f.read()
	# clients = clients.split('\n')
	
	# for c in clients:
	# 	if c != '':
	file = open("persistent_storage/agg_model.h5", 'rb')
	data = {'fname':'agg_model.h5', 'id':'sec_agg'}
	files = {
		'json': ('json_data', json.dumps(data), 'application/json'),
		'model': ('agg_model.h5', file, 'application/octet-stream')
	}
	
	print('aggmodel')
	req = requests.post(url='http://localhost:8000/secagg_model', files=files)
	print(req.status_code)
	
	# print(req.text)
	return "Aggregated model sent to main server!"




if __name__ == '__main__':
	app.run(host='localhost', port=8003, debug=False, use_reloader=True)















