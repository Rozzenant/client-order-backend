from django.urls import path
from store.views import CategoryChildrenCountRawSQLView, ClientTotalSumRawSQLView

urlpatterns = [
    path("analytics/client-total-sum-raw/", ClientTotalSumRawSQLView.as_view()),
    path(
        "analytics/category-children-count-raw/",
        CategoryChildrenCountRawSQLView.as_view(),
    ),
]
