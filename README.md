# B2B E-commerce Platform

A B2B e-commerce platform built with Django, supporting Arabic language and RTL layout.

## Features

- Multi-user system (Admin, Company, Customer, Guest)
- Arabic language support with RTL layout
- Company profile management
- Product management
- Order management
- Discount and offers system
- Interactive search
- Shopping cart
- Location-based services
- PDF order confirmation
- Interactive maps integration

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run migrations:
```bash
python manage.py migrate
```

4. Create a superuser:
```bash
python manage.py createsuperuser
```

5. Run the development server:
```bash
python manage.py runserver
```

## Project Structure

- `accounts/`: User authentication and profiles
- `companies/`: Company management
- `products/`: Product management
- `orders/`: Order management
- `cart/`: Shopping cart functionality
- `core/`: Core functionality and settings
- `static/`: Static files
- `templates/`: HTML templates
- `media/`: User uploaded files

## License

MIT License 