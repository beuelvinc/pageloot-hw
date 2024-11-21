from django.urls import path
from .views import (
    UserListCreateView,
    ExpenseListCreateView,
    ExpenseDetailView,
    ExpensesByDateRangeView,
    CategorySummaryView,
)

urlpatterns = [
    path('users/', UserListCreateView.as_view(), name='user-list-create'),
    path('expenses/', ExpenseListCreateView.as_view(), name='expense-list-create'),
    path('expenses/<int:pk>/', ExpenseDetailView.as_view(), name='expense-detail'),
    path('expenses/<int:user_id>/date-range/', ExpensesByDateRangeView.as_view(), name='expenses-by-date-range'),
    path('expenses/<int:user_id>/category-summary/', CategorySummaryView.as_view(), name='category-summary')
]
