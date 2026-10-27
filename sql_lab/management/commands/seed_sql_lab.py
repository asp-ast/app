import random
from datetime import date, timedelta
from decimal import Decimal

from django.core.management.base import BaseCommand
from django.db import transaction
from django.utils import timezone

from sql_lab.models import (
    Category,
    Customer,
    Department,
    Employee,
    Order,
    OrderItem,
    Product,
    Project,
)


class Command(BaseCommand):
    help = "Создаёт большой набор тестовых данных для практики SQL."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="Удалить существующие данные перед заполнением.",
        )

    def handle(self, *args, **options):
        random.seed(42)

        if options["clear"]:
            self.clear_data()

        with transaction.atomic():
            departments = self.create_departments()
            employees = self.create_employees(departments)
            customers = self.create_customers(employees)
            categories = self.create_categories()
            products = self.create_products(categories)
            orders = self.create_orders(customers)
            order_items = self.create_order_items(orders, products)
            projects = self.create_projects(employees)

        self.stdout.write(self.style.SUCCESS("Данные успешно созданы."))
        self.stdout.write(f"Departments: {len(departments)}")
        self.stdout.write(f"Employees:   {len(employees)}")
        self.stdout.write(f"Customers:   {len(customers)}")
        self.stdout.write(f"Categories:  {len(categories)}")
        self.stdout.write(f"Products:    {len(products)}")
        self.stdout.write(f"Orders:      {len(orders)}")
        self.stdout.write(f"OrderItems:  {len(order_items)}")
        self.stdout.write(f"Projects:    {len(projects)}")

    def clear_data(self):
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Project.objects.all().delete()
        Customer.objects.all().delete()
        Product.objects.all().delete()
        Category.objects.all().delete()
        Employee.objects.all().delete()
        Department.objects.all().delete()

        self.stdout.write("Старые данные удалены.")

    def create_departments(self):
        department_data = [
            ("Engineering", "Tallinn", "900000"),
            ("Sales", "Tallinn", "650000"),
            ("Marketing", "Tartu", "420000"),
            ("Finance", "Tallinn", "520000"),
            ("HR", "Tartu", "300000"),
            ("Support", "Narva", "380000"),
            ("Analytics", "Tallinn", "610000"),
            ("Logistics", "Pärnu", "470000"),
            ("Product", "Tallinn", "750000"),
            ("Security", "Tartu", "480000"),
            ("Legal", "Tallinn", "350000"),
            ("Operations", "Pärnu", "560000"),
        ]

        departments = [
            Department(
                name=name,
                city=city,
                budget=Decimal(budget),
                active=True,
            )
            for name, city, budget in department_data
        ]

        return list(Department.objects.bulk_create(departments))

    def create_employees(self, departments):
        # В разных отделах разное количество сотрудников.
        # Это важно для GROUP BY / HAVING.
        employee_counts = [
            18,
            14,
            9,
            12,
            5,
            22,
            16,
            7,
            20,
            11,
            4,
            13,
        ]

        job_titles = [
            "Junior Developer",
            "Developer",
            "Senior Developer",
            "Team Lead",
            "Analyst",
            "Senior Analyst",
            "Manager",
            "Specialist",
        ]

        employees = []
        employee_number = 1

        today = date.today()

        for department, count in zip(departments, employee_counts):
            for _ in range(count):
                # Делаем зарплаты намеренно неоднородными.
                # В одних отделах средняя зарплата будет заметно выше.
                base_salary = {
                    "Engineering": 115000,
                    "Sales": 85000,
                    "Marketing": 78000,
                    "Finance": 105000,
                    "HR": 65000,
                    "Support": 60000,
                    "Analytics": 125000,
                    "Logistics": 70000,
                    "Product": 110000,
                    "Security": 130000,
                    "Legal": 120000,
                    "Operations": 82000,
                }[department.name]

                salary = Decimal(
                    base_salary + random.randint(-25000, 35000)
                )

                salary = max(salary, Decimal("40000"))

                hired_at = today - timedelta(
                    days=random.randint(60, 3200)
                )

                employees.append(
                    Employee(
                        department=department,
                        name=f"Employee {employee_number:03d}",
                        job_title=random.choice(job_titles),
                        salary=salary,
                        active=random.random() > 0.12,
                        hired_at=hired_at,
                    )
                )

                employee_number += 1

        return list(Employee.objects.bulk_create(employees))

    def create_customers(self, employees):
        regions = [
            "Estonia",
            "Finland",
            "Latvia",
            "Lithuania",
            "Germany",
            "Sweden",
            "Poland",
            "Denmark",
        ]

        segments = [
            "bronze",
            "silver",
            "gold",
            "vip",
        ]

        customers = []
        now = timezone.now()

        for number in range(1, 61):
            created_at = now - timedelta(
                days=random.randint(30, 1400),
                hours=random.randint(0, 23),
            )

            # Нам нужны и свежие, и давно не заходившие пользователи.
            login_mode = number % 7

            if login_mode == 0:
                last_login = None
            elif login_mode in (1, 2):
                last_login = now - timedelta(
                    days=random.randint(400, 1000)
                )
            else:
                last_login = now - timedelta(
                    days=random.randint(1, 180)
                )

            customers.append(
                Customer(
                    name=f"Customer {number:03d}",
                    email=f"customer{number:03d}@example.com",
                    region=random.choice(regions),
                    segment=random.choice(segments),
                    blocked=number in {
                        3,
                        7,
                        12,
                        19,
                        27,
                        34,
                        41,
                        48,
                        55,
                    },
                    active=number not in {11, 23, 37, 52},
                    account_manager=random.choice(employees),
                    created_at=created_at,
                    last_login=last_login,
                )
            )

        return list(Customer.objects.bulk_create(customers))

    def create_categories(self):
        category_names = [
            "Laptops",
            "Phones",
            "Monitors",
            "Keyboards",
            "Mice",
            "Headphones",
            "Cameras",
            "Networking",
            "Storage",
            "Accessories",
            "Printers",
            "Tablets",
        ]

        categories = [
            Category(
                name=name,
                active=name not in {"Printers"},
            )
            for name in category_names
        ]

        return list(Category.objects.bulk_create(categories))

    def create_products(self, categories):
        products = []

        product_number = 1

        for category in categories:
            product_count = 8

            for _ in range(product_count):
                price = Decimal(
                    random.randint(25, 2200)
                ).quantize(Decimal("0.01"))

                cost = (
                    price * Decimal(str(random.uniform(0.45, 0.82)))
                ).quantize(Decimal("0.01"))

                products.append(
                    Product(
                        category=category,
                        name=f"{category.name} Product {product_number:03d}",
                        sku=f"SKU-{product_number:04d}",
                        price=price,
                        cost=cost,
                        stock=random.randint(0, 150),
                        active=random.random() > 0.10,
                    )
                )

                product_number += 1

        return list(Product.objects.bulk_create(products))

    def create_orders(self, customers):
        """
        Намеренно задаём очень разные количества заказов для клиентов.

        Первые несколько клиентов не имеют заказов вообще.
        Есть клиенты с 1-5 заказами.
        Есть клиенты с десятками заказов.

        Это позволяет тренировать:
        - COUNT
        - HAVING COUNT
        - LEFT JOIN
        - NOT EXISTS
        - DELETE по агрегированным условиям
        """

        order_counts = [
            0,
            0,
            0,
            0,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            10,
            12,
            15,
            18,
            20,
            22,
            25,
            28,
            3,
            4,
            5,
            6,
            8,
            9,
            10,
            11,
            12,
            13,
            14,
            15,
            16,
            17,
            18,
            19,
            20,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
            11,
            12,
            14,
            16,
            1,
            2,
            3,
            4,
            5,
            6,
            7,
            8,
            9,
            10,
        ]

        statuses = [
            "pending",
            "paid",
            "shipped",
            "cancelled",
            "refunded",
        ]

        now = timezone.now()
        orders = []

        for customer, count in zip(customers, order_counts):
            for _ in range(count):
                # Нам нужны старые и новые заказы.
                age_days = random.choice(
                    [
                        random.randint(0, 30),
                        random.randint(31, 180),
                        random.randint(181, 700),
                        random.randint(701, 1200),
                    ]
                )

                created_at = now - timedelta(
                    days=age_days,
                    hours=random.randint(0, 23),
                    minutes=random.randint(0, 59),
                )

                orders.append(
                    Order(
                        customer=customer,
                        status=random.choice(statuses),
                        created_at=created_at,
                        discount_percent=Decimal(
                            random.choice(
                                ["0", "0", "0", "5", "10", "15", "20"]
                            )
                        ),
                    )
                )

        return list(Order.objects.bulk_create(orders))

    def create_order_items(self, orders, products):
        """
        Последние 10 товаров намеренно никогда не продаются.
        Это полезно для NOT EXISTS / LEFT JOIN задач.

        Остальные товары случайным образом распределяем по заказам.
        """

        products_for_sales = products[:-10]

        order_items = []

        for order in orders:
            item_count = random.randint(1, 5)

            selected_products = random.sample(
                products_for_sales,
                item_count,
            )

            for product in selected_products:
                quantity = random.randint(1, 6)

                order_items.append(
                    OrderItem(
                        order=order,
                        product=product,
                        quantity=quantity,
                        unit_price=product.price,
                    )
                )

        return list(
            OrderItem.objects.bulk_create(
                order_items,
                batch_size=1000,
            )
        )

    def create_projects(self, employees):
        project_names = [
            "Website Redesign",
            "Mobile App",
            "Data Warehouse",
            "Customer Portal",
            "Security Audit",
            "Payment Integration",
            "CRM Migration",
            "Analytics Platform",
            "Cloud Migration",
            "Internal Automation",
            "Monitoring System",
            "Documentation",
            "Performance Optimization",
            "Recommendation Engine",
            "New Sales Dashboard",
        ]

        statuses = [
            "planned",
            "active",
            "done",
            "cancelled",
        ]

        today = date.today()
        projects = []

        for number in range(1, 221):
            employee = random.choice(employees)

            status = random.choice(statuses)

            # Специально создаём много активных проектов,
            # но часть сотрудников оставляем без активных проектов.
            if number % 11 == 0:
                status = "active"

            projects.append(
                Project(
                    employee=employee,
                    name=f"{random.choice(project_names)} #{number:03d}",
                    status=status,
                    budget=Decimal(
                        random.randint(5000, 250000)
                    ),
                    started_at=today - timedelta(
                        days=random.randint(10, 1000)
                    ),
                )
            )

        return list(
            Project.objects.bulk_create(
                projects,
                batch_size=1000,
            )
        )
