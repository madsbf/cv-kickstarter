PyCampus
========

Data Mining using Python project repository


# CNApi

The campusnet api is a python module for retrieving grades and user info about student at DTU.

## Usage

```python
app_name = 'MyCampusNetApp'
app_token = 'sh2870272-2ush292-ji2u98s2-2h2821-jsw9j2ihs982'
student_number = 's123456'

api = cnapi.CampusNetApi(app_name, app_token, student_number)

api.authenticate('secret-password')

# Fetch grades
grades = api.grades()

# Fetch user info
user = api.user()
```

## Credentials

In order to use the api token you need to register an app at CampusNet (https://www.campusnet.dtu.dk/data/Documentation/Index.aspx).
