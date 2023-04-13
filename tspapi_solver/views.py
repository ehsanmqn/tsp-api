import json

from django.shortcuts import render

from rest_framework import status
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.response import Response
from rest_framework.views import APIView

from tspapi_solver.serializers import VrpSolverInputSerializer


class VrpSolver(APIView):
    """
    The VRP solver API
    """

    parser_classes = (MultiPartParser, FormParser)
    serializer_class = VrpSolverInputSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return self.on_valid_request_data(request, serializer.validated_data)

    def on_valid_request_data(self, request, data):

        return Response({
            "code": status.HTTP_200_OK,
            "message": "Operation successful",
            "result": data
        }, status=status.HTTP_200_OK)
