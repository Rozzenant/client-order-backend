from rest_framework import serializers


class AddOrderItemSerializer(serializers.Serializer):
    order_id = serializers.IntegerField()
    nomenclature_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)
