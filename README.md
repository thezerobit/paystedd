# PAYSTEDD

A single file pastebin implementation for Python 2.X using Bottle,
SQLAlchemy, and Pygments.

## Install

Ubuntu:

```
sudo apt-get install postgresql postgresql-server-dev-9.1

sudo -u postgres createuser -D -A -P paystedduser # paysteddpass
sudo -u postgres createdb -O paystedduser paystedd

# create and activate a virtualenv
pip install -r requirements.txt
python pastedd.py # to run test server at http://localhost:8080/
```

## Deployment

See Bottle's documentation on
[Deployment](http://bottlepy.org/docs/stable/deployment.html).

## Author

* Stephen A. Goss (steveth45@gmail.com)

## Copyright

Copyright (c) 2012 Stephen A. Goss (steveth45@gmail.com)

# License

Licensed under the Modified BSD License.

