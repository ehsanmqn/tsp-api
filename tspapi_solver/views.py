import json
import pika

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from app import settings
from tspapi_solver.serializers import VrpSolverSubmitStatelessSerializer, VrpSolverGetStatusSerializer

# Establish connection with RabbitMQ server
connection = pika.BlockingConnection(pika.ConnectionParameters(
    host=settings.MESSAGE_BROKER,
    port=settings.MESSAGE_BROKER_PORT,
    virtual_host='/',
    credentials=pika.PlainCredentials(settings.MESSAGE_BROKER_USERNAME, settings.MESSAGE_BROKER_PASSWORD)))

channel = connection.channel()
channel.queue_declare(queue='TSP_INPUT_QUEUE')
channel.queue_declare(queue='TSP_OUTPUT_QUEUE')


class VrpSolverSubmitStateless(APIView):
    """
    The VRP solver API to submit job request for process data
    """

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = VrpSolverSubmitStatelessSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.on_valid_request_data(request, serializer.validated_data)

    def on_valid_request_data(self, request, data):

        # Publish message to queue
        channel.basic_publish(
            exchange='',
            routing_key=settings.TSP_INPUT_QUEUE,
            properties=pika.BasicProperties(
                reply_to=str(data.get('id')),
                correlation_id=str(data.get('id')),
            ),
            body=json.dumps(data)
        )

        return Response({
            "code": status.HTTP_200_OK,
            "message": "Operation successful",
            "result": {
                "job": data.get('id')
            }
        }, status=status.HTTP_200_OK)


class VrpSolverGetStatus(APIView):
    """
    The VRP solver API to get result of a job based on job id
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
