# Phimart - E-commerce API

Phimart is a Django Rest Framework (DRF)-based eCommerce backend that provides API endpoints for managing products, categories, orders, and carts. It also includes JWT authentication using Djoser and API documentation with Swagger (drf_yasg).

## Features

- **Product Management**: Create, update, retrieve, and delete products.
- **Category Management**: Organize products into categories.
- **Cart System**: Add, remove, and manage cart items.
- **Order Processing**: Place and manage orders.
- **JWT Authentication**: Secure authentication using Djoser.
- **Swagger API Documentation**: Interactive API documentation with drf_yasg.

## Technologies Used

- **Django** - High-level Python web framework
- **Django REST Framework (DRF)** - Toolkit for building REST APIs
- **Djoser** - Authentication system with JWT support
- **drf_yasg** - API documentation with Swagger UI
- **PostgreSQL** (or SQLite) - Database

## Installation

1. **Clone the Repository**
   ```sh
   git clone https://github.com/yourusername/phimart.git
   cd phimart
   ```

2. **Create and Activate Virtual Environment**
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```sh
   pip install -r requirements.txt
   ```

4. **Apply Migrations**
   ```sh
   python manage.py migrate
   ```

5. **Create a Superuser (Optional, for Admin Access)**
   ```sh
   python manage.py createsuperuser
   ```

6. **Run the Development Server**
   ```sh
   python manage.py runserver
   ```

## API Endpoints

| Method | Endpoint                 | Description |
|--------|--------------------------|-------------|
| GET    | `/api/products/`         | List all products |
| POST   | `/api/products/`         | Create a new product |
| GET    | `/api/categories/`       | List all categories |
| GET    | `/api/cart/`             | Get user cart |
| POST   | `/api/cart/add/`         | Add an item to the cart |
| POST   | `/api/orders/`           | Place an order |
| POST   | `/auth/jwt/create/`      | Obtain JWT token |
| POST   | `/auth/jwt/refresh/`     | Refresh JWT token |

## API Documentation

Swagger UI is available at:
```
http://127.0.0.1:8000/swagger/
```

ReDoc documentation is available at:
```
http://127.0.0.1:8000/redoc/
```

## Envirnment Variables
Create a `.env` file in the root directory and add the following:
```ini
SECRET_KEY=your_secret_key
DEBUG=True
DATABASE_URL=pour_database_url
ALLOWED_HOSTS=*
EMIL_HOST=your_emali_host
```

## Authentication
Phimart uses JWT authentication. To access protected routes:

1. Obtain a token:
   ```sh
   POST /auth/jwt/create/ {"email": "user@example.com", "password": "password"}
   ```
2. Use the token in requests:
   ```sh
   Authorization: Bearer <your_token>
   ```

## Contributing

Contributions are welcome! Feel free to fork the repository and submit a pull request.

## License

This project is licensed under the MIT License.

____
### Author
[Your Name](https://github.com/yourusername)