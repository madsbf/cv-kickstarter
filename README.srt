PyCampus
========

Data Mining using Python project repository


# CNApi

This library is designed for having a nice interface for integrating with
the CampusNet API. The library provides an interface for the network requests
as well as objects for wrapping the data returned by the CampusNet API.

For documentation of the Campusnet API, see:

https://www.campusnet.dtu.dk/data/Documentation/CampusNet%20public%20API.pdf

Example of usage:

At first instantiate the api:

    >>> app_name = 'MyCampusNetApp'
    >>> app_token = 'sh2870272-2ush292-ji2u98s2-2h2821-jsw9j2ihs982'

    >>> api = cnapi.CampusNetApi(app_name, app_token)

In order to fetch information, authenticate the student with the student number
and password:

    >>> api.authenticate('s123456', 'secret-password')

or if the auth token is already in posession use:

    >>> api.authenticate_with_token('s123456', '21EF8196-ED05-4BAB-9081')

To fetch the grades of the given user:

    >>> grades = api.grades()

To fetch the user infor of the given user:

    >>> user = api.user()
