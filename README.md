# Reddrec Application

This is the root of the Reddrec web application.

Requirements: [Docker](https://www.docker.com/get-started), [Nodejs](https://nodejs.org/en/)

## Building:

```
# Build React frontend
pushd webpage
npm install
npm run build
popd

# Everything else
docker-compose build
```

Note that you should run `npm run build` in the `webpage/` directory every time that you want to update the React build served by Flask. Could be Dockerized in future.

## Running:

```
docker-compose up reddrec
```

Development mode server will be live at [localhost:5000](http://localhost:5000).

## Testing:

Initial setup requires some environment variables ([source: praw docs](https://praw.readthedocs.io/en/latest/package_info/contributing.html?highlight=testing#adding-and-updating-integration-tests)):

```bash
export prawtest_client_id=myclientid
export prawtest_client_secret=myclientsecret
export prawtest_password=mypassword
export prawtest_test_subreddit=reddit_api_test
export prawtest_username=myusername
export prawtest_user_agent='reddrec-bot (integration test)'

# Optional (use in place of username & password):
# export prawtest_refresh_token=myrefreshtoken
```

We now test with:

```
docker-compose run test
```
