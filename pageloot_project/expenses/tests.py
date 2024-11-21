import unittest
from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User, Expense
from datetime import date

class TestExpenseAppTestCase(TestCase):
    def setUp(self):
        # Initialize the test client
        self.client = APIClient()

        # Create test users
        self.user1 = User.objects.create(username="testuser1", email="testuser1@example.com")
        self.user2 = User.objects.create(username="testuser2", email="testuser2@example.com")

        # Create test expenses
        self.expense1 = Expense.objects.create(
            user=self.user1, title="Groceries", amount=50.75, date=date(2024, 11, 20), category="Food"
        )
        self.expense2 = Expense.objects.create(
            user=self.user1, title="Flight Ticket", amount=300.50, date=date(2024, 11, 18), category="Travel"
        )
        self.expense3 = Expense.objects.create(
            user=self.user2, title="Electricity Bill", amount=100.00, date=date(2024, 11, 19), category="Utilities"
        )

        # Test URLs
        self.expenses_url = "/expenses/"
        self.expenses_detail_url = f"/expenses/{self.expense1.id}/"
        self.user_expenses_date_range_url = f"/expenses/{self.user1.id}/date-range/"
        self.user_expenses_category_summary_url = f"/expenses/{self.user1.id}/category-summary/"

    def test_create_user(self):
        """Test creating a user."""
        data = {"username": "newuser", "email": "newuser@example.com"}
        response = self.client.post("/users/", data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "newuser")

    def test_get_users(self):
        """Test retrieving all users."""
        response = self.client.get("/users/")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    def test_create_expense(self):
        """Test creating an expense."""
        data = {
            "user": self.user1.id,
            "title": "New Expense",
            "amount": 120.00,
            "date": "2024-11-21",
            "category": "Food",
        }
        response = self.client.post(self.expenses_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Expense")

    def test_retrieve_expense(self):
        """Test retrieving a single expense."""
        response = self.client.get(self.expenses_detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], self.expense1.title)

    def test_update_expense(self):
        """Test updating an expense."""
        data = {"title": "Updated Expense", "amount": 55.00}
        response = self.client.put(self.expenses_detail_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Expense")
        self.assertEqual(float(response.data["amount"]), 55.00)

    def test_delete_expense(self):
        """Test deleting an expense."""
        response = self.client.delete(self.expenses_detail_url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Expense.objects.filter(id=self.expense1.id).exists())

    def test_expenses_by_date_range(self):
        """Test filtering expenses by date range for a user."""
        params = {"start_date": "2024-11-17", "end_date": "2024-11-19"}
        response = self.client.get(self.user_expenses_date_range_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], self.expense2.title)

    def test_category_summary(self):
        """Test getting category summary for a user's expenses."""
        params = {"month": "11", "year": "2024"}
        response = self.client.get(self.user_expenses_category_summary_url, params)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)
        food_expense = next(item for item in response.data if item["category"] == "Food")
        self.assertEqual(float(food_expense["total"]), 50.75)

    def test_invalid_expense_amount(self):
        """Test creating an expense with an invalid amount."""
        data = {
            "user": self.user1.id,
            "title": "Invalid Expense",
            "amount": -10.00,  # Invalid negative amount
            "date": "2024-11-21",
            "category": "Food",
        }
        response = self.client.post(self.expenses_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("amount", response.data)
