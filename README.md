# glasfluegel

Created by neo.

https://glasfluegel.appspot.com

## Description

This is glasfluegel-viur.

## Build the Vi

To build the Vi, run

```bash
$ cd vi
$ make deploy
```

## Install prerequisites

To install prerequisites, once do

```bash
$ pip2 install -t deploy/lib -r requirements.txt --upgrade
```

or on any prerequisite change/update.

## Run local development version

To locally run, do

```bash
$ ./local_run.sh
```

or manually, do

```bash
$ cd deploy
$ dev_appserver.py -A glasfluegel --log_level=debug .
```

## Deploy to GAE

Deployment is performed using the gcloud SDK:

```bash
$ cd deploy

# Deploy to dev
$ gcloud app deploy --no-promote -q --project=glasfluegel --version=$USER-dev

# Deploy to live (beware!)
$ gcloud app deploy -q --project=glasfluegel --version=`date +"%Y-%m-%d"-$USER`
```

## Contact

Contact @codepilot for help and support.
