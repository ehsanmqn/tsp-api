import json

from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class CreateVrpRequestTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("request-vrp-tsp-api")

    def test_valid_request_data(self):
        # create a valid request data
        data = {
            "id": "1234",
            "depot": 0,
            "num_vehicles": 1,
            "locations": json.dumps([{"latitude": 40.7128, "longitude": -74.0060}]),
            "max_distance": 100000,
            "cost_coefficient": 100
        }

        # post the request to the API endpoint
        response = self.client.post(self.url, data)

        # assert that the response code is 200 OK
        self.assertIn("code", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assert that the response message is "Operation successful"
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Operation successful")

        # assert that the response result contains "result" key
        self.assertIn("result", response.data)

    def test_invalid_id(self):
        # create an invalid request data with empty ID
        data = {
            "id": "",
            "depot": 0,
            "num_vehicles": 1,
            "locations": json.dumps([{"latitude": 40.7128, "longitude": -74.0060}]),
            "max_distance": 100000,
            "cost_coefficient": 100
        }

        # post the request to the API endpoint
        response = self.client.post(self.url, data)

        # assert that the response code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_depot(self):
        # create an invalid request data with depot < 0
        data = {
            "id": "1234",
            "depot": -1,
            "num_vehicles": 1,
            "locations": json.dumps([{"latitude": 40.7128, "longitude": -74.0060}])
        }

        # post the request to the API endpoint
        response = self.client.post(self.url, data)

        # assert that the response code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # assert that the response message is "Invalid input data"
        self.assertIn("depot", response.data)

    def test_invalid_num_vehicles(self):
        # create an invalid request data with num_vehicles = 0
        data = {
            "id": "1234",
            "depot": 0,
            "num_vehicles": -1,
            "locations": json.dumps([{"latitude": 40.7128, "longitude": -74.0060}])
        }

        # post the request to the API endpoint
        response = self.client.post(self.url, data)

        # assert that the response code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # assert that the response message is "Invalid input data"
        self.assertIn("num_vehicles", response.data)

    def test_invalid_locations(self):
        # create an invalid request data with empty locations
        data = {
            "id": "1234",
            "depot": 0,
            "num_vehicles": 1,
            "locations": ""
        }

        # post the request to the API endpoint
        response = self.client.post(self.url, data)

        # assert that the response code is 400 Bad Request
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

        # assert that the response message is "Invalid input data"
        self.assertIn("locations", response.data)