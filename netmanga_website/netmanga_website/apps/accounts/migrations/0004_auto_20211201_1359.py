# Generated by Django 3.1.13 on 2021-12-01 13:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0003_withdraworder_time'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mangaseries',
            name='primary_Genre',
            field=models.CharField(blank=True, choices=[('Select', 'Select'), ('Action', 'Action'), ('Drama', 'Drama'), ('Comedy', 'Comedy'), ('Fantasy', 'Fantasy'), ('Slice of Life', 'Slice of Life'), ('Romance', 'Romance'), ('Superhero', 'Superhero'), ('Sci-Fi', 'Sci-Fi'), ('Thriller', 'Thriller'), ('Supernatural', 'Supernatural'), ('Mystery', 'Mystery'), ('Sports', 'Sports'), ('Historical', 'Historical'), ('Heartwarming', 'Heartwarming'), ('Horror', 'Horror'), ('Informative', 'Informative')], max_length=18, null=True),
        ),
        migrations.AlterField(
            model_name='mangaseries',
            name='secondary_Genre',
            field=models.CharField(blank=True, choices=[('Select', 'Select'), ('Action', 'Action'), ('Drama', 'Drama'), ('Comedy', 'Comedy'), ('Fantasy', 'Fantasy'), ('Slice of Life', 'Slice of Life'), ('Romance', 'Romance'), ('Superhero', 'Superhero'), ('Sci-Fi', 'Sci-Fi'), ('Thriller', 'Thriller'), ('Supernatural', 'Supernatural'), ('Mystery', 'Mystery'), ('Sports', 'Sports'), ('Historical', 'Historical'), ('Heartwarming', 'Heartwarming'), ('Horror', 'Horror'), ('Informative', 'Informative')], max_length=18, null=True),
        ),
    ]
