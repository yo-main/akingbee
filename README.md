 ![akingbee](https://github.com/yo-main/akingbee/actions/workflows/akingbee.yaml/badge.svg)  

# akingbee.com

A website for beekeepers !

This website aims to help beekeepers to manage their hives and record everything, planify things and so on.

Even though I do not maintain a friendly relationship with bees, I understand and acknowledge their importance in this world. This website is my way of helping them while reducing the probability of me getting stingged.

The website is run using `go` on the backend and `htmx` on the frontend.

## Requirements

You need to have installed:

- [go](https://go.dev/dl/)
- [docker](https://docs.docker.com/get-started/get-docker/)
- [sqlite](https://www.sqlite.org/download.html)

## Running locally

Run the service on localhost:8080 with

```bash
go mod download
go run .
```

## Infrastructure

I don't expect a high traffic load.
The website is hosted in my RaspBerry and the database is managed through sqlite.


## Front tools

### emojis

They have been downloaded from:

- https://ionic.io/ionicons
- https://www.svgrepo.com/vectors

### Framework

The front is built using htmx, and css styling is done through bulma css

## CI

Lints & tests (lol) are run on the `master` branch.
Docker images are built when publishing a new release (manual process atm)
