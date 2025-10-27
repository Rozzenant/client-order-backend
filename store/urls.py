from django.urls import path
from store.views import (
    CategoryChildrenCountRawSQLView,
    ClientTotalSumRawSQLView,
    RefreshTop5ProductsView,
    Top5ProductsLastMonthAPIView,
    Top5ProductsMaterializedView,
)

urlpatterns = [
    path("analytics/client-total-sum-raw/", ClientTotalSumRawSQLView.as_view()),
    path(
        "analytics/category-children-count-raw/",
        CategoryChildrenCountRawSQLView.as_view(),
    ),
    path("api/top-products/", Top5ProductsLastMonthAPIView.as_view()),
    path("top5-products/", Top5ProductsMaterializedView.as_view()),
    path("top5-products/refresh/", RefreshTop5ProductsView.as_view()),
]
