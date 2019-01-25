# glasfluegel.net

Welcome!

This is the source code of [https://www.glasfluegel.net], a website about the GLASFLÜGEL sailplane manufacturer from Germany, which was active from the 1960s to 1980s and a pioneer in composite technology aircraft production. Because this website and its community is mostly located in german-speaking countries, the rest of this README is in german, but you can ask any question if further assistance is needed.

This website is entirely established on (ViUR)[https://viur.is]. ViUR is a free software development framework written in Python and providing a powerful SDK to develop web-apps running on the Google App Engine platform.

## Build the Vi

To build the Vi, run

```bash
$ cd vi
$ make deploy
```

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

## License

This website and software is Copyright (C) 2016-2019 by Jan Max Meyer.

It is licensed under the GNU AFFERO GENERAL PUBLIC LICENSE.

## Contact

Contact @phorward for help and support.
