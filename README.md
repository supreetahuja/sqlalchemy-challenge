# sqlalchemy-challenge

# Climate App Project

This project involves building a web application to analyze climate data using Flask, SQLAlchemy, and SQLite. The app provides various routes to query and display climate-related information from a provided SQLite database.

## Table of Contents
- [Project Overview](#project-overview)
- [Features](#features)
- [Getting Started](#getting-started)
- [API Endpoints](#api-endpoints)
- [Technologies Used](#technologies-used)
- [License](#license)

## Project Overview

The Climate App project involves creating a Flask web application to perform basic climate analysis and data exploration using SQLAlchemy ORM queries, Pandas, and Matplotlib. The project is structured into several routes that allow users to retrieve climate data, precipitation details, station information, temperature observations, and temperature statistics for specific date ranges.

## Features

- Retrieve precipitation data for the last 12 months.
- Get a list of available weather stations.
- Obtain temperature observations for the most active station in the last year.
- Calculate temperature statistics (TMIN, TAVG, TMAX) for specified date ranges.
- Web-based user interface for easy data retrieval.

# API Endpoints
## The app provides the following API endpoints:

/api/v1.0/precipitation: Returns precipitation data for the last 12 months.
/api/v1.0/stations: Returns a list of available weather stations.
/api/v1.0/tobs: Returns temperature observations for the most active station in the last year.
/api/v1.0/<start>: Returns temperature statistics for the specified start date.
/api/v1.0/<start>/<end>: Returns temperature statistics for the specified start and end dates.
