from django.urls import path
from apps.dashboard.views import (
    DashboardStatsView,
    SalesOverTimeView,
    PopularProductsView,
    AppointmentsStatsView,
    RecentActivityView,
    LowStockProductsView,
)

urlpatterns = [
    path('stats/', DashboardStatsView.as_view(), name='dashboard-stats'),
    path('sales-over-time/', SalesOverTimeView.as_view(), name='sales-over-time'),
    path('popular-products/', PopularProductsView.as_view(), name='popular-products'),
    path('appointments-stats/', AppointmentsStatsView.as_view(), name='appointments-stats'),
    path('recent-activity/', RecentActivityView.as_view(), name='recent-activity'),
    path('low-stock/', LowStockProductsView.as_view(), name='low-stock-products'),
]
