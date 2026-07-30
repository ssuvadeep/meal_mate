from django.db import migrations, models
import django.db.models.deletion


def clear_old_cart_items(apps, schema_editor):
    CartItem = apps.get_model('delivery', 'CartItem')
    CartItem.objects.all().delete()


class Migration(migrations.Migration):

    dependencies = [
        ('delivery', '0006_alter_restaurant_picture_cartitem'),
    ]

    operations = [
        migrations.RunPython(clear_old_cart_items, migrations.RunPython.noop),
        migrations.AddField(
            model_name='cartitem',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AlterField(
            model_name='cartitem',
            name='Customer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='delivery.customer'),
        ),
        migrations.RemoveField(
            model_name='cartitem',
            name='MenuItem',
        ),
        migrations.AddField(
            model_name='cartitem',
            name='MenuItem',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='cart_items', to='delivery.menuitem'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='cartitem',
            unique_together={('Customer', 'MenuItem')},
        ),
    ]