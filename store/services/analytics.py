from django.db import connection


def get_clients_with_total_sum():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT c.name, SUM(oi.quantity * n.price) AS total_sum
            FROM store_client c
            JOIN store_order o ON o.client_id = c.id
            JOIN store_orderitem oi ON oi.order_id = o.id
            JOIN store_nomenclature n ON n.id = oi.nomenclature_id
            GROUP BY c.name
        """
        )
        return cursor.fetchall()
