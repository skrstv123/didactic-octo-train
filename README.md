# SRGAN API
this api currently will respond asynchronously to a superresolve request. it will send the result to user's email.

#### to begin development/running the API locally : 
1. Clone repo
2. create virtal env
```
cd didactic-octo-train
pip install virtualenv
virtualenv fypenv
.\fypenv\bin\activate.bat
```
3. install requirements
```
pip install -r fypreq.txt
```
4. create db
```
cd fyp2022
python manage.py migrate
```
5.  create superuser
```
python manage.py createsuperuser
```
6. start server
```
python manage.py runserver
```

#### processing a job:
```
python manage.py process_jobs
```

## Using the video converter
open the srgan notebook in Google colab and follow the instructions in notebook

to make the api also process videos, you can use method defined in notebook to create a command


#### API documentation 
[postman collection](https://www.getpostman.com/collections/6a76aa6ce916f0101fe3)

