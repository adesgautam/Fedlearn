# Fedlearn

An implementation to simulate a federated learning environment.

It is an attempt to mimic the scenario described in the paper [Towards Federated Learning at Scale: System Design](https://arxiv.org/pdf/1902.01046)

### Tech stack
* Python 3.6.1
* Keras
* Flask

### Update to previous version
Added a secure aggregator where the model aggregation will be done. The main server can't see the models from the devices. The secure aggregator is a trusted 3rd party where the model aggregation is done.

## Run the system using the steps below:
### Booting up
1. Run "Device 1" using `python app.py`
2. Run "Device 2" using `python app.py`
3. Run "Secure Aggregator" using `python sec_agg.py`
4. Run "Main Server" using `python main_server.py`

This will start the Flask servers of the two devices, secure aggregator and the main server.

Servers - 
* Main server - `http://localhost:8000/`
* Device1 - `http://localhost:8001/`
* Device2 - `http://localhost:8002/`
* Secure Aggregator - `http://localhost:8003/`

Everything will work using the REST APIs. 

### System working
1. First a model will be trained locally on the device.
On 'Device1' and 'Device2' server navigate to: `http://localhost:8001/modeltrain` and `http://localhost:8002/modeltrain` respectively.

The models will be trained on MNIST data.

2. Once the devices are ready send a status signal to the server that they are ready, using, `http://localhost:8001/sendstatus` and `http://localhost:8002/sendstatus`.

There will be a response from the main server.

3. Now, the trained models will be sent to the secure aggregator server using `http://localhost:8001/sendmodel` and `http://localhost:8002/sendmodel`

4. The secure aggregator will aggregate the model and build a global model. ` http://localhost:8003/aggregate_models`

5. The secure aggregator will send this aggregated model to the main server.
`http://localhost:8003/send_model_secagg`

6. The main server will send the aggregated model to the devices.
7. `http://localhost:8000/send_model_clients`

6. Goto step 1. The whole process is repeated again and the aggregated global model is improved at every round.

I tested this on the MNIST data and after 2 rounds got an accuracy of about `95%`. The model will eventually update when more devices will be used. The models on devices are being trained on all the train data and also because of this the accuracy is consistent, if the data is partitioned among the devices it would reveal the real performance.

#### If you would like to improve the current system please feel free to experiment and submit a PR.

## Future improvements
* Better model aggregation methods.
* Main server to send parameter configuration to devices based upon their performance.
* A better dataset to simulate the real world usage.
* Android app for simulating devices.
* Main server migration to Heroku or AWS.



