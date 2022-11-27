# portfolio

Online web software for deploying a directory of service professionals.

1. [Functionality](#functionality)
2. [Design](#design)
4. [Roadmap](#roadmap)
3. [Setting up](#setting-up)
4. [Roadmap](#roadmap)


## Functionality

High level view of different roles and their possible actions:
<br>

**Developer: Admin of the directory (Eg: EmptyCup)**

As a developer, to deploy **Portfolio** for a particular service you need to:

1. Define a portfolio (Eg: Interior designer)
2. Define a service (Eg: House design project)

Once deployed, users can sign up and use the below functionality.
<br>

**User: Service professional (Eg: Interior Designer)**

- Add portfolio (Profile, Stats, Gallery, Testimonials, Ratings)
- Configure service (ETA, Pricing, Deliverables)
- List portfolio in directory
- Showcase portfolio
- View tenders floated by Customers (see below).
- Submit proposal for tenders.

<br>

**User: Customer (Eg: Home owner)**

- Browse directory
- Float a tender
- Connect with provider


## Design

The system has 4 independently deployed components:

1. Static web frontend - Offers UI functionality by fetching data from the backend REST API
2. Backend REST API - Maintains a DB and runs a JSON REST API
3. CLI Tool - Single command line tool for admins to manage the deployment
4. Static web documentation - Documentation for the entire system.

## Roadmap

All the planned functionality will be broken down into smaller minor releases starting [v0.1](https://github.com/EmptyCupHQ/portfolio/milestone/1).


## Setting up

- [npm](https://docs.npmjs.com/downloading-and-installing-node-js-and-npm) needs to be installed before getting started.
- [pip]() needs to be installed before getting started.

1. Fork & clone the [repository](https://github.com/EmptyCupHQ/portfolio)
2. Install [virtualenv](https://emptycuphq.github.io/notes/python/virtualenv.md)
3. Install [python dependencies](https://emptycuphq.github.io/notes/python/pip.md)
4. Install [node dependencies](https://emptycuphq.github.io/notes/basics/npm.md)
