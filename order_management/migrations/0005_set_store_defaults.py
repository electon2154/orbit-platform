from django.db import migrations

def set_store_defaults(apps, schema_editor):
    Order = apps.get_model('order_management', 'Order')
    for order in Order.objects.all():
        # Get store information from the customer
        customer = order.customer
        order.store_name = customer.store_name
        order.store_location = customer.location
        order.store_city = customer.city
        order.store_phone = customer.phone
        order.save()

class Migration(migrations.Migration):
    dependencies = [
        ('order_management', '0004_order_store_city_order_store_location_and_more'),
    ]

    operations = [
        migrations.RunPython(set_store_defaults),
    ]