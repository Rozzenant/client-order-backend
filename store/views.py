# from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from store.services.analytics import (
    get_category_children_counts,
    get_clients_with_total_sum,
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
