FROM ubuntu:14.04
MAINTAINER Joseph Juzl "joejuzl@gmail.com"
RUN apt-get update
RUN apt-get install -y python3.4-dev python3-setuptools supervisor git-core python3-pip
RUN pip3 install virtualenv
RUN pip3 install uwsgi
RUN virtualenv --no-site-packages -p /usr/bin/python3.4 /opt/ve/friendmap
ADD . /opt/apps/friendmap
ADD ./supervisor.conf /opt/supervisor.conf
ADD ./run.sh /usr/local/bin/run
RUN /opt/ve/friendmap/bin/pip install -r /opt/apps/friendmap/requirements.txt
RUN (cd /opt/apps/friendmap && /opt/ve/friendmap/bin/python manage.py syncdb --noinput)
RUN (cd /opt/apps/friendmap && echo "from django.contrib.auth.models import User; User.objects.create_superuser('admin', 'myemail@example.com', 'changeme')" | /opt/ve/friendmap/bin/python manage.py shell)
RUN (cd /opt/apps/friendmap && /opt/ve/friendmap/bin/python manage.py collectstatic --noinput)
EXPOSE 8000
CMD ["/bin/sh", "-e", "/usr/local/bin/run"]