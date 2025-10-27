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


def get_top_5_products_last_month():
    with connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT
              n.name AS product_name,
              COALESCE(top.name, '—') AS top_level_category,
              SUM(oi.quantity) AS total_sold
            FROM store_orderitem oi
            JOIN store_order o ON o.id = oi.order_id
            JOIN store_nomenclature n ON n.id = oi.nomenclature_id
            LEFT JOIN store_category c ON c.id = n.category_id
            LEFT JOIN store_category top ON c.parent_id IS NULL AND top.id = c.id
            WHERE o.created_at >= CURRENT_DATE - INTERVAL '1 month'
            GROUP BY n.name, top.name
            ORDER BY total_sold DESC
            LIMIT 5;
        """
        )
        return [
            {
                "product_name": row[0],
                "top_level_category": row[1],
                "total_sold": row[2],
            }
            for row in cursor.fetchall()
        ]


def refresh_top5_matview():
    with connection.cursor() as cursor:
        cursor.execute("REFRESH MATERIALIZED VIEW top_5_products_last_month_matview")


def get_top5_products_from_matview():
    with connection.cursor() as cursor:
        cursor.execute("SELECT * FROM top_5_products_last_month_matview")
        return [
            {
                "product_name": row[0],
                "top_level_category": row[1],
                "total_sold": row[2],
            }
            for row in cursor.fetchall()
        ]
