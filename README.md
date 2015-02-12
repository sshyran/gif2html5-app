# Gif -> HTML5

Gif2HTML5 is a free and open-source to convert gif to mp4 so it can be embedded in a website. HTML5 video will reduce the bandwidth used to load the page. As mp4 is significantly smaller than Gif

## Architecture
Gif2HTML5 is python application built on Flask. Currently, it deploys to Heroku but it can be deployed on any platforms as needed.

## Configuration
To run locally, make sure you have the [pip][pip] installed, the package managers for Python. Then do:

```shell
# install the requirements
pip install --requirement requirements.txt
```

You'll need a number of environment variables present. Please put these in `.env`, using this as a template:

```
# AWS credentials
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
```

## Running Gif2HTML5
To run Glance locally:

```shell
make run
```

## Testing
To run test:

```shell
make test
```
