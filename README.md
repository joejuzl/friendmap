# Friendmap

## Installation:

### With Docker (easiest!):

Change directory to the location of the Dockerfile.

```
docker build -t friendmap .
docker run -d -p 8000:8000 friendmap
```
**Hit the IP of your docker at port 8000**

hint: run `boot2docker ip` for mac, localhost for linux

hint: admin password is "changeme"

### Without Docker:
#####need:
* python3
* pip3
* virtualenv

Run:

```
virtualenv -p /usr/local/Cellar/python3/3.4.3_2/bin/python3.4 fm
source fm/bin/activate
pip3 install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser
make sure to use the username admin
python manage.py runserver
```
**Hit localhost:8000 in your browser**


## Usage:

Please use Chrome!!!

Create some users by typing in username and password then clicking signup. Use the signin dropdown in the top left when already logged in.

Add friends by searching for their username and clicking on them.

Watch your friend graph grow.


Sign in as admin (password is changme for docker, or what you set it too) to see all the friendships.


##caveats:
This is by no means prod ready.
Some things that would be required:

* A proper database, e.g. postgres, running in a seperate container
* A proper http server, e.g. nginx, to server static files
* Testing for the javascript and end-to-end tests
* Logging
* Automated build process, e.g. paver
* Better error handling, custom exceptions.
