 ![Aristaeus](https://github.com/yo-main/akingbee/actions/workflows/aristaeus.yaml/badge.svg)  ![Cerbes](https://github.com/yo-main/akingbee/actions/workflows/cerbes.yaml/badge.svg)  ![Hermes](https://github.com/yo-main/akingbee/actions/workflows/hermes.yaml/badge.svg)  ![Poseidon](https://github.com/yo-main/akingbee/actions/workflows/poseidon.yaml/badge.svg)  ![Gaea](https://github.com/yo-main/akingbee/actions/workflows/gaea.yaml/badge.svg)

# akingbee.com
A website for beekeepers !

This website aims to help beekeepers to manage their hives and record everything which has happened, planify things and so on.
It's mostly a pet project that I started a few years ago and on which I kept working on through the years, and still continue to this day.

## Micro services

Today the project is composed of several services.

### Aristaeus 

Aristaeus is the Greek god that discovered bee-keeping. 
It only makes sense that the service is in charge of managing hives & apiaries is named after this god.

The service itself is composed of a web api and of a rabbitmq listener.


### Cerbes 

Who's better than cerberus himself to protect the realm of bees ?

Cerbes will manages users & authentication through jwt. It's not keeping the gates of hell, but it does guard the entrance of something.
It's reason enough for me to name it this way.

### Hermes 

Hermes is the messager of the gods ! I couldn't name otherwise a service that sends emails !

### Poseidon  

Poseidon, god of the seas and oceans. There's no better gods than him for spreading my website through the immensity of what is the world wide web.

It's basically a react app. If you wanna dive in this service's code, keep in mind that you might find things that will hurt you, deeply (some things are better kept hidden in the deep darkness of the oceans).

### Gaea  

Gaea, she's the mother of all gods. And everyone needs a mother to rely on (even Gods). So I named my "chassis" after her, since this library will be used by all the other services.

## Infrastructure

The whole stack is running in a kubernetes cluster in digital ocean.
The database (postgresql) is inside that cluster as well. It's dangerous (I already lost all my data [2] times), but it's cheaper, and I like to live dangerously (not to the point to not have any backup though).

I force myself to do things correctly. All services are well tested (except poseidon, but that might come one day). CI has been implemented with github actions. 
