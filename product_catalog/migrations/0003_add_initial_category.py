from django.db import migrations

def add_initial_category(apps, schema_editor):
    ProductCategory = apps.get_model('product_catalog', 'ProductCategory')
    ProductCategory.objects.create(
        name="غذائية",
        description="المنتجات الغذائية"
    )

def remove_initial_category(apps, schema_editor):
    ProductCategory = apps.get_model('product_catalog', 'ProductCategory')
    ProductCategory.objects.filter(name="غذائية").delete()

class Migration(migrations.Migration):

    dependencies = [
        ('product_catalog', '0002_productcategory'),
    ]

    operations = [
        migrations.RunPython(add_initial_category, remove_initial_category),
    ] 