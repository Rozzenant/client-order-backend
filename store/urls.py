from django.urls import path
from store.views import ClientTotalSumRawSQLView

urlpatterns = [
    path("analytics/client-total-sum-raw/", ClientTotalSumRawSQLView.as_view()),
]
