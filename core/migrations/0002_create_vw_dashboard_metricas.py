from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("core", "0001_initial"),
    ]

    operations = [
        migrations.RunSQL(
            sql="""
            CREATE OR REPLACE VIEW vw_dashboard_metricas AS
            SELECT 
                1 AS id,
                0 AS total_ecopontos,
                0 AS total_coletas,
                0 AS total_usuarios,
                0.0 AS total_kg_reciclados;
            """,
            reverse_sql="DROP VIEW IF EXISTS vw_dashboard_metricas;",
        )
    ]
