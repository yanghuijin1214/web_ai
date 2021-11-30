# Generated by Django 3.2.7 on 2021-11-30 05:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Model',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('model_name', models.CharField(max_length=50, verbose_name='모델 파일 이름')),
                ('model', models.FileField(upload_to='image/', verbose_name='파일 경로')),
                ('created_date', models.DateTimeField(auto_now_add=True, verbose_name='파일 생성 시간')),
                ('data_size', models.IntegerField()),
                ('accuracy', models.CharField(max_length=10, verbose_name='정확도')),
                ('learning_time', models.CharField(max_length=10)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.user', verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('upload_date', models.DateTimeField(auto_now_add=True, verbose_name='업로드시간')),
                ('image_name', models.CharField(max_length=50, verbose_name='이미지명')),
                ('image', models.ImageField(upload_to='image/', verbose_name='image')),
                ('labeling', models.BooleanField(default=False, verbose_name='라벨링 여부')),
                ('labeling_name', models.CharField(max_length=50, null=True, verbose_name='라벨링명')),
                ('labeling_int', models.IntegerField(default=-1, verbose_name='라벨링 숫자')),
                ('training', models.BooleanField(default=False, verbose_name='학습 여부')),
                ('predict', models.CharField(max_length=50, null=True, verbose_name='예측결과')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='login.user', verbose_name='user')),
            ],
        ),
    ]
