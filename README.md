# didactic-octo-train

## under development
#### to begin development : 
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

#### endpoints
[postman collection](https://www.getpostman.com/collections/6607fe981be201a45789)
