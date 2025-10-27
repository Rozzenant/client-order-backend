from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("store", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
                CREATE MATERIALIZED VIEW top_5_products_last_month_matview AS
                SELECT
                    n.name AS product_name,
                    COALESCE(parent.name, c.name) AS top_level_category,
                    SUM(oi.quantity) AS total_sold
                FROM store_orderitem oi
                JOIN store_order o ON o.id = oi.order_id
                JOIN store_nomenclature n ON n.id = oi.nomenclature_id
                LEFT JOIN store_category c ON c.id = n.category_id
                LEFT JOIN store_category parent ON c.parent_id = parent.id
                WHERE o.created_at >= CURRENT_DATE - INTERVAL '1 month'
                GROUP BY n.name, parent.name, c.name
                ORDER BY total_sold DESC
                LIMIT 5
            """,
            reverse_sql="DROP MATERIALIZED VIEW IF EXISTS \
            top_5_products_last_month_matview",
        )
    ]
