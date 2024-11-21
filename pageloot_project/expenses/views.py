import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Sum
from .models import Expense, User
from .serializers import *

logger = logging.getLogger('django')


class UserListCreateView(APIView):
    def get(self, request):
        logger.debug("Fetching all users")
        users = User.objects.all()
        serializer = UserSerializer(users, many=True)
        logger.info(f"{len(users)} users fetched successfully.")
        return Response(serializer.data)

    def post(self, request):
        logger.debug("Creating a new user")
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"User {serializer.data['username']} created successfully.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"User creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseListCreateView(APIView):
    def get(self, request):
        logger.debug("Fetching all expenses")
        expenses = Expense.objects.all()
        serializer = ExpenseSerializer(expenses, many=True)
        logger.info(f"{len(expenses)} expenses fetched successfully.")
        return Response(serializer.data)

    def post(self, request):
        logger.debug("Creating a new expense")
        serializer = ExpenseSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            logger.info(f"Expense '{serializer.data['title']}' created successfully.")
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        logger.error(f"Expense creation failed: {serializer.errors}")
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ExpenseDetailView(APIView):
    def get(self, request, pk):
        logger.debug(f"Fetching expense with ID {pk}")
        try:
            expense = Expense.objects.get(pk=pk)
            serializer = ExpenseSerializer(expense)
            logger.info(f"Expense {expense.title} fetched successfully.")
            return Response(serializer.data)
        except Expense.DoesNotExist:
            logger.error(f"Expense with ID {pk} not found.")
            return Response({"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

    def put(self, request, pk):
        logger.debug(f"Updating expense with ID {pk}")
        try:
            expense = Expense.objects.get(pk=pk)
            serializer = ExpenseSerializer(expense, data=request.data, partial = True)
            if serializer.is_valid():
                serializer.save()
                logger.info(f"Expense {expense.title} updated successfully.")
                return Response(serializer.data)
            logger.error(f"Expense update failed: {serializer.errors}")
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Expense.DoesNotExist:
            logger.error(f"Expense with ID {pk} not found.")
            return Response({"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, pk):
        logger.debug(f"Deleting expense with ID {pk}")
        try:
            expense = Expense.objects.get(pk=pk)
            expense.delete()
            logger.info(f"Expense with ID {pk} deleted successfully.")
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Expense.DoesNotExist:
            logger.error(f"Expense with ID {pk} not found.")
            return Response({"error": "Expense not found."}, status=status.HTTP_404_NOT_FOUND)


class ExpensesByDateRangeView(APIView):
    def get(self, request, user_id):
        logger.debug(f"Fetching expenses for user {user_id} in date range")
        start_date = request.query_params.get('start_date')
        end_date = request.query_params.get('end_date')

        if not start_date or not end_date:
            logger.error("Date range is missing in the request.")
            return Response(
                {"error": "Both start_date and end_date are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        expenses = Expense.objects.filter(user_id=user_id, date__range=[start_date, end_date])
        logger.info(f"{len(expenses)} expenses fetched for user {user_id} from {start_date} to {end_date}.")
        serializer = ExpenseSerializer(expenses, many=True)
        return Response(serializer.data)


class CategorySummaryView(APIView):
    def get(self, request, user_id):
        logger.debug(f"Fetching category summary for user {user_id}")
        month = request.query_params.get('month')
        year = request.query_params.get('year')

        if not month or not year:
            logger.error("Month or year is missing in the request.")
            return Response(
                {"error": "Both month and year are required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        expenses = Expense.objects.filter(user_id=user_id, date__year=year, date__month=month)
        summary = expenses.values('category').annotate(total=Sum('amount'))
        logger.info(f"Category summary generated for user {user_id} for {month}/{year}.")
        return Response(summary)
