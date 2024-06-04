# Generated by Django 3.2.25 on 2024-06-02 09:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('social', '0006_commentlikes_delete_commentrating'),
        ('wildlifeAPI', '0009_wildlifespeciessightings'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='wildlifespeciessightings',
            name='location',
        ),
        migrations.AddField(
            model_name='wildlifespeciessightings',
            name='related_post',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='sightings', to='social.post'),
        ),
    ]
