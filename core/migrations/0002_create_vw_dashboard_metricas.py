from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE VIEW IF NOT EXISTS vw_dashboard_metricas AS
            SELECT 
                1 AS id,
                COUNT(*) AS total_ecopontos
            FROM core_ecoponto;
            """,
            reverse_sql="DROP VIEW IF EXISTS vw_dashboard_metricas;",
        )
    ]
