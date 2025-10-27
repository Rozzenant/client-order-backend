# from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from store.services.analytics import get_clients_with_total_sum


class ClientTotalSumRawSQLView(APIView):
    def get(self, request):
        rows = get_clients_with_total_sum()
        data = [{"name": row[0], "total_sum": row[1]} for row in rows]
        return Response(data)
