from __future__ import annotations

from decimal import Decimal
from datetime import timedelta

from django.contrib.auth.hashers import make_password
from django.db import migrations
from django.utils import timezone


PASSWORD = "pass123"


def seed_demo_data(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Pet = apps.get_model("pets", "Pet")
    Product = apps.get_model("products", "Product")
    StockMovement = apps.get_model("inventory", "StockMovement")
    Order = apps.get_model("orders", "Order")
    Appointment = apps.get_model("appointments", "Appointment")
    Payment = apps.get_model("payments", "Payment")

    # Avoid duplicating demo data
    if Order.objects.exists() or Appointment.objects.exists():
        return

    staff_users = (
        ("admin", True, True, "admin@example.com"),
        ("piero.o", False, True, "piero.o@example.com"),
        ("pieroyo", False, True, "pieroyo@example.com"),
        ("testuser", False, True, "testuser@example.com"),
    )

    regular_users = {
        "juan.perez": {
            "email": "juan.perez@example.com",
            "pets": (
                ("Max", "Dog", 5),
                ("Luna", "Cat", 3),
            ),
        },
        "maria.garcia": {
            "email": "maria.garcia@example.com",
            "pets": (
                ("Rocky", "Dog", 4),
            ),
        },
        "carlos.lopez": {
            "email": "carlos.lopez@example.com",
            "pets": (
                ("Michi", "Cat", 2),
                ("Toby", "Dog", 6),
            ),
        },
    }

    products_seed = (
        ("Alimento Premium", "Alimento balanceado para mascotas", Decimal("89.90"), 50),
        ("Juguete Dental", "Mordedor que cuida los dientes", Decimal("29.50"), 30),
        ("Vitamina Omega", "Suplemento para pelo brillante", Decimal("59.00"), 20),
    )

    # Create or update staff users
    for username, is_superuser, is_staff, email in staff_users:
        user, _ = User.objects.get_or_create(username=username)
        user.email = email
        user.is_staff = is_staff or is_superuser
        user.is_superuser = is_superuser
        user.password = make_password(PASSWORD)
        user.save()

    # Create or update regular users and their pets
    for username, info in regular_users.items():
        user, _ = User.objects.get_or_create(username=username)
        user.email = info["email"]
        user.is_staff = False
        user.is_superuser = False
        user.password = make_password(PASSWORD)
        user.save()

        Pet.objects.filter(owner=user).delete()
        for name, species, age in info["pets"]:
            Pet.objects.create(owner=user, name=name, species=species, age=age)

    # Products + initial stock movements
    product_objects = []
    for name, description, price, stock in products_seed:
        product, _ = Product.objects.get_or_create(name=name, defaults={
            "description": description,
            "price": price,
            "stock": 0,
        })
        product.description = description
        product.price = price
        product.save()
        product_objects.append((product, stock))

    for product, stock in product_objects:
        StockMovement.objects.create(
            product=product,
            movement_type="ADJUSTMENT",
            quantity=stock,
            reason="Carga inicial de demostración",
            user=None,
        )

    now = timezone.now()

    appointment_plan = {
        "juan.perez": 5,
        "maria.garcia": 2,
        "carlos.lopez": 2,
    }

    for username, count in appointment_plan.items():
        user = User.objects.get(username=username)
        pets = list(Pet.objects.filter(owner=user))
        if not pets:
            continue
        Appointment.objects.filter(owner=user).delete()
        for idx in range(count):
            pet = pets[idx % len(pets)]
            Appointment.objects.create(
                owner=user,
                pet=pet,
                scheduled_at=now + timedelta(days=idx + 1),
                reason=f"Consulta de seguimiento #{idx + 1}",
                status="scheduled" if idx < count - 1 else "completed",
                notes="Cita generada para datos de demostración",
            )

    order_plan = {
        "juan.perez": [
            (Decimal("120.50"), "completed"),
            (Decimal("89.90"), "completed"),
            (Decimal("49.99"), "pending"),
            (Decimal("210.00"), "completed"),
            (Decimal("35.75"), "completed"),
            (Decimal("18.20"), "cancelled"),
        ],
        "maria.garcia": [
            (Decimal("65.00"), "completed"),
            (Decimal("32.45"), "completed"),
            (Decimal("149.90"), "pending"),
            (Decimal("22.00"), "completed"),
        ],
        "carlos.lopez": [
            (Decimal("78.10"), "completed"),
            (Decimal("99.99"), "completed"),
            (Decimal("45.50"), "pending"),
            (Decimal("60.00"), "completed"),
            (Decimal("55.75"), "completed"),
            (Decimal("120.00"), "completed"),
        ],
    }

    Payment.objects.filter(transaction_id__startswith="TXN-SEED-").delete()
    usernames = list(order_plan.keys())
    Order.objects.filter(customer__username__in=usernames).delete()

    payment_methods = ["CARD", "CASH", "TRANSFER", "YAPE"]

    for username, orders in order_plan.items():
        user = User.objects.get(username=username)
        for idx, (total, status) in enumerate(orders, start=1):
            order = Order.objects.create(
                customer=user,
                total=total,
                status=status,
                notes="Pedido generado para datos de demostración",
            )
            Payment.objects.create(
                user=user,
                amount=total,
                payment_method=payment_methods[idx % len(payment_methods)],
                status="COMPLETED" if status == "completed" else "PENDING",
                transaction_id=f"TXN-SEED-{username}-{idx}",
                notes=f"Pago ligado al pedido #{order.pk}",
            )


def purge_demo_data(apps, schema_editor):
    User = apps.get_model("auth", "User")
    Order = apps.get_model("orders", "Order")
    Appointment = apps.get_model("appointments", "Appointment")
    Payment = apps.get_model("payments", "Payment")

    usernames = ["admin", "piero.o", "pieroyo", "testuser", "juan.perez", "maria.garcia", "carlos.lopez"]
    Payment.objects.filter(transaction_id__startswith="TXN-SEED-").delete()
    Order.objects.filter(customer__username__in=usernames).delete()
    Appointment.objects.filter(owner__username__in=usernames).delete()
    User.objects.filter(username__in=usernames).delete()


class Migration(migrations.Migration):

    dependencies = [
        ("orders", "0001_initial"),
        ("appointments", "0001_initial"),
        ("payments", "0001_initial"),
        ("inventory", "0001_initial"),
        ("products", "0001_initial"),
        ("pets", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(seed_demo_data, purge_demo_data),
    ]
