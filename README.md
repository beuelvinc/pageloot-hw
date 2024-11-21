# Pageloot Project

A Django-based application that manages expenses, backed by PostgreSQL and Docker.

## Prerequisites
1. Docker installed. You can install Docker by following the instructions at [Install Docker](https://docs.docker.com/get-docker/).
2. Docker Compose installed. You can install Docker Compose by following the instructions at [Install Docker Compose](https://docs.docker.com/compose/install/).

## Running the Project
To run the entire project, simply execute the following command in the root directory:
docker-compose up -d

Once the project is running, open your browser and navigate to:
http://localhost:8080

## Running Unit Tests
To run the unit tests:
1. Access the Django container:
docker exec -it django_container_name bash
2. Run the unit tests inside the container:
python manage.py test

## Running E2E Test Cases with Robot Framework
This project includes basic E2E test cases, assuming the DRF UI is the actual UI.

Steps to Run E2E Tests:
1. Create a virtual environment:
python -m venv e2e-env
source e2e-env/bin/activate  # On Windows, use e2e-env\Scripts\activate
2. Install dependencies:
pip install -r requirements-e2e-test.txt
3. Navigate to the E2E tests directory:
cd e2e-tests
4. Run the E2E test:
robot test-expense-app.robot

