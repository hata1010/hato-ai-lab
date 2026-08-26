from django.db import migrations


class Migration(migrations.Migration):
    """Elimina una columna residual que ya no pertenece al modelo Metrica.

    La columna motor_referencia existe en algunas bases heredadas, pero no
    figura en el modelo actual ni en las migraciones 0001-0004. Esta migracion
    normaliza el esquema PostgreSQL de esas instalaciones sin cambiar el
    estado Django del modelo.
    """

    dependencies = [
        ("produccion", "0004_metrica_finca_alter_metrica_codigo_and_more"),
    ]

    operations = [
        migrations.RunSQL(
            sql="ALTER TABLE produccion_metrica DROP COLUMN IF EXISTS motor_referencia;",
            reverse_sql=migrations.RunSQL.noop,
        ),
    ]
