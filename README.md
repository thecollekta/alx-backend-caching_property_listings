# Property Listings API with Django, PostgreSQL, and Redis

A high-performance property listings API built with Django, PostgreSQL, and Redis for caching. This project demonstrates how to implement efficient data caching in a Django application.

## Features

- **Property Management**: Create, read, update, and delete property listings
- **High Performance**: Redis caching for improved response times
- **Containerized**: Docker and Docker Compose for easy setup and deployment
- **Scalable**: Designed to handle high traffic with efficient database queries
- **RESTful API**: Follows REST principles for easy integration

## Prerequisites

- Docker and Docker Compose
- Python 3.9+
- Git

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/your-username/alx-backend-caching_property_listings.git
cd alx-backend-caching_property_listings
```

### 2. Set up environment variables

Create a `.env` file in the project root with the following variables:

```env
DEBUG=True
SECRET_KEY=your-secret-key-here
DJANGO_ALLOWED_HOSTS=localhost,127.0.0.1
IS_DOCKER=false  # Set to true when running in Docker
```

### 3. Build and run with Docker (Recommended)

```bash
docker-compose up --build -d
```

### 4. Run migrations

```bash
docker-compose exec web python manage.py migrate
```

### 5. Create a superuser (optional)

```bash
docker-compose exec web python manage.py createsuperuser
```

### 6. Access the application

- API: <http://localhost:8000/properties>
- Admin Interface: <http://localhost:8000/admin/>
- PostgreSQL: localhost:5432
- Redis: localhost:6379

## Development Setup (Without Docker)

1. Create and activate a virtual environment:

   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .\.venv\Scripts\activate
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the development server:

   ```bash
   python manage.py runserver
   ```

## Project Structure

```text
alx-backend-caching_property_listings/
├── alx_backend_caching_property_listings/  # Django project settings
├── properties/                             # Property listings app
│   ├── migrations/                         # Database migrations
│   ├── __init__.py
│   ├── admin.py                            # Admin interface configuration
│   ├── apps.py                             # App configuration
│   ├── models.py                           # Database models
│   ├── serializers.py                      # API serializers
│   ├── urls.py                             # URL routing
│   └── views.py                            # API views
├── .env.example                            # Example environment variables
├── .gitignore                              # Git ignore file
├── docker-compose.yml                      # Docker Compose configuration
├── Dockerfile                              # Docker configuration
├── manage.py                               # Django management script
└── requirements.txt                        # Python dependencies
```

## API Endpoints

### Properties

| Endpoint | Method | Description | Cache Duration |
|----------|--------|-------------|----------------|
| `/properties/` | GET | List all properties | 15 minutes |
| `/properties/` | POST | Create a new property | - |
| `/properties/{id}/` | GET | Get property details | - |
| `/properties/{id}/` | PUT | Update a property | - |
| `/properties/{id}/` | DELETE | Delete a property | - |

## Caching Strategy

This project implements a comprehensive caching strategy using Redis with automatic cache invalidation and monitoring:

1. **View-Level Caching**
   - The property list endpoint (`GET /properties/`) is cached for 15 minutes using `@cache_page`
   - Cache is automatically invalidated after the timeout period
   - Provides quick response times for repeated requests to the same URL

2. **Low-Level Caching**
   - Property querysets are cached for 1 hour using Django's low-level cache API
   - Implemented in `properties/utils.py` with `get_all_properties()`
   - Reduces database load by caching the actual queryset results
   - Independent of view caching, providing more granular control

3. **Automatic Cache Invalidation**
   - Uses Django signals to automatically invalidate cache on data changes
   - The `all_properties` cache is cleared when any Property is created, updated, or deleted
   - Ensures data consistency between the cache and database
   - Implemented in `properties/signals.py` with `post_save` and `post_delete` handlers

4. **Cache Monitoring & Metrics**
   - Tracks Redis cache performance with `get_redis_cache_metrics()` in `utils.py`
   - Monitors key metrics:
     - `keyspace_hits`: Number of successful key lookups
     - `keyspace_misses`: Number of failed key lookups
     - `hit_ratio`: Ratio of hits to total requests (hits / (hits + misses))
   - Logs metrics for monitoring and analysis
   - Handles errors gracefully with appropriate fallbacks

5. **Cache Storage**
   - Redis is used as the cache backend
   - View cache keys are automatically generated by Django
   - Queryset cache uses the key `'all_properties'`
   - Cache keys are automatically managed by Django's caching framework

6. **Performance Benefits**
   - Reduces database load by serving cached data
   - Improves response times for frequently accessed data
   - Two-level caching provides both short-term and longer-term caching benefits
   - Automatic invalidation ensures data consistency
   - Metrics provide visibility into cache performance

### Verifying Cache

To verify that caching is working:

1. Make a GET request to `http://localhost:8000/properties/`
2. Check the response headers for `X-From-Cache: 1` on subsequent requests (view cache)
3. The response will be served from cache until either:
   - The 15-minute view cache expires, or
   - Any property is created, updated, or deleted (invalidates the cache)
4. The underlying queryset will be cached for 1 hour or until invalidated by changes

### Cache Headers

The API includes the following cache-related headers:

- `Cache-Control: max-age=900` - Indicates the response can be cached for 15 minutes (900 seconds)
- `Expires` - Shows the exact time when the cache will expire
- `X-From-Cache` - Indicates if the response was served from cache (1) or generated fresh (0)

### Cache Invalidation Events

The cache is automatically invalidated in the following cases:

- When a new property is created
- When an existing property is updated
- When a property is deleted
- After the configured timeout period (15 minutes for view cache, 1 hour for queryset cache)

### Cache Metrics

The application tracks and logs the following Redis cache metrics:

- **Hits**: Number of successful key lookups
- **Misses**: Number of failed key lookups
- **Hit Ratio**: Percentage of successful lookups (hits / (hits + misses))

These metrics are available through the `get_redis_cache_metrics()` function in `utils.py` and are automatically logged for monitoring purposes.

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `DEBUG` | Enable debug mode | `True` |
| `SECRET_KEY` | Django secret key | - |
| `DJANGO_ALLOWED_HOSTS` | Allowed hostnames | `localhost,127.0.0.1` |
| `IS_DOCKER` | Whether running in Docker | `false` |
| `POSTGRES_DB` | PostgreSQL database name | `property_db` |
| `POSTGRES_USER` | PostgreSQL username | `property_user` |
| `POSTGRES_PASSWORD` | PostgreSQL password | `property_password` |

## License

This project is for educational purpose as part of the ALX ProDEV SE Backend Programme.
