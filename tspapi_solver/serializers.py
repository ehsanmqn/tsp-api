from rest_framework import serializers


class CreateVrpRequestSerializer(serializers.Serializer):
    """
    Input serializer for the VRP solver submit API
    """
    id = serializers.CharField(min_length=1, max_length=64, allow_blank=True, allow_null=True, help_text="Request ID (If not specified, an ID will generate automatically for the request)")
    depot = serializers.IntegerField(required=True, min_value=0, help_text="The start and end location for the route")
    num_vehicles = serializers.IntegerField(required=True, min_value=0, help_text="The number of vehicles in the fleet. If set 1, it would be TSP. (For a vehicle routing problem (VRP), the number of vehicles can be greater than 1.)")
    locations = serializers.JSONField(required=True, allow_null=False, help_text="Geographical locations of the problem. Use JSON format data inside array: [{\"latitude\": 40.7128, \"longitude\": -74.0060}, ... ]")
    max_distance = serializers.IntegerField(required=True, min_value=0, help_text="Vehicle maximum travel distance")
    cost_coefficient = serializers.IntegerField(required=True, min_value=0, help_text="Difference between the largest value of route end cumul variables and the smallest value of route start cumul variables.")


class CreateVrptwRequestSerializer(serializers.Serializer):
    """
    Input serializer for the VRP solver submit API
    """
    id = serializers.CharField(min_length=1, max_length=64, allow_blank=True, allow_null=True, help_text="Request ID (If not specified, an ID will generate automatically for the request)")
    depot = serializers.IntegerField(required=True, min_value=0, help_text="The start and end location for the route")
    num_vehicles = serializers.IntegerField(required=True, min_value=0, help_text="The number of vehicles in the fleet. If set 1, it would be TSP. (For a vehicle routing problem (VRP), the number of vehicles can be greater than 1.)")
    locations = serializers.JSONField(required=True, allow_null=False, help_text="Geographical locations of the problem. Use JSON format data inside array: [{\"latitude\": 40.7128, \"longitude\": -74.0060}, ... ]")
    time_windows = serializers.JSONField(required=True, allow_null=False, help_text="An array of time windows for the locations.")
    wait_time = serializers.IntegerField(required=True, min_value=0, help_text="An upper bound for the total time over each vehicle's route.")
    max_time_vehicle = serializers.IntegerField(required=True, min_value=0, help_text="An upper bound for slack (the wait times at the locations).")


class RetrieveJobStatusSerializer(serializers.Serializer):
    """
    Input serializer for the VRP solver get status
    """
    id = serializers.CharField(required=True, min_length=1, max_length=64, help_text="Request ID")
