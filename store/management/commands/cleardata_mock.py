from django.core.management.base import BaseCommand
from store.models import Client, Category, Nomenclature, Order, OrderItem


class Command(BaseCommand):
    help = "Удаляет все тестовые данные из базы (созданные мок-командой)"

    def add_arguments(self, parser):
        parser.add_argument(
            "--confirm",
            action="store_true",
            help="Подтвердить удаление без запроса",
        )

    def handle(self, *args, **options):
        confirm = options["confirm"]

        if not confirm:
            self.stdout.write(
                self.style.WARNING("Это удалит ВСЕ тестовые данные из БД!")
            )
            answer = (
                input("Вы уверены, что хотите продолжить? (yes/no): ").strip().lower()
            )
            if answer not in ("y", "yes"):
                self.stdout.write(self.style.ERROR("Операция отменена"))
                return

        self.stdout.write("Удаляю данные...")

        # сначала дочерние, потом родительские
        deleted = {}
        for model in [OrderItem, Order, Nomenclature, Category, Client]:
            count, _ = model.objects.all().delete()
            deleted[model.__name__] = count

        self.stdout.write("Удаление завершено!\n")
        for name, count in deleted.items():
            self.stdout.write(f"  - {name}: {count} записей удалено")

        self.stdout.write(self.style.SUCCESS("Все тестовые данные успешно очищены"))
