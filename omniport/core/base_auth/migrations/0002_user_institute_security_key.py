# Generated by Django 3.0.3 on 2021-10-06 04:55

from django.db import migrations, models
import uuid

from base_auth.models import User

class Migration(migrations.Migration):

    dependencies = [
        ('base_auth', '0001_initial'),
    ]

    def generate_institute_security_key(apps, schema_editor):
        """
        Helper function to generate unique institute security keys while
        migrations
        """
        for user in User.objects.all():
            user.institute_security_key = uuid.uuid4()
            user.save()

    operations = [
        migrations.AddField(
            model_name='user',
            name='institute_security_key',
            field=models.CharField(default=uuid.uuid4, blank=False, max_length=255, null=False),
            preserve_default=True
        ),
        migrations.RunPython(
            code=generate_institute_security_key,
            reverse_code=migrations.RunPython.noop,
        ),
        migrations.AlterField(
            model_name='user',
            name='institute_security_key',
            field=models.CharField(default=uuid.uuid4, blank=False, max_length=255, null=False, unique=True),
        ),
    ]
