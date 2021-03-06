# Generated by Django 2.2 on 2020-04-21 14:13

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Node',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=255, verbose_name='name')),
                ('sequent', models.PositiveSmallIntegerField(default=0, editable=False, verbose_name='sequent')),
                ('tree_path', models.TextField(db_index=True, editable=False, verbose_name='branch')),
                ('created_at', models.DateTimeField(default=None, editable=False, verbose_name='created date')),
                ('parent', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='materialized_paths.Node', verbose_name='parent')),
            ],
            options={
                'verbose_name': 'node',
                'verbose_name_plural': 'nodes',
                'ordering': ['tree_path', 'created_at'],
            },
        ),
    ]
