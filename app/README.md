# Reddrec Application

This is the root of the Reddrec web application.

Requirements: [Docker](https://www.docker.com/get-started), [Nodejs](https://nodejs.org/en/)

## Building:

```
pushd webpage; npm run build; popd; # Build React frontend
docker-compose build # Everything else
```

Note that you should run `npm run build` in the `webpage/` directory every time that you want to update the React build served by Flask. Could be Dockerized in future.

## Running:

```
docker-compose up reddrec
```

Development mode server will be live at [localhost:5000](http://localhost:5000).

## Testing:

```
docker-compose run test
```
