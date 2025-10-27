# from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
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
