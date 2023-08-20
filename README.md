# Time Series Forecasting for local bussiness

A web based application for local bussiness to record every day sales and predict upcoming demands for different products


### Built With
  ![flask2](https://github.com/SohelSlicing/TSA-for-local-businesses/assets/111112815/be2d3f2c-54b3-4319-9dd2-b5748ce45c04)
  ![sqlite](https://github.com/SohelSlicing/TSA-for-local-businesses/assets/111112815/294ca470-746d-46da-9900-af6d0039027f)
  ![python](https://github.com/SohelSlicing/TSA-for-local-businesses/assets/111112815/25f44332-8846-4cc2-8391-dc97d6b743c9)


### How to run the Project
* Pull the repo into your local machine
* Create a python virtual enviroment
> for Windows
``` 
  cd TSA-for-local-businesses
  py -m venv env
  .\env\Scripts\activate
```
 > for unix/macOS
```
  py -m venv env
  .\env\Scripts\activate
```
* Install all dependencies
```
  pip install -r requirements.txt
```
* Initialise the database
```
  python src.database.model.py
``` 
* Launch the flask app
```
  python app.py
```
* Launch the local host http://127.0.0.1:5000/


### Screen caps from the project

* Login page
![Login](https://github.com/SohelSlicing/TSA-for-local-businesses/assets/111112815/3a04a3ab-c1f9-4c9d-b4ed-920a91cf0902)

* Add a Product
![Add product](https://github.com/SohelSlicing/TSA-for-local-businesses/assets/111112815/06d0ec94-c566-4676-8d29-cb5a20e30819)

* Transaction page <br>
![Add transaction](https://github.com/SohelSlicing/TSA-for-local-businesses/assets/111112815/c5bd6dfd-6e87-4f0f-81bf-cfe40209d52f)
