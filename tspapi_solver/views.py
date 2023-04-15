import json
import pika
import secrets
import string

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from rest_framework.response import Response
from rest_framework.views import APIView

from app import settings
from tspapi_solver.serializers import CreateVrpRequestSerializer, VrpSolverGetStatusSerializer, \
    CreateVrptwRequestSerializer

# Define the digits container for id generator
alphabet = string.ascii_letters + string.digits


# Establish connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=settings.MESSAGE_BROKER,
    port=settings.MESSAGE_BROKER_PORT,
    virtual_host='/',
    heartbeat=0,
    credentials=pika.PlainCredentials(settings.MESSAGE_BROKER_USERNAME, settings.MESSAGE_BROKER_PASSWORD)))

channel = connection.channel()
channel.heartbeat_interval = 0
channel.queue_declare(queue=settings.TSP_INPUT_QUEUE)
channel.queue_declare(queue=settings.TSP_OUTPUT_QUEUE)


class CreateVrpRequest(APIView):
    """
    The VRP solver API to submit job request for process VRP/TSP problem
    """

    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = CreateVrpRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.on_valid_request_data(request, serializer.validated_data)

    def on_valid_request_data(self, request, data):

        # Get or create message id
        message_id = str(data.get('id'))
        if message_id is None or message_id == "":
            message_id = "".join(secrets.choice(alphabet) for i in range(10))

        data['id'] = message_id

        # Define message type according to number of vehicles
        data['message_type'] = 'VRP' if data['num_vehicles'] > 1 else 'TSP'

        # Publish message to queue
        channel.basic_publish(
            exchange='',
            routing_key=settings.TSP_INPUT_QUEUE,
            properties=pika.BasicProperties(
                reply_to=message_id,
                correlation_id=message_id,
            ),
            body=json.dumps(data)
        )

        return Response({
            "code": status.HTTP_200_OK,
            "message": "Operation successful",
            "result": {
                "job": message_id
            }
        }, status=status.HTTP_200_OK)


class CreateVrptwRequest(APIView):
    """
    The VRP solver API to submit job request for process VRP/TSP problem
    """

    parser_classes = (MultiPartParser, FormParser, JSONParser)
    serializer_class = CreateVrptwRequestSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.on_valid_request_data(request, serializer.validated_data)

    def on_valid_request_data(self, request, data):

        # Get or create message id
        message_id = str(data.get('id'))
        if message_id is None or message_id == "":
            message_id = "".join(secrets.choice(alphabet) for i in range(10))

        data['id'] = message_id

        # Define message type
        data['message_type'] = 'VRPTW'

        # Publish message to queue
        channel.basic_publish(
            exchange='',
            routing_key=settings.TSP_INPUT_QUEUE,
            properties=pika.BasicProperties(
                reply_to=message_id,
                correlation_id=message_id,
            ),
            body=json.dumps(data)
        )

        return Response({
            "code": status.HTTP_200_OK,
            "message": "Operation successful",
            "result": {
                "job": message_id
            }
        }, status=status.HTTP_200_OK)


class RetrieveJobStatus(APIView):
    """
    The API to get result of a job based on job identifier
    """

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = VrpSolverGetStatusSerializer

    def get(self, request):
        serializer = self.serializer_class(data=request.query_params)
        serializer.is_valid(raise_exception=True)
        return self.on_valid_request_data(request, serializer.validated_data)

    def on_valid_request_data(self, request, data):
        correlation_id = data.get('id')

        # Consume message from  queue with matching correlation ID
        method_frame, header_frame, body = channel.basic_get(queue=settings.TSP_OUTPUT_QUEUE)

        if method_frame:
            # Check correlation ID and return status if it matches
            if header_frame.correlation_id == correlation_id:
                channel.basic_ack(method_frame.delivery_tag)

                return Response({
                    "code": status.HTTP_200_OK,
                    "message": "Operation successful",
                    "result": json.loads(body.decode())
                }, status=status.HTTP_200_OK)

            # If correlation ID does not match, re-queue message and return error
            channel.basic_nack(method_frame.delivery_tag, requeue=True)

            return Response({
                "code": status.HTTP_404_NOT_FOUND,
                "message": "No matching message found with message id = {}".format(correlation_id),
            }, status=status.HTTP_404_NOT_FOUND)

        return Response({
            "code": status.HTTP_404_NOT_FOUND,
            "message": "No messages available",
        }, status=status.HTTP_404_NOT_FOUND)
