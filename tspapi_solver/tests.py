import json

from django.urls import reverse
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status


class VrpSolverTestCase(TestCase):

    def setUp(self):
        self.client = APIClient()
        self.url = reverse("vrp-solver")

    def test_valid_request_data(self):
        # create a valid request data
        data = {
            "id": "1234",
            "depot": 0,
            "num_vehicles": 1,
            "locations": json.dumps([{"latitude": 40.7128, "longitude": -74.0060}])
        }

        # post the request to the API endpoint
        response = self.client.post(self.url, data)

        # assert that the response code is 200 OK
        self.assertIn("code", response.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # assert that the response message is "Operation successful"
        self.assertIn("message", response.data)
        self.assertEqual(response.data["message"], "Operation successful")

        # assert that the response result is equal to the request data
        self.assertIn("result", response.data)

