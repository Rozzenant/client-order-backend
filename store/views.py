# from django.shortcuts import render

from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from store.models import Nomenclature, Order, OrderItem
from store.serializer import AddOrderItemSerializer
from store.services.analytics import (
    get_category_children_counts,
    get_clients_with_total_sum,
    get_top5_products_from_matview,
    get_top_5_products_last_month,
    refresh_top5_matview,
)


class ClientTotalSumRawSQLView(APIView):
    def get(self, request):
        rows = get_clients_with_total_sum()
        data = [{"name": row[0], "total_sum": row[1]} for row in rows]
        return Response(data)


class CategoryChildrenCountRawSQLView(APIView):
    def get(self, request):
        data = get_category_children_counts()
        return Response(data)


class Top5ProductsLastMonthAPIView(APIView):
    def get(self, request):
        data = get_top_5_products_last_month()
        return Response(data)


class Top5ProductsMaterializedView(APIView):
    def get(self, request):
        data = get_top5_products_from_matview()
        return Response(data)


class RefreshTop5ProductsView(APIView):
    def post(self, request):
        refresh_top5_matview()
        return Response({"status": "Materialized view refreshed"})


class AddOrderItemView(APIView):
    def post(self, request):
        serializer = AddOrderItemSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        order_id = serializer.validated_data["order_id"]
        nomenclature_id = serializer.validated_data["nomenclature_id"]
        quantity = serializer.validated_data["quantity"]

        order = get_object_or_404(Order, id=order_id)
        nomenclature = get_object_or_404(Nomenclature, id=nomenclature_id)

        if nomenclature.quantity < quantity:
            return Response(
                {"error": "Not enough stock"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        order_item, created = OrderItem.objects.get_or_create(
            order=order, nomenclature=nomenclature, defaults={"quantity": quantity}
        )

        if not created:
            order_item.quantity += quantity
            order_item.save()

        # Уменьшаем количество на складе
        nomenclature.quantity -= quantity
        nomenclature.save()

        return Response(
            {
                "message": "Item added successfully",
                "order_id": order.id,
                "nomenclature_id": nomenclature.id,
                "quantity": order_item.quantity,
            },
            status=status.HTTP_200_OK,
        )
