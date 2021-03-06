# Generated by Django 3.2 on 2021-04-19 13:22

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.SmallAutoField(primary_key=True, serialize=False, verbose_name='ИД')),
                ('title', models.CharField(max_length=256, verbose_name='Заголовок')),
                ('text', models.TextField(verbose_name='Текст')),
                ('next', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='prev_item', to='kopipasta.item', verbose_name='сдедующий')),
                ('prev', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='next_item', to='kopipasta.item', verbose_name='предыдущий')),
            ],
            options={
                'verbose_name': 'Элемент',
                'verbose_name_plural': 'Элементы',
            },
        ),
    ]
