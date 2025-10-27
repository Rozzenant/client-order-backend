from django.core.management.base import BaseCommand
from store.models import Client, Category, Nomenclature, Order, OrderItem
from faker import Faker
import random

fake = Faker()


class Command(BaseCommand):
    help = "Генерирует мок‑данные: категории, товары, клиентов, заказы"

    def add_arguments(self, parser):
        parser.add_argument(
            "--categories", type=int, default=5, help="Количество корневых категорий"
        )
        parser.add_argument(
            "--clients", type=int, default=10, help="Количество клиентов"
        )
        parser.add_argument(
            "--products", type=int, default=50, help="Количество товаров"
        )

    def handle(self, *args, **options):
        self.stdout.write("Очищаю базу данных...")
        OrderItem.objects.all().delete()
        Order.objects.all().delete()
        Nomenclature.objects.all().delete()
        Category.objects.all().delete()
        Client.objects.all().delete()

        # Генерация категорий с произвольной вложенностью
        self.stdout.write("Генерирую категории...")

        def generate_category_tree(parent=None, depth=0, max_depth=4):
            """Рекурсивно создаёт дерево категорий случайной глубины"""
            if depth > max_depth:
                return []

            categories = []
            num_children = random.randint(1, 3)
            for _ in range(num_children):
                category = Category.objects.create(
                    name=fake.word(),
                    parent=parent,
                )
                categories.append(category)
                # случайно решаем, будет ли ветвление дальше
                if random.choice([True, False]):
                    categories += generate_category_tree(
                        parent=category, depth=depth + 1, max_depth=max_depth
                    )
            return categories

        root_categories = [
            Category.objects.create(name=fake.word())
            for _ in range(options["categories"])
        ]
        all_categories = []
        for cat in root_categories:
            all_categories += generate_category_tree(parent=cat)

        all_categories += root_categories
        self.stdout.write(f"Категорий создано: {len(all_categories)}")

        # Клиенты
        self.stdout.write("Создаю клиентов...")
        clients = [
            Client.objects.create(name=fake.company(), address=fake.address())
            for _ in range(options["clients"])
        ]
        self.stdout.write(f"Клиентов создано: {len(clients)}")

        # Номенклатура
        self.stdout.write("Создаю товары...")
        nomenclatures = []
        for _ in range(options["products"]):
            n = Nomenclature.objects.create(
                name=fake.word(),
                quantity=random.randint(10, 100),
                price=round(random.uniform(10, 5000), 2),
                category=random.choice(all_categories),
            )
            nomenclatures.append(n)
        self.stdout.write(f"Товаров создано: {len(nomenclatures)}")

        # Заказы
        self.stdout.write("Создаю заказы и позиции...")
        total_orders = 0
        total_items = 0
        for client in clients:
            for _ in range(random.randint(1, 3)):
                order = Order.objects.create(client=client)
                total_orders += 1
                items = random.sample(nomenclatures, k=random.randint(1, 5))
                for item in items:
                    qty = random.randint(1, 5)
                    OrderItem.objects.create(
                        order=order, nomenclature=item, quantity=qty
                    )
                    total_items += 1

        self.stdout.write(f"Заказов создано: {total_orders}, позиций: {total_items}")
        self.stdout.write(self.style.SUCCESS("Моки успешно загружены!"))
