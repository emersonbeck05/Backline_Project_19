# **Backline Rental System**

A web-based instrument rental management system built with Django for Backline companies. The system allows employees to manage instrument inventory, track customer rentals, and handle check-in and check-out workflows.

### **Team Members**

Emerson Beck — UI Design, Wireframes

Ethan Jones — Frontend, Backend, Database Development

Madhav Mangalagiri — Database Schema, SQL Implementation


### **Project Overview**

Backline companies rent musical equipment to touring bands and musicians. This system replaces manual, error-prone processes with a centralized database-driven application. Employees can manage instrument inventory, register customers, and create and close rentals — all from a single interface.

### **Features**

Instrument inventory management (add, edit, track status)

Customer record management

Rental creation and tracking

Instrument check-in and check-out workflows

Status tracking: Available, Rented, Maintenance

Barcode-based instrument identification

### **Tech Stack**

Backend: Python, Django

Database: SQLite (via Django ORM)

Frontend: HTML, CSS (Django templates)


### **Project Structure**

backline/

|── models.py          # Database models: Instrument, Customer, Rental

|── IMPLEMENTATION.md  # Implementation details and decisions

|── README.md

### Database Models

Instrument
Stores all rental inventory items. Fields: barcode (unique), name, category, status (available / rented / maintenance).

Customer
Stores customer information. Fields: first_name, last_name, email (unique), phone_number.

Rental
Links a customer to an instrument for a rental period. Fields: instrument, customer, rental_date, returned, return_date. Includes a mark_returned() method that closes the rental and updates the instrument status back to available.

### **Setup & Installation**

Prerequisites

Python 3.x

Django

### **Steps**

### Clone the repository

git clone https://github.com/emersonbeck05/Backline_Project_19.git

cd backline

### Install Django

pip install django

### Apply database migrations

python manage.py makemigrations

python manage.py migrate

### Run the development server

python manage.py runserver

Then open your browser to http://127.0.0.1:8000/.

### **Architecture**

The system follows the MVC (Model-View-Controller) pattern:

Model — models.py defines the data structure and business logic (e.g., marking rentals as returned)

View — Django templates render the UI for inventory, customer, and rental pages

Controller — Django views handle user actions and update the database accordingly

### **SE Process**

This project uses "Scrum". Weekly standups are held to coordinate progress across milestones. Sprint planning and retrospectives are documented in each Project Milestone submission.