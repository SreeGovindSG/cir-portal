
Development Environment

Its super easy to set up our development environment
Collect Pre-requisites

Install python-pip, python-dev and virtualenvwrapper

sudo apt-get install python-pip python-dev memcached
sudo pip install virtualenvwrapper

Get the files

You can clone it directly from https://bitbucket.org/tonythomas01/doctorkanu

git clone git@bitbucket.org:tonythomas01/thinkfoss.git

Setup development environment

First, some initialization steps. Most of this only needs to be done one time. You will want to add the command to source /usr/local/bin/virtualenvwrapper.sh to your shell startup file (.bashrc or .zshrc) changing the path to virtualenvwrapper.sh depending on where it was installed by pip.

export WORKON_HOME=~/Envs
mkdir -p $WORKON_HOME
source /usr/local/bin/virtualenvwrapper.sh

Lets create a virtual environment for our project

mkvirtualenv thinkfoss
workon thinkfoss

Install requirements

All the requirements are mentioned in the file requirements.txt.

pip install -r requirements.txt

Setup database

Setup tables in the DB

python manage.py syncdb

Collect all the static files for fast serving

python manage.py collectstatic

Run server

python manage.py runserver

