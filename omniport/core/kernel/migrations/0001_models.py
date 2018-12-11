import django.core.validators
import django.db.models.deletion
import django_countries.fields
import swapper
from django.db import migrations, models

import kernel.utils.upload_to


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        # Depends on the app auth for defining the model User
        swapper.dependency('auth', 'User'),
    ]

    operations = [
        # Institute
        migrations.CreateModel(
            name='Centre',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=7, unique=True)),
                ('name', models.CharField(max_length=127)),
            ],
            options={
                'swappable': swapper.swappable_setting('kernel', 'Centre'),
            },
        ),
        migrations.CreateModel(
            name='Department',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=7, unique=True)),
                ('name', models.CharField(max_length=127)),
            ],
            options={
                'swappable': swapper.swappable_setting('kernel', 'Department'),
            },
        ),
        migrations.CreateModel(
            name='Residence',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=7, unique=True)),
                ('name', models.CharField(max_length=127)),
            ],
            options={
                'swappable': swapper.swappable_setting('kernel', 'Residence'),
            },
        ),
        migrations.CreateModel(
            name='Branch',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=7, unique=True)),
                ('name', models.CharField(max_length=127)),
                ('semester_count', models.IntegerField(blank=True, null=True)),
            ],
            options={
                'verbose_name_plural': 'branches',
                'swappable': swapper.swappable_setting('kernel', 'Branch'),
            },
        ),
        migrations.CreateModel(
            name='Course',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=7, unique=True)),
                ('name', models.CharField(max_length=127)),
                ('credits', models.IntegerField(validators=[django.core.validators.MinValueValidator(limit_value=1)])),
            ],
            options={
                'swappable': swapper.swappable_setting('kernel', 'Course'),
            },
        ),
        migrations.CreateModel(
            name='Degree',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('code', models.CharField(max_length=7, unique=True)),
                ('name', models.CharField(max_length=127)),
                ('graduation', models.CharField(choices=[('mat', 'Matriculate'), ('int', 'Intermediate'), ('ass', 'Associate'), ('gra', 'Graduate'), ('pos', 'Postgraduate'), ('doc', 'Doctorate'), ('pdo', 'Postdoctorate')], max_length=3)),
            ],
            options={
                'swappable': swapper.swappable_setting('kernel', 'Degree'),
            },
        ),

        # Roles
        migrations.CreateModel(
            name='FacultyMember',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('designation', models.CharField(max_length=63)),
            ],
            options={
                'swappable': swapper.swappable_setting('kernel', 'FacultyMember'),
            },
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('enrolment_number', models.CharField(max_length=15, unique=True)),
                ('current_year', models.IntegerField()),
                ('current_semester', models.IntegerField()),
                ('current_cgpa', models.DecimalField(blank=True, decimal_places=3, max_digits=5, null=True, validators=[django.core.validators.MaxValueValidator(10.0), django.core.validators.MinValueValidator(0.0)], verbose_name='current CGPA')),
            ],
            options={
                'swappable': swapper.swappable_setting('kernel', 'Student'),
            },
        ),
        migrations.CreateModel(
            name='Maintainer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('start_date', models.DateField()),
                ('end_date', models.DateField(blank=True, null=True)),
                ('role', models.CharField(blank=True, max_length=127)),
                ('designation', models.CharField(blank=True, max_length=127)),
                ('post', models.CharField(blank=True, max_length=127)),
            ],
            options={
                'swappable': swapper.swappable_setting('kernel', 'Maintainer'),
            },
        ),

        # Person
        migrations.CreateModel(
            name='Person',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user', models.OneToOneField(blank=True, null=True, on_delete=django.db.models.CASCADE, to=swapper.get_model_name('auth', 'User'))),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('short_name', models.CharField(blank=True, max_length=63)),
                ('full_name', models.CharField(max_length=255)),
                ('display_picture', models.ImageField(blank=True, max_length=255, null=True, upload_to=kernel.utils.upload_to.UploadTo('kernel', 'display_pictures'))),
            ],
            options={
                'verbose_name_plural': 'people',
                'swappable': swapper.swappable_setting('kernel', 'Person'),
            },
        ),

        # Personal information
        migrations.CreateModel(
            name='BiologicalInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('date_of_birth', models.DateField()),
                ('blood_group', models.CharField(choices=[('O+', 'O+'), ('O-', 'O-'), ('A+', 'A+'), ('A-', 'A-'), ('B+', 'B+'), ('B-', 'B-'), ('AB+', 'AB+'), ('AB-', 'AB-')], max_length=3)),
                ('gender', models.CharField(choices=[('man', 'Man'), ('woman', 'Woman'), ('n-bin', 'Non-binary/Other'), ('n-dis', 'Prefer not to disclose')], max_length=7)),
                ('sex', models.CharField(choices=[('male', 'Male'), ('female', 'Female'), ('n-bin', 'Non-binary/Other'), ('n-dis', 'Prefer not to disclose')], max_length=7)),
                ('pronoun', models.CharField(choices=[('h', 'He/him/his'), ('s', 'She/her/her'), ('t', 'They/them/their')], max_length=1)),
                ('impairment', models.CharField(choices=[('o', 'Orthopaedically impaired'), ('v', 'Visually impaired'), ('h', 'Hearing impaired'), ('s', 'Speech impaired'), ('n', 'No impairment')], max_length=1)),
            ],
            options={
                'verbose_name_plural': 'biological information',
                'swappable': swapper.swappable_setting('kernel', 'BiologicalInformation'),
            },
        ),
        migrations.CreateModel(
            name='FinancialInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('local_bank', models.CharField(blank=True, max_length=63)),
                ('local_bank_account_number', models.CharField(blank=True, max_length=31)),
                ('annual_income', models.DecimalField(blank=True, decimal_places=2, max_digits=31, null=True)),
            ],
            options={
                'verbose_name_plural': 'financial information',
                'swappable': swapper.swappable_setting('kernel', 'FinancialInformation'),
            },
        ),
        migrations.CreateModel(
            name='PoliticalInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('nationality', django_countries.fields.CountryField(max_length=2)),
                ('religion', models.CharField(blank=True, max_length=15)),
                ('passport_number', models.CharField(blank=True, max_length=15)),
                ('driving_license_number', models.CharField(blank=True, max_length=31)),
            ],
            options={
                'verbose_name_plural': 'political information',
                'swappable': swapper.swappable_setting('kernel', 'PoliticalInformation'),
            },
        ),
        migrations.CreateModel(
            name='ResidentialInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('room_number', models.CharField(max_length=15)),
            ],
            options={
                'verbose_name_plural': 'residential information',
                'swappable': swapper.swappable_setting('kernel', 'ResidentialInformation'),
            },
        ),

        # Generics
        migrations.CreateModel(
            name='ContactInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('primary_phone_number', models.CharField(max_length=15, unique=True)),
                ('secondary_phone_number', models.CharField(blank=True, max_length=15, null=True, unique=True)),
                ('email_address', models.EmailField(max_length=254, unique=True)),
                ('email_address_verified', models.BooleanField(default=False)),
                ('institute_webmail_address', models.EmailField(blank=True, max_length=254, null=True, unique=True)),
                ('entity_object_id', models.PositiveIntegerField()),
                ('video_conference_id', models.CharField(blank=True, max_length=127, null=True, unique=True, verbose_name='video conference ID')),
                ('entity_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'contact information',
            },
        ),
        migrations.CreateModel(
            name='LocationInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=127)),
                ('state', models.CharField(max_length=127)),
                ('country', django_countries.fields.CountryField(max_length=2)),
                ('postal_code', models.IntegerField(validators=[django.core.validators.RegexValidator('[0-9]{3,9}')])),
                ('latitude', models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True)),
                ('longitude', models.DecimalField(blank=True, decimal_places=8, max_digits=12, null=True)),
                ('entity_object_id', models.PositiveIntegerField()),
                ('entity_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
            ],
            options={
                'verbose_name_plural': 'location information',
            },
        ),
        migrations.CreateModel(
            name='SocialLink',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('site', models.CharField(choices=[('beh', 'Behance'), ('blo', 'Blogger'), ('dri', 'Dribble'), ('fac', 'Facebook'), ('fli', 'Flickr'), ('git', 'Github'), ('goo', 'Google'), ('lin', 'LinkedIn'), ('med', 'Medium'), ('pin', 'Pinterest'), ('red', 'Reddit'), ('sky', 'Skype'), ('sna', 'Snapchat'), ('tum', 'Tumblr'), ('twi', 'Twitter'), ('you', 'YouTube'), ('oth', 'Other website')], max_length=7)),
                ('url', models.URLField(max_length=255, verbose_name='URL')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='SocialInformation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('datetime_created', models.DateTimeField(auto_now_add=True)),
                ('datetime_modified', models.DateTimeField(auto_now=True)),
                ('entity_object_id', models.PositiveIntegerField()),
                ('entity_content_type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='contenttypes.ContentType')),
                ('links', models.ManyToManyField(blank=True, to='kernel.SocialLink')),
            ],
            options={
                'verbose_name_plural': 'social information',
            },
        ),
    ]
