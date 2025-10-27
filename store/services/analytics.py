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


def get_category_children_counts():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT parent.id, parent.name, COUNT(child.id) AS children_count
            FROM store_category parent
            LEFT JOIN store_category child ON child.parent_id = parent.id
            GROUP BY parent.id, parent.name
        """
        )
        return [
            {"id": row[0], "name": row[1], "children_count": row[2]}
            for row in cursor.fetchall()
        ]
