# Time Series Forecasting for local bussiness

A web based application for local bussiness to record every day sales and predict upcoming demands for different products

### Built With
  ![flask2](https://github.com/SohelSlicing/TSA-for-local-businesses/assets/111112815/be2d3f2c-54b3-4319-9dd2-b5748ce45c04)
  ![sqlite](https://github.com/SohelSlicing/TSA-for-local-businesses/assets/111112815/294ca470-746d-46da-9900-af6d0039027f)
  ![python](https://github.com/SohelSlicing/TSA-for-local-businesses/assets/111112815/25f44332-8846-4cc2-8391-dc97d6b743c9)



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