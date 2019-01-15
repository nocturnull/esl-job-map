# ESL Job Map Website
ESL Job Map is a job seeking website where recruiters post jobs for teachers to apply to. 

## Getting Started
The following instructions will point you in the right direction and help you get started with installing the website.

### Prerequisites
* Python 3.4 >=
* pip
* virtualenv
* Redis
* PostgreSQL 10 >=
* Node.js

#### Linux
```bash
sudo apt-get update
sudo apt-get install python3.6
sudo apt-get install python3-pip
sudo pip3 install virtualenv
sudo apt install redis
sudo systemctl enable redis-server
sudo apt-get install postgresql postgresql-contrib
sudo -i -u postgres
creatuser --interactive
createdb esljobmap
```

#### Mac OS X
* Install [Python 3](https://www.python.org/downloads/mac-osx/)
* Install [Node.js](https://nodejs.org/en/download/)
* Install PostgreSQL
```bash
brew doctor
brew update
brew install postgresql
brew services start postgresql
createdb esljobmap
psql esljobmap
```

Once logged into PostgreSQL, set the password for your account.
```postgresql
\password YOUR_USERNAME
```

* Install Redis
```bash
brew install redis
brew services start redis
redis-cli ping
redis-server
```
* Install Foundation
```bash
npm install --global foundation-cli
```

### Environment Variables
Add the following environment variables to your .bashrc or .bash_profile file
```bash
export ESLJOBMAP_DEBUG=True
export ESLJOBMAP_DB_NAME=esljobmap
export ESLJOBMAP_DB_USER=username
export ESLJOBMAP_DB_PASSWORD=secretpassword
export ESLJOBMAP_DB_HOST="127.0.0.1"
export ESLJOBMAP_DB_PORT=5432
export ESLJOBMAP_REDIS_HOST=redis://127.0.0.1:6379/
export MAILGUN_DOMAIN=mail.yourdomain.com
export MAILGUN_PRIVATE_API_KEY=secretkey
export AWS_ACCESS_KEY_ID=accesskey
export AWS_SECRET_ACCESS_KEY=secretkey
export AWS_DEFAULT_REGION=region
export AWS_S3_BUCKET=bucket
export AWS_S3_PARENT_DIR=staging
```

### Installing
Clone the repo
```bash
mkdir ~/WebApps; cd ~/WebApps
git clone https://YOUR_USERNAME@bitbucket.org/esl-job-map/esl-job-map.git
```

Install back end dependencies in a virtual environment.
```bash
cd ~/WebApps/esl-job-map
virtualenv p36venv
virtualenv --relocatable p36venv
. p36venv/bin/activate
pip install -r requirements.txt
```

Install the front end dependencies with npm.
```bash
cd ~/WebApps/esl-job-map/esljobmap/static/foundation
npm install
```

Run the migrations
```bash
cd ~/WebApps/esl-job-map/esljobmap
python manage.py migrate 
```

Install Fixtures
```bash
python manage.py loaddata countries.json
python manage.py loaddata visa_types.json
```

Start the local web server to ensure everything works.
```bash
python manage.py runserver
```

## Building Assets
```bash
cd ~/WebApps/esl-job-map/esljobmap/static/foundation
foundation watch
```

## Coding Style Guide
Please follow the [PEP 8 Style Guide](https://www.python.org/dev/peps/pep-0008/)

## Running Tests
### Database
To clear the database for quick testing run the following query.
```postgresql
SELECT 'drop table if exists "' || tablename || '"cascade;' as pg_drop FROM pg_tables WHERE schemaname='public';
```

## Deployment
TODO

## Built With
* [Django 2](https://www.djangoproject.com/) - The web framework
* [Foundation 6](https://foundation.zurb.com) - The front end framework
* [PostgreSQL](https://www.postgresql.org/) - The relational database

## Authors
* Steven Wilson - CEO
* Marcos Daniel Arroyo - Software Developer and Architect

## License
Copyright (C) ESL Job Map - All Rights Reserved Unauthorized copying of this file, via any medium is strictly prohibited Proprietary and confidential