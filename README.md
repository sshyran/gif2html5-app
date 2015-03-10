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

You will need Redis for queue system. To install Redis please run
```
brew install redis
```

and to start redis please run
```
redis-server /usr/local/etc/redis.conf
```

## Running Gif2HTML5
To run Glance locally:

```shell
make run
```

## How to use
Right now, we make it as simple as possible, once you deploy the app you can just go
```shell
curl -H "Content-Type: application/json" -d '{"url":"http://media.giphy.com/media/WSqcqvTxgwfYs/giphy.gif", "webhook":"http://google.com" }' http://localhost:5000/convert
```

The gif will be downloaded, processed and uploaded to Amazon S3

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
4. Add AWS key by running `heroku config:set AWS_ACCESS_KEY_ID=YOUR_KEY` and `heroku config:set AWS_SECRET_ACCESS_KEY=YOUR_ACCESS`
