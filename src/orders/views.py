from django.shortcuts import get_object_or_404, redirect, render

from .forms import OrderCreateForm
from .models import Order, OrderItem


def order_list(request):
    orders = Order.objects.select_related("customer").prefetch_related("items")
    return render(request, "orders/order_list.html", {"orders": orders})


def order_detail(request, pk):
    order = get_object_or_404(
        Order.objects.select_related("customer").prefetch_related("items__product"),
        pk=pk,
    )
    return render(request, "orders/order_detail.html", {"order": order})


def order_create(request):
    form = OrderCreateForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        product = form.cleaned_data["product"]
        quantity = form.cleaned_data["quantity"]
        customer = request.user if request.user.is_authenticated else None
        order = Order.objects.create(customer=customer)
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            unit_price=product.price,
        )
        return redirect("orders:order_detail", pk=order.pk)
    return render(request, "orders/order_create.html", {"form": form})
