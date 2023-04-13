from rest_framework import serializers


class VrpSolverInputSerializer(serializers.Serializer):
    """
    Input serializer for the VRP solver API view
    """
    id = serializers.CharField(required=True, min_length=1, max_length=64, help_text="Request ID")
    depot = serializers.IntegerField(required=True, min_value=0, help_text="The start and end location for the route")
    num_vehicles = serializers.IntegerField(required=True, min_value=0, help_text="The number of vehicles in the fleet. If set 1, it would be TSP. (For a vehicle routing problem (VRP), the number of vehicles can be greater than 1.)")
    locations = serializers.JSONField(required=True, allow_null=False, help_text="Geographical locations of the problem. Use JSON format data inside array: [{\"latitude\": 40.7128, \"longitude\": -74.0060}, ... ]")
