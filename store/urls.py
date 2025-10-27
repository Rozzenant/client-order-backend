from django.urls import path
from store.views import (
    CategoryChildrenCountRawSQLView,
    ClientTotalSumRawSQLView,
    Top5ProductsLastMonthAPIView,
)

urlpatterns = [
    path("analytics/client-total-sum-raw/", ClientTotalSumRawSQLView.as_view()),
    path(
        "analytics/category-children-count-raw/",
        CategoryChildrenCountRawSQLView.as_view(),
    ),
    path("api/top-products/", Top5ProductsLastMonthAPIView.as_view()),
]
