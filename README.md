# django-orders

Standalone Django app that owns the ordering feature of the TestCap shop.

## Contents

- `Order` and `OrderItem` models
- Order list/detail and order creation flow
- Admin registration with inline items

## Cross-repo dependency

This app imports `catalog.models.Product` from the separate `django-catalog`
repo and references it with a foreign key. `django-catalog` must be installed
first (the project's `make setup` does this in the right order). The dependency
is one-way: catalog never imports orders.

## URLs

Included by `django-core1` at `/orders/`:

- `/orders/` - order list
- `/orders/new/` - create an order for an active catalog product
- `/orders/<pk>/` - order detail with line items and total

## Install (development)

```bash
pip install -e .
```

## Tests

Run from the `django-core1` repo:

```bash
python manage.py test orders
```
