# Django TSP Solver API
This is a Django project that provides APIs for solving TSP, VRP, and VRPTW problems. This project uses RabbitMQ as message broker to communicate with the [TSP Solver service](https://github.com/ehsanmqn/tsp-solver).

This project designed to provide APIs to communicate with the TSP Solver service. It is able to use cases related following problems:
1. Traveling Salesperson Problem (TSP) 
2. Vehicle Routing Problem (VRP)
3. Vehicle Routing Problem with Time Window (VRPTW)

## Usage
### Manual
1. Clone the repository
2. Create a virtual environment using the command `virtualenv -p python3 venv`
3. Activate the virtual environment using the command `source venv/bin/activate`
4. Install dependencies using the command `pip install -r requirements.txt`
5. Collect static files using command `python manage.py collectstatic`
6. Considering the RabbitMQ is running on _localhost_, Run this command: `export MESSAGE_BROKER="localhost"`
7. To run the Django server, use the command `python manage.py runserver 0.0.0.0:8000`.

### Docker compose
Run following command in the project directory
```bash
docker-compose up
```

## Endpoints
The API documentation is provided upon opening each of the following endpoint addresses.

### Submit VRP/TSP problem
`Endpoint`: http://127.0.0.1:8000/api/v1/vrp-tsp/

`Method`: POST

**Request Data:**

For TSP request, the _num_vehicles_ must be 1. Otherwise, it will be considered as VRP problem.
```json
{
    "id": 1,
    "depot": 0,
    "num_vehicles": 1,
    "locations": [
        {"latitude": 40.7128, "longitude": -74.0060},
            {"latitude": 34.0522, "longitude": -118.2437},
            {"latitude": 41.8781, "longitude": -87.6298},
            {"latitude": 29.7604, "longitude": -95.3698},
            {"latitude": 39.9526, "longitude": -75.1652},
            {"latitude": 33.4484, "longitude": -112.0740},
            {"latitude": 29.4241, "longitude": -98.4936},
            {"latitude": 32.7157, "longitude": -117.1611},
            {"latitude": 32.7767, "longitude": -96.7970},
            {"latitude": 37.3382, "longitude": -121.8863}
    ],
    "max_distance": 100000,
    "cost_coefficient": 100
}
```
**Response:**
* Status: 200 OK
* Body:
```json
{
    "code": 200,
    "message": "Operation successful",
    "result": {
        "job": "1"
    }
}
```
Use the job identifier in order to retrieve result related to this job.


### Submit VRPTW problem
`Endpoint`: http://127.0.0.1:8000/api/v1/vrptw/

`Method`: POST

**Request Data:**

```json
{
    "message_type": "VRPTW",
    "id": "968ae423-2a40-447e-943c-de18b3a2ef12",
    "depot": 0,
    "num_vehicles": 2,
    "locations": [
        {"latitude": 40.7128, "longitude": -74.0060},
            {"latitude": 34.0522, "longitude": -118.2437},
            {"latitude": 41.8781, "longitude": -87.6298},
            {"latitude": 29.7604, "longitude": -95.3698},
            {"latitude": 39.9526, "longitude": -75.1652},
            {"latitude": 33.4484, "longitude": -112.0740},
            {"latitude": 29.4241, "longitude": -98.4936},
            {"latitude": 32.7157, "longitude": -117.1611},
            {"latitude": 32.7767, "longitude": -96.7970},
            {"latitude": 37.3382, "longitude": -121.8863}
    ],
    "time_windows": [
        [0, 5],  
        [7, 12],
        [10, 15],
        [16, 18],  
        [10, 13],  
        [0, 5],  
        [5, 10],  
        [0, 4],  
        [5, 10],  
        [0, 3]  
    ],
    "wait_time": 30,
    "max_time_vehicle": 30
}
```
**Response:**
* Status: 200 OK
* Body:
```json
{
    "code": 200,
    "message": "Operation successful",
    "result": {
        "job": "968ae423-2a40-447e-943c-de18b3a2ef12"
    }
}
```

### Get Job Status API
To retrieve results related to a particular job, utilize its identifier. However, keep in mind that as this project is stateless and the tsp-solver requires time to solve the problem and publish the results on topic, there may be instances where a valid id returns a 404 error. If this occurs, you will need to make the request again until the result is obtained.

The API extracts the ID from the validated data and consumes messages from the TSP_OUTPUT_QUEUE using the pika library. It checks each message for a matching correlation ID and returns the result if found. If no matching message is found, it Nack all the consumed messages and returns a 404 NOT FOUND response.


`Endpoint`: http://127.0.0.1:8000/api/v1/status/?id=968ae423-2a40-447e-943c-de18b3a2ef12

`Method`: GET

**Query Parameters:**
* `id`: The unique identifier of the job provided in earlier APIs response

**Response:**
* Status: 200 OK
* Body:
```json
{
    "code": 200,
    "message": "Operation successful",
    "result": {
        "id": "ehsanmgh",
        "solution": [
            {
                "route": [
                    0,
                    4,
                    8,
                    3,
                    6,
                    5,
                    7,
                    1,
                    9,
                    2,
                    0
                ],
                "vehicle": 0,
                "distance": 10476
            }
        ],
        "code": 200,
        "message": "Operation successful."
    }
}
```
If the job is not yet completed, the response will be:
```json
{
  "code": 404,
  "message": "No matching message found with message id = job_id"
}
```

## Message Broker
The project uses RabbitMQ as the message broker to handle the communication between the TSP solver service and the client. The connection parameters are read from Django settings file.

The input queue name and output queue name are set in Django settings file as well.

## Dependencies
This project depends on the following packages:

* Django
* djangorestframework
* pika (for RabbitMQ connection)

## Tests
The CreateVrpRequest API view has 5 implemented tests. To conduct tests on this view, utilize the following command:

```bash
export MESSAGE_BROKER="localhost"
python manage.py test
```
