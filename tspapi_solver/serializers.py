from rest_framework import serializers


class VrpSolverInputSerializer(serializers.Serializer):
    """
    Input serializer for the VRP solver API view
    """
    id = serializers.CharField(required=True)
    depot = serializers.IntegerField(required=True)
    num_vehicles = serializers.IntegerField(required=True)
    locations = serializers.JSONField(required=True)