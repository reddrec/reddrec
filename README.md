# Reddrec

Reddrec is a web app that provides subreddit recommendations.

## Initial setup

Reddrec is super simple to build and run. A little initial setup makes things ez-pz.

First let's get the following: [Docker](https://www.docker.com/get-started), [Nodejs](https://nodejs.org/en/), [a Reddit account](https://www.reddit.com/)

Next we'll create a new Reddit developer app (it's free): [reddit.com/prefs/apps](https://www.reddit.com/prefs/apps/)

Finally we need to add our Reddit secrets to our environment. We recommend having these at login in your `.bash_profile` (or similar):

```bash
# reddrec .. Environment for main app stuff
export reddrec_praw_client_id='app-client-id-replace-me'
export reddrec_praw_client_secret='app-client-s3cr3t-replace-me'
export reddrec_praw_username='app-username-replace-me'
export reddrec_praw_password='app-p4ssw0rd-replace-me'
export reddrec_praw_user_agent='github.com/reddrec (crawler)'

# reddrec .. Environment for integration tests
export prawtest_client_id='test-client-id-replace-me'
export prawtest_client_secret='test-client-s3cr3t-replace-me'
export prawtest_username='test-username-replace-me'
export prawtest_password='test-p4ssw0rd-replace-me'
export prawtest_user_agent='github.com/reddrec (integration test)'
```
[see: praw docs](https://praw.readthedocs.io/en/latest/package_info/contributing.html?highlight=testing#adding-and-updating-integration-tests)

## Building

```
# Build React frontend
pushd webpage
npm install
npm run build
popd

# Everything else
docker-compose build
```

Building takes a few minutes.

_n.b.: Run `npm run build` in the `webpage` directory whenever you need to update the webpage. Technically you can use `npm start` but it will not connect with Flask and things will be broken. We'd like to get rid of this step in the future (and have auto-update behavior) since this extra step is annoying. Ideally we should move all Nodejs stuff into Docker._

## Running

```
docker-compose up reddrec
```

Development mode server will be live at [localhost:5000](http://localhost:5000).

## Testing

Run all tests with:

```
docker-compose run test
```

You can also launch a Redis client (while the app is running) for debug purposes:

```
docker-compose run rcli
```