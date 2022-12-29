# Generated by Django 3.1.3 on 2022-09-19 10:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('Brands', '0001_initial'),
        ('Members', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Buy',
            fields=[
                ('buy_no', models.AutoField(primary_key=True, serialize=False)),
                ('buydate', models.DateTimeField(auto_now_add=True, null=True)),
                ('buynum', models.IntegerField(blank=True, null=True)),
                ('buystatus', models.CharField(blank=True, max_length=20, null=True)),
                ('buy_tot', models.IntegerField(blank=True, null=True)),
                ('d_no', models.ForeignKey(db_column='d_no', default=1, on_delete=django.db.models.deletion.CASCADE, to='Members.delivery')),
                ('p_no', models.ForeignKey(db_column='p_no', on_delete=django.db.models.deletion.CASCADE, to='Members.payment')),
                ('st_no', models.ForeignKey(db_column='st_no', on_delete=django.db.models.deletion.CASCADE, to='Brands.stock')),
                ('u_no', models.ForeignKey(db_column='u_no', on_delete=django.db.models.deletion.CASCADE, to='Members.user')),
            ],
            options={
                'db_table': 'buy',
                'managed': True,
            },
        ),
        migrations.CreateModel(
            name='Basket',
            fields=[
                ('ba_no', models.AutoField(primary_key=True, serialize=False)),
                ('ba_cnt', models.IntegerField(blank=True, null=True)),
                ('st_no', models.ForeignKey(db_column='st_no', on_delete=django.db.models.deletion.CASCADE, to='Brands.stock')),
                ('u_no', models.ForeignKey(db_column='u_no', on_delete=django.db.models.deletion.CASCADE, to='Members.user')),
            ],
            options={
                'db_table': 'basket',
                'managed': True,
            },
        ),
    ]
