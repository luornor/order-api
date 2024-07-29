
# Order Management Service
## Responsibilities
Manage delivery information and statuses.
Communicate with delivery api to create a delivery
## Order Summary:
Display details of a specific order.
## Order History:
List of all orders placed by the user.

## Table of Contents

- [Requirements](#requirements)
- [Installation](#installation)
- [Configuration](#configuration)
- [Running the Project](#running-the-project)
- [API Documentation](#api-documentation)

## Requirements

- Python 3.x
- Django 3.x or higher
- Django REST Framework

## Installation

1. **Clone the repository:**

   git clone https://github.com/luornor/api-gateway.git
   cd api-gateway
   
## Create a virtual environment:

python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`

## Install the dependencies:

pip install -r requirements.txt

### Database Migrations:

Run the following commands to apply the database migrations:

python manage.py makemigrations
python manage.py migrate

## Configuration
### Environment Variables:

Create a `.env` file in the project root and add the following environment variables:

SECRET_KEY=your_secret_key
DEBUG=True  # Set to False in production
CLOUDAMQP_URL

## Running the Project

### Start the development server:

python manage.py runserver

The API will be available at `http://127.0.0.1:8002/`.

## API Documentation

This project uses Swagger for API documentation. Once the server is running, you can access the documentation at:

`http://127.0.0.1:8002/`


## Additional Information

### Admin Panel:

You can access the Django admin panel at `http://127.0.0.1:8002/admin/`.

### Static Files:

Collect static files by running:

python manage.py collectstatic


### Creating a Superuser:

To create a superuser account, run:

python manage.py createsuperuser

## License

This project is licensed under the MIT License. See the `LICENSE` file for details.

Feel free to customize this template according to your project's specific requirements and details.


