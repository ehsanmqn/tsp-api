# Django TSP Solver API
This is a Django project that provides two APIs for solving Vehicle Routing Problem (VRP). This project uses RabbitMQ as message broker to communicate with the [TSP Solver service](https://github.com/ehsanmqn/tsp_solver).

This project designed to provide APIs to communicate with the VRP Solver. It is able to use cases related following probles:
1. Traveling Salesperson Problem (TSP) 
2. Vehicle Routing Problem (VRP)

## Usage
### Manual
1. Clone the repository
2. Create a virtual environment using the command python -m venv env
3. Activate the virtual environment using the command source env/bin/activate
4. Install dependencies using the command pip install -r requirements.txt
5. To run the Django server, use the command python manage.py runserver.

### Docker
Run following command in the project directory
```bash
docker-compose up --build
```

## Endpoints
### Submit Job Request API
`Endpoint`: /vrp-submit/

`Method`: POST

**Form Data:**
* `id`: A unique string ID for the job
* `data`: A JSON object containing the problem data in the following format:
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
    ]
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

### Get Job Status API
`Endpoint`: /get-status/

`Method`: GET

**Query Parameters:**
* `id`: The unique string ID of the job

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

If the job does not exist, the response will be:
```json
{
  "code": 404,
  "message": "No messages available"
}
```

## Message Broker
The project uses RabbitMQ as the message broker to handle the communication between the VRP solver and the client. The connection parameters are read from Django settings file.

The input queue name and output queue name are set in Django settings file as well.

## Dependencies
This project depends on the following packages:

* Django
* djangorestframework
* pika (for RabbitMQ connection)