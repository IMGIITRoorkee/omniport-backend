import django.core.validators
import django.db.models.deletion
import django_countries.fields
import swapper
from django.db import migrations, models

import formula_one.utils.upload_to
import formula_one.validators.aspect_ratio


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
                ('display_picture', models.ImageField(blank=True, max_length=255, null=True, upload_to=formula_one.utils.upload_to.UploadTo('kernel', 'display_pictures'), validators=[formula_one.validators.aspect_ratio.AspectRatioValidator(1)])),
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
                ('annual_income', models.DecimalField(blank=True, decimal_places=2, max_digits=31, null=True, validators=[django.core.validators.MinValueValidator(0)])),
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
                ('religion', models.CharField(blank=True, max_length=63)),
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
    ]
