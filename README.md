Aforro Backend Developer Assignment (Round-2)

This repository contains a complete Django backend project built as part of the Aforro Backend Developer assessment.
The project focuses on scalability, performance, clean architecture, caching, async processing, and containerization.


1️) Complete Django Project

The project is built using Django + Django REST Framework and follows a modular app-based architecture.

Apps Included

products – Categories & Products

stores – Stores & Inventory

orders – Orders & Order Items

search – Search suggestions

core – Health check & base logic


2️) Models, APIs, Serializers & URLs

🔹 Core Models

Category

Product

Store

Inventory

Order

OrderItem

Each model is normalized and uses foreign key relationships for data integrity.

🔹 API Design

API-only backend (JSON responses)

Built using APIView

No HTML templates used

🔹 Example API Endpoints

Endpoint	Method	Description

/	GET	Health check

/stores/<id>/inventory/	GET	Store inventory

/api/search/suggest/?q=	GET	Search suggestions

/orders/<store_id>/	GET	Orders summary

3️) Seed Data Command

A custom Django management command is used to generate realistic test data.

Command Location

core/management/commands/seed_data.py

Run Seed Command

python manage.py seed_data

Data Generated

10 Categories

1000 Products

20 Stores

Inventory for each store

✔️ Uses Faker for realistic data

✔️ Helps test performance at scale


4️) Redis Implementation (Caching)

Redis is used to cache search suggestions to improve performance.

Cached Logic

Search results are cached based on query string

Reduces repeated database hits

Example

cache_key = f"search:{query}"

data = cache.get(cache_key)

if not data:

    data = get_suggestions_from_db(query)
    
    cache.set(cache_key, data, timeout=300)

Benefits

Faster API responses

Reduced database load

Scalable under high traffic


5️) Celery Task Integration (Async)

Celery is integrated for background processing.

Use Case

Order processing

Async tasks that should not block API response

Example Task

@shared_task

def process_order(order_id):

    order = Order.objects.get(id=order_id)
    
    # async processing logic

Why Celery?

Non-blocking API

Handles heavy operations

Improves user experience


6️) Docker Environment

The project is fully Dockerized for consistent setup.

Docker Services

Django API

Redis

Celery Worker

Run with Docker

docker-compose up --build

Docker Benefits

Easy deployment

Same environment across systems

Production-ready setup


7️) Tests (3–5)

Basic test cases are included to validate core functionality.

Tests Covered

Store inventory API

Search suggestions API

Order aggregation logic

Run Tests

python manage.py test


✔️ Ensures API correctness

✔️ Prevents regressions


8️) Setup Instructions

Local Setup

git clone <repo-url>

cd project

python -m venv myenv

myenv\Scripts\activate

pip install -r requirements.txt

python manage.py migrate

python manage.py seed_data

python manage.py runserver


9️) Docker Usage

Build & Run

docker-compose up --build

Stop Containers

docker-compose down

10) Sample API Requests
    
Health Check

GET /

{

  "status": "ok",
  
  "message": "Aforro Backend API is running"
  
}

Store Inventory

GET /stores/1/inventory/

[

  {
  
    "product": "Laptop",
    
    "price": "55000",
    
    "category": "electronics",
    
    "quantity": 15
    
  }
  
]

Search Suggestions

GET /api/search/suggest/?q=lap

{

  "suggestions": ["laptop", "lapdesk"]
  
}


11) Notes on Caching & Async Logic


Redis caches frequent search queries

Celery handles background tasks

API remains responsive under load

Designed for horizontal scaling


12) Scalability Considerations


Optimized ORM queries (select_related, annotate)

Redis caching layer

Async task processing with Celery

Dockerized microservice-ready setup

Database can be switched to PostgreSQL easily

Author

Dudekula Rajesh
Backend Developer | Django | REST APIs

Final Notes

API-only backend

Production-ready structure

Meets all assessment requirements

Designed with scalability in mind
