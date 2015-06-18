GIF2HTML5 App
=============

[![Build Status](https://travis-ci.org/fusioneng/gif2html5-app.svg?branch=master)](https://travis-ci.org/fusioneng/gif2html5-app)

GIF2HTML5 is a free and open source Python application to convert GIFs to MP4 videos and image keyframes. These files are automatically pushed to S3, and then reported to the CMS.

GIF isn't intended as a looping video format, but most of the web uses it as such. Serving GIFs transparently as HTML5 video significantly improves page performance while achieving the same comical effect of the GIF.

## Architecture

GIF2HTML5 is Python application built on Flask. We've deployed it to Heroku but you can deploy it to your platform of choice.

If you use WordPress, we've [released a companion plugin](https://github.com/fusioneng/gif2html5-plugin/issues) to make it easy to integrate GIF2HTML5 in your WordPress theme.

## Configuration

To run GIF2HTML5 locally, make sure you have the `pip` installed, the package manager for Python. Then do:

```shell
# Install the requirements
pip install --requirement requirements.txt
```

Python newbie? It's much easier to run Python applications inside of a virtual environment. With [virtualenvwrapper](https://virtualenvwrapper.readthedocs.org/en/latest/#introduction), it's as easy as `mkvirtualenv gif2html5` and `workon gif2html5`.

You'll need a number of environment variables present. Please put these in `.env`, using this as a template:

```
# AWS credentials
AWS_ACCESS_KEY_ID=
AWS_SECRET_ACCESS_KEY=
REDISTOGO_URL=
BUCKET=
FOLDER=
```

If you want to secure the conversion endpoint with a secret key, you can add a `GIF2HTML5_API_KEY` setting:

```
GIF2HTML5_API_KEY=
```

With this API key setting present, all POST requests will need to include an `api_key` field with the same value.

You will need Redis for queue system. To install Redis on Mac OS X with `brew`, run:

```
brew install redis
```

To start Redis, run:

```
redis-server /usr/local/etc/redis.conf
```

## Running

To run GIF2HTML5 locally:

```shell
make run
```

## Using

We've tried to make it as simple to use as possible, and encourage your constructive feedback. Once you've deployed the app, you can call it like this:

```shell
curl -H "Content-Type: application/json" -d '{"url":"http://media.giphy.com/media/WSqcqvTxgwfYs/giphy.gif", "api_key" : "$YOUR_API_KEY" }' http://localhost:5000/convert
```

The GIF will be downloaded, processed and uploaded to Amazon S3.

### Webhook

If you want to convert the GIF asynchronously you can provide webhook endpoint in the JSON. The application will return right away and webhook will be called once the GIF is converted and uploaded to S3.

```shell
curl -H "Content-Type: application/json" -d '{"url":"http://media.giphy.com/media/WSqcqvTxgwfYs/giphy.gif", "webhook":"http://google.com", "api_key" : "$YOUR_API_KEY"}' http://localhost:5000/convert

```

## Testing

To run tests:

```shell
make test
```

## Deploying to Heroku

1. Please download and install. [Heroku Toolbelt](https://devcenter.heroku.com/articles/getting-started-with-python#set-up)
2. Run `heroku login` to login
3. Run `heroku create` to create a box
4. Then push the code to heroku by doing `git push heroku master`
5. Add AWS key by running `heroku config:set AWS_ACCESS_KEY_ID=YOUR_KEY` and `heroku config:set AWS_SECRET_ACCESS_KEY=YOUR_ACCESS` and `heroku config:set BUCKET=YOURBUCKET` and `heroku config:set FOLDER=YOURFOLDER`
6. Add API_KEY by running `heroku config:set GIF2HTML5_API_KEY=YOURGIF2HTML5_API_KEY`
7. You're going to need Redis Addon by running `heroku addons:create redistogo`
8. You're going to need at least one worker and one web by running `heroku ps:scale web=1 worker=1`
