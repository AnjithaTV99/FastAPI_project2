Overview:
This project demonstrates a simple user registration system using the FastAPI framework. The application utilizes both MongoDB and PostgreSQL databases to store user information and profile pictures, respectively. The project is structured with a modular approach, separating database management into a dedicated module.

Features:
User Registration:

Users can register with a full name, email, password, phone number, and a profile picture.
Database Integration:

MongoDB is used for storing user profile pictures.
PostgreSQL is used for storing user registration details.
Error Handling:

Proper error handling is implemented for scenarios such as duplicate email registration.
Structured Codebase:

The project is organized with separate modules for MongoDB and PostgreSQL database management, making it modular and maintainable.
Technologies Used:
FastAPI: A modern, fast (high-performance), web framework for building APIs with Python 3.7+ based on standard Python type hints.
SQLAlchemy: A SQL toolkit and Object-Relational Mapping (ORM) library for Python.
Motor: An asynchronous Python driver for MongoDB.
Project Structure:
main.py: The main FastAPI application file containing API routes.
models.py: Defines SQLAlchemy models for PostgreSQL database.
database.py: Manages database connections for both MongoDB and PostgreSQL.
config.py: Contains configuration settings, including database URLs.
How to Run:
Clone the repository.
Install the required dependencies using pip install -r requirements.txt.
Run the FastAPI application using uvicorn main:app --reload.
Open http://127.0.0.1:8000/docs in your browser to access the FastAPI Swagger documentation.
