GIF2HTML5 App
=============

![Build Status](https://magnum.travis-ci.com/fusioneng/gif2html5-app.svg?token=qjLxqTcR19p9TfqYJxuN&branch=master)

GIF2HTML5 is a free and open source Python application to convert GIFs to MP4 videos and image keyframes. These files are automatically pushed to S3, and then reported to the CMS.

GIF isn't intended as a looping video format, but most of the web uses it as such. Serving GIFs transparently as HTML5 video significantly improves page performance while achieving the same comical effect of the GIF.

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
REDISTOGO_URL=
BUCKET=
FOLDER=
```

If you want to secure the conversion endpoint with a secret key. Add a `GIF2HTML5_API_KEY` setting:

```
GIF2HTML5_API_KEY=
```

If you specify an API key, then all POST requests will need to include an `api_key` field with the same value.

You will need Redis for queue system. To install Redis please run
```
brew install redis
```

and to start redis please run
```
redis-server /usr/local/etc/redis.conf
```

## Running Gif2HTML5
To run Gif2HTML5 locally:

```shell
make run
```

## How to use
Right now, we make it as simple as possible, once you deploy the app you can just do
```shell
curl -H "Content-Type: application/json" -d '{"url":"http://media.giphy.com/media/WSqcqvTxgwfYs/giphy.gif", "api_key" : "$YOUR_API_KEY" }' http://localhost:5000/convert
```

The gif will be downloaded, processed and uploaded to Amazon S3

## Webhook
If you want to convert the video asynchronously you can provide webhook in the JSON. The application will return right away and webhook will be called once the video is ready.

```shell
curl -H "Content-Type: application/json" -d '{"url":"http://media.giphy.com/media/WSqcqvTxgwfYs/giphy.gif", "webhook":"http://google.com", "api_key" : "$YOUR_API_KEY"}' http://localhost:5000/convert

```

## Testing
To run test:

```shell
make test
```

## How to deploy to Heroku
1. Please download and install. [Heroku Toolbelt](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)
2. Run `heroku login` to login
3. Run `heroku create` to create a box
4. Then push the code to heroku by doing `git push heroku master`
5. Add AWS key by running `heroku config:set AWS_ACCESS_KEY_ID=YOUR_KEY` and `heroku config:set AWS_SECRET_ACCESS_KEY=YOUR_ACCESS` and `heroku config:set BUCKET=YOURBUCKET` and `heroku config:set FOLDER=YOURFOLDER`
6. Add API_KEY by running `heroku config:set GIF2HTML5_API_KEY=YOURGIF2HTML5_API_KEY`
7. You're going to need Redis Addon by running `heroku addons:create redistogo`
8. You're going to need at least one worker and one web by running `heroku ps:scale web=1 worker=1`
