# Time Series Forecasting for local bussiness

A web based application for local bussiness to record every day sales and predict upcoming demands for different products

### Built With



### How to run the Project
* Pull the repo into your local machine
* Create a python virtual enviroment
    * for Windows
'''
    cd TSA-for-local-businesses
    py -m venv env
    .\env\Scripts\activate
'''
    * for unix/macOS
'''
    py -m venv env
    .\env\Scripts\activate
'''
* Install all dependencies
'''
pip install -r requirements.txt
'''
* Initialise the database
'''
python src.database.model.py
''' 
* Launch the flask app
'''
python app.py
'''
* Launch the local host http://127.0.0.1:5000/