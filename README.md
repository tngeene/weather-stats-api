# Weather API

> Main repository for the weather statistcs API.

This app returns max, minimum, average and median temperature values of a
city's weather forecast. Data is provided from the open API
[weatherapi.com](https://www.weatherapi.com/)

This project has been hosted and is available [here](https://weather-api.tngeene.com/)

1. [Requirements](#requirements)
2. [Setup](#setup)
3. [Usage](#usage)
4. [Development](#development)

## Requirements

1. Python 3.9+ installed
2. Text editor such as [vs code](https://code.visualstudio.com/) or sublime text
3. Git - preferrably use terminal like [gitbash](https://gitforwindows.org/)
4. An account with the open API provider, [weatherapi.com](https://www.weatherapi.com/)

## Setup

1. Clone the repository.
2. Change directory to the location of this repository.
3. Create a `.env` file using the included `.env.example` as an example.
4. Populate the missing variables with the relevant values. The `WEATHER_API_KEY` is obtained on the weatherapi dashboard.
5. Generate a secret key for your app and paste into the SECRET_KEY section of the `.env` file
    you can find generate the key from [here](https://djecrety.ir/)
6. Create and start your preferred Python virtual environment. For
    more information on how to set up a virtual environment, check the instructions on [this link](https://tutorial.djangogirls.org/en/django_installation/). Install the required libraries by running the commands below, by changing to
    the project directory.

            pip install -r requirements.txt

7. After installation, run the following command:

        python manage.py migrate

8. A local `dbsqlite` file will be generate at the root of the project.
9. Run `python manage.py runserver`
10. For details of how to get started with django, check out [this link](https://www.djangoproject.com/start/)
11. In order to work with a virtual environment, check out [this link](https://tutorial.djangogirls.org/en/installation/#pythonanywhere)

In case you have docker installed, run

    docker compose up --build -d

> Give the entrypoint.sh read-write permissions by running `sudo chmod u+x ./entrypoint.sh` before running the above command.

Visit the base url, e.g `http://127.0.0.1:8000/api/locations/nairobi/?days=5`

### Run Development Server

To run locally:

    python manage.py runserver

### Usage

### Valid Request made

While on a browser window or any API testing platform, e.g postman, make a `GET` request to `/api/locations/{city_name}/?days={days_to_lookup}` . Where `city_name` is the name of the city to check weather data, and `days` are the number of days to look up.

A sample request would be, `/api/locations/rabat/?days=10`. While a sample response is;

    {
        "maximum": 20.7,
        "minimum": 12.5,
        "average": 16.1,
        "median": 16.1
    }

The response returns with a status code of `200`

### Non existent city name

If a non existent city name is provided, the response to expect is a `400` (bad request).

For example, `api/locations/hogwarts/?days=3`, returns

    {
        "error": {
            "code": 1006,
            "message": "No matching location found."
        }
    }

### Days Lookup validation and error handling

For the API to work, you need to provide the number of days to fetch data from the API.
This is set as a request url parameter.
In case it's not passed as a query parameter, expect a response `406` (not acceptable), with the following response message:

    {
        "detail": "Provide number of days to look up forecast"
    }

In addition to this, the number of days must lie between 0 and 10 days. Anything below this also result in an error 406. For example, making a request like `api/locations/lusaka/?days=13` or `api/locations/lusaka/?days=0` results in
the following error:

    {
        "detail": "Number of days to look up must be between 0 and 10"
    }

When the days provided is empty.
Example request is `api/locations/lusaka/?days=`
The status code is also `406` with the following error message;

    {
        "detail": "Number of days to lookup cannot be an empty value."
    }

When the days provided is a string.
Example request is `api/locations/lusaka/?days=two`
The status code is also `406` with the following error message;

    {
        "detail": "Days provided must be a valid integer."
    }

### Testing

To run the test cases, run the following command

    python manage.py test core.tests

### Development

Pull the latest main version:

    git pull origin main

Create local development branch and switch to it:

    git branch {feature_branch_name}
    git checkout {feature_branch_name}

Make desired changes then commit the branch.

    git add .
    git commit -m "changes to{feature_branch_name}"
    git push origin {feature_branch_name}
