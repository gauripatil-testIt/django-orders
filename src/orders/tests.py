from decimal import Decimal

from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from catalog.models import Category, Product

from .models import Order, OrderItem


class OrderFlowTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(name="Books", slug="books")
        self.product = Product.objects.create(
            category=self.category,
            name="Clean Code",
            slug="clean-code",
            price=Decimal("39.99"),
        )
        self.user = get_user_model().objects.create_user(
            username="buyer", password="secret123"
        )

    def test_create_order_from_catalog_product(self):
        response = self.client.post(
            reverse("orders:order_create"),
            {"product": self.product.pk, "quantity": 2},
        )
        order = Order.objects.get()
        self.assertRedirects(response, order.get_absolute_url())
        self.assertEqual(order.items.count(), 1)
        self.assertEqual(order.total, Decimal("79.98"))

    def test_order_detail_renders_items(self):
        order = Order.objects.create(customer=self.user)
        OrderItem.objects.create(
            order=order,
            product=self.product,
            quantity=1,
            unit_price=self.product.price,
        )
        response = self.client.get(order.get_absolute_url())
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Clean Code")
        self.assertContains(response, "39.99")
