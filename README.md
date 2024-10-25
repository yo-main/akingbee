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

The website is hosted in my RaspBerry.

The database (postgresql) is inside that cluster as well. It's dangerous (I already lost all my data [2] times), but it's cheaper, and I like to live dangerously (not to the point to not have any backup though).

I force myself to do things correctly. All services are well tested (except poseidon, but that might come one day). CI has been implemented with github actions. 

Logs are managed by the stack promtail/loki/grafana, but I'm not so sastified with the way I've done those things for now (logs could be parsed in a much better way).
