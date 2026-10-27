from django.db import models
from django.utils import timezone


class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    city = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=14, decimal_places=2)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "sql_lab_department"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Employee(models.Model):
    department = models.ForeignKey(
        Department,
        on_delete=models.CASCADE,
        related_name="employees",
    )
    name = models.CharField(max_length=150)
    job_title = models.CharField(max_length=100)
    salary = models.DecimalField(max_digits=12, decimal_places=2)
    active = models.BooleanField(default=True)
    hired_at = models.DateField()

    class Meta:
        db_table = "sql_lab_employee"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["department"]),
            models.Index(fields=["active"]),
            models.Index(fields=["salary"]),
        ]

    def __str__(self):
        return self.name


class Customer(models.Model):
    class Segment(models.TextChoices):
        BRONZE = "bronze", "Bronze"
        SILVER = "silver", "Silver"
        GOLD = "gold", "Gold"
        VIP = "vip", "VIP"

    name = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    region = models.CharField(max_length=100)
    segment = models.CharField(
        max_length=20,
        choices=Segment.choices,
        default=Segment.BRONZE,
    )
    blocked = models.BooleanField(default=False)
    active = models.BooleanField(default=True)

    account_manager = models.ForeignKey(
        Employee,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="managed_customers",
    )

    created_at = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(null=True, blank=True)

    class Meta:
        db_table = "sql_lab_customer"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["region"]),
            models.Index(fields=["segment"]),
            models.Index(fields=["blocked"]),
        ]

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "sql_lab_category"
        ordering = ["id"]

    def __str__(self):
        return self.name


class Product(models.Model):
    category = models.ForeignKey(
        Category,
        on_delete=models.CASCADE,
        related_name="products",
    )
    name = models.CharField(max_length=200)
    sku = models.CharField(max_length=50, unique=True)
    price = models.DecimalField(max_digits=12, decimal_places=2)
    cost = models.DecimalField(max_digits=12, decimal_places=2)
    stock = models.PositiveIntegerField(default=0)
    active = models.BooleanField(default=True)

    class Meta:
        db_table = "sql_lab_product"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["active"]),
            models.Index(fields=["price"]),
        ]

    def __str__(self):
        return self.name


class Order(models.Model):
    class Status(models.TextChoices):
        PENDING = "pending", "Pending"
        PAID = "paid", "Paid"
        SHIPPED = "shipped", "Shipped"
        CANCELLED = "cancelled", "Cancelled"
        REFUNDED = "refunded", "Refunded"

    customer = models.ForeignKey(
        Customer,
        on_delete=models.CASCADE,
        related_name="orders",
    )
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
    )
    created_at = models.DateTimeField(default=timezone.now)
    discount_percent = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        default=0,
    )

    class Meta:
        db_table = "sql_lab_order"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["customer"]),
            models.Index(fields=["status"]),
            models.Index(fields=["created_at"]),
        ]

    def __str__(self):
        return f"Order #{self.pk}"


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name="items",
    )
    product = models.ForeignKey(
        Product,
        on_delete=models.CASCADE,
        related_name="order_items",
    )
    quantity = models.PositiveIntegerField()
    unit_price = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )

    class Meta:
        db_table = "sql_lab_order_item"
        ordering = ["id"]
        constraints = [
            models.UniqueConstraint(
                fields=["order", "product"],
                name="unique_sql_lab_order_product",
            ),
        ]
        indexes = [
            models.Index(fields=["order"]),
            models.Index(fields=["product"]),
        ]

    def __str__(self):
        return f"Order #{self.order_id}, Product #{self.product_id}"


class Project(models.Model):
    class Status(models.TextChoices):
        PLANNED = "planned", "Planned"
        ACTIVE = "active", "Active"
        DONE = "done", "Done"
        CANCELLED = "cancelled", "Cancelled"

    employee = models.ForeignKey(
        Employee,
        on_delete=models.CASCADE,
        related_name="projects",
    )
    name = models.CharField(max_length=200)
    status = models.CharField(
        max_length=20,
        choices=Status.choices,
    )
    budget = models.DecimalField(
        max_digits=12,
        decimal_places=2,
    )
    started_at = models.DateField()

    class Meta:
        db_table = "sql_lab_project"
        ordering = ["id"]
        indexes = [
            models.Index(fields=["employee"]),
            models.Index(fields=["status"]),
        ]

    def __str__(self):
        return self.name
