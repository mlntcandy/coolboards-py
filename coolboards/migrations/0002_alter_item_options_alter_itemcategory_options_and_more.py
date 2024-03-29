# Generated by Django 4.2.2 on 2024-01-14 08:06

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import simple_history.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('coolboards', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='item',
            options={'verbose_name': 'Товар', 'verbose_name_plural': 'Товары'},
        ),
        migrations.AlterModelOptions(
            name='itemcategory',
            options={'verbose_name': 'Категория товара', 'verbose_name_plural': 'Категории товаров'},
        ),
        migrations.AlterModelOptions(
            name='itemphoto',
            options={'verbose_name': 'Фотография товара', 'verbose_name_plural': 'Фотографии товаров'},
        ),
        migrations.AlterModelOptions(
            name='manufacturer',
            options={'verbose_name': 'Производитель', 'verbose_name_plural': 'Производители'},
        ),
        migrations.AlterModelOptions(
            name='order',
            options={'verbose_name': 'Заказ', 'verbose_name_plural': 'Заказы'},
        ),
        migrations.AlterModelOptions(
            name='orderitem',
            options={'verbose_name': 'Товар в заказе', 'verbose_name_plural': 'Товары в заказе'},
        ),
        migrations.AlterModelOptions(
            name='review',
            options={'verbose_name': 'Отзыв', 'verbose_name_plural': 'Отзывы'},
        ),
        migrations.AlterField(
            model_name='item',
            name='category',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coolboards.itemcategory', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='item',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='item',
            name='description',
            field=models.TextField(null=True, verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='item',
            name='discount',
            field=models.DecimalField(decimal_places=2, max_digits=9, null=True, verbose_name='Скидка'),
        ),
        migrations.AlterField(
            model_name='item',
            name='manufacturer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='coolboards.manufacturer', verbose_name='Производитель'),
        ),
        migrations.AlterField(
            model_name='item',
            name='name',
            field=models.TextField(verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='item',
            name='new',
            field=models.BooleanField(verbose_name='Новинка'),
        ),
        migrations.AlterField(
            model_name='item',
            name='photos',
            field=models.ManyToManyField(blank=True, to='coolboards.itemphoto', verbose_name='Фотографии'),
        ),
        migrations.AlterField(
            model_name='item',
            name='price',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена'),
        ),
        migrations.AlterField(
            model_name='item',
            name='stock',
            field=models.PositiveIntegerField(verbose_name='Количество на складе'),
        ),
        migrations.AlterField(
            model_name='itemcategory',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='itemcategory',
            name='name',
            field=models.TextField(verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='itemcategory',
            name='photo',
            field=models.ImageField(null=True, upload_to='categories/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='itemcategory',
            name='slug',
            field=models.SlugField(verbose_name='Слаг'),
        ),
        migrations.AlterField(
            model_name='itemphoto',
            name='added_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления'),
        ),
        migrations.AlterField(
            model_name='itemphoto',
            name='main',
            field=models.BooleanField(default=False, verbose_name='Основное'),
        ),
        migrations.AlterField(
            model_name='itemphoto',
            name='name',
            field=models.CharField(max_length=255, null=True, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='itemphoto',
            name='photo',
            field=models.ImageField(upload_to='item_photos/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='description',
            field=models.TextField(verbose_name='Описание'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='name',
            field=models.TextField(verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='photo',
            field=models.ImageField(null=True, upload_to='manufacturers/', verbose_name='Фото'),
        ),
        migrations.AlterField(
            model_name='manufacturer',
            name='slug',
            field=models.SlugField(verbose_name='Слаг'),
        ),
        migrations.AlterField(
            model_name='order',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_address',
            field=models.TextField(verbose_name='Адрес доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='delivery_method',
            field=models.CharField(choices=[('P', 'Pickup'), ('C', 'Courier'), ('S', 'Parcel')], max_length=1, verbose_name='Способ доставки'),
        ),
        migrations.AlterField(
            model_name='order',
            name='email',
            field=models.CharField(max_length=128, verbose_name='Email'),
        ),
        migrations.AlterField(
            model_name='order',
            name='first_name',
            field=models.CharField(max_length=128, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='order',
            name='items',
            field=models.ManyToManyField(blank=True, through='coolboards.OrderItem', to='coolboards.item', verbose_name='Товары'),
        ),
        migrations.AlterField(
            model_name='order',
            name='last_name',
            field=models.CharField(max_length=128, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='order',
            name='notes',
            field=models.TextField(blank=True, null=True, verbose_name='Примечания'),
        ),
        migrations.AlterField(
            model_name='order',
            name='order_status',
            field=models.CharField(choices=[('N', 'created'), ('A', 'awaiting_payment'), ('C', 'collecting'), ('D', 'delivering'), ('F', 'done'), ('X', 'cancelled')], max_length=1, verbose_name='Статус заказа'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_amount',
            field=models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Сумма'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_complete',
            field=models.BooleanField(verbose_name='Оплачен'),
        ),
        migrations.AlterField(
            model_name='order',
            name='payment_method',
            field=models.CharField(choices=[('P', 'pickup'), ('O', 'online')], max_length=1, verbose_name='Способ оплаты'),
        ),
        migrations.AlterField(
            model_name='order',
            name='phone',
            field=models.CharField(max_length=16, verbose_name='Телефон'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coolboards.item', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='order',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coolboards.order', verbose_name='Заказ'),
        ),
        migrations.AlterField(
            model_name='orderitem',
            name='quantity',
            field=models.PositiveIntegerField(verbose_name='Количество'),
        ),
        migrations.AlterField(
            model_name='review',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, verbose_name='Дата создания'),
        ),
        migrations.AlterField(
            model_name='review',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='coolboards.item', verbose_name='Товар'),
        ),
        migrations.AlterField(
            model_name='review',
            name='rating',
            field=models.PositiveSmallIntegerField(verbose_name='Оценка'),
        ),
        migrations.AlterField(
            model_name='review',
            name='text',
            field=models.TextField(verbose_name='Текст'),
        ),
        migrations.AlterField(
            model_name='review',
            name='user_name',
            field=models.TextField(verbose_name='Имя'),
        ),
        migrations.CreateModel(
            name='HistoricalOrder',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Дата создания')),
                ('first_name', models.CharField(max_length=128, verbose_name='Имя')),
                ('last_name', models.CharField(max_length=128, verbose_name='Фамилия')),
                ('phone', models.CharField(max_length=16, verbose_name='Телефон')),
                ('email', models.CharField(max_length=128, verbose_name='Email')),
                ('notes', models.TextField(blank=True, null=True, verbose_name='Примечания')),
                ('payment_complete', models.BooleanField(verbose_name='Оплачен')),
                ('payment_amount', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Сумма')),
                ('payment_method', models.CharField(choices=[('P', 'pickup'), ('O', 'online')], max_length=1, verbose_name='Способ оплаты')),
                ('order_status', models.CharField(choices=[('N', 'created'), ('A', 'awaiting_payment'), ('C', 'collecting'), ('D', 'delivering'), ('F', 'done'), ('X', 'cancelled')], max_length=1, verbose_name='Статус заказа')),
                ('delivery_method', models.CharField(choices=[('P', 'Pickup'), ('C', 'Courier'), ('S', 'Parcel')], max_length=1, verbose_name='Способ доставки')),
                ('delivery_address', models.TextField(verbose_name='Адрес доставки')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Заказ',
                'verbose_name_plural': 'historical Заказы',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalManufacturer',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('photo', models.TextField(max_length=100, null=True, verbose_name='Фото')),
                ('name', models.TextField(verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('slug', models.SlugField(verbose_name='Слаг')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Производитель',
                'verbose_name_plural': 'historical Производители',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalItemCategory',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('photo', models.TextField(max_length=100, null=True, verbose_name='Фото')),
                ('name', models.TextField(verbose_name='Название')),
                ('description', models.TextField(verbose_name='Описание')),
                ('slug', models.SlugField(verbose_name='Слаг')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'historical Категория товара',
                'verbose_name_plural': 'historical Категории товаров',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
        migrations.CreateModel(
            name='HistoricalItem',
            fields=[
                ('id', models.BigIntegerField(auto_created=True, blank=True, db_index=True, verbose_name='ID')),
                ('created_at', models.DateTimeField(blank=True, editable=False, verbose_name='Дата создания')),
                ('name', models.TextField(verbose_name='Название')),
                ('description', models.TextField(null=True, verbose_name='Описание')),
                ('price', models.DecimalField(decimal_places=2, max_digits=9, verbose_name='Цена')),
                ('discount', models.DecimalField(decimal_places=2, max_digits=9, null=True, verbose_name='Скидка')),
                ('new', models.BooleanField(verbose_name='Новинка')),
                ('stock', models.PositiveIntegerField(verbose_name='Количество на складе')),
                ('history_id', models.AutoField(primary_key=True, serialize=False)),
                ('history_date', models.DateTimeField(db_index=True)),
                ('history_change_reason', models.CharField(max_length=100, null=True)),
                ('history_type', models.CharField(choices=[('+', 'Created'), ('~', 'Changed'), ('-', 'Deleted')], max_length=1)),
                ('category', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='coolboards.itemcategory', verbose_name='Категория')),
                ('history_user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='+', to=settings.AUTH_USER_MODEL)),
                ('manufacturer', models.ForeignKey(blank=True, db_constraint=False, null=True, on_delete=django.db.models.deletion.DO_NOTHING, related_name='+', to='coolboards.manufacturer', verbose_name='Производитель')),
            ],
            options={
                'verbose_name': 'historical Товар',
                'verbose_name_plural': 'historical Товары',
                'ordering': ('-history_date', '-history_id'),
                'get_latest_by': ('history_date', 'history_id'),
            },
            bases=(simple_history.models.HistoricalChanges, models.Model),
        ),
    ]
