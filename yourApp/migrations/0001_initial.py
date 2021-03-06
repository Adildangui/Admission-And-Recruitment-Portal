# Generated by Django 2.1.7 on 2019-05-07 04:49

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Attachments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UUID', models.CharField(max_length=255)),
                ('Graduation_GraduationCertificate', models.CharField(max_length=255, null=True)),
                ('GateAttachments_GateRankCard', models.CharField(max_length=255, null=True)),
                ('Research_ResearchPapers', models.CharField(max_length=255, null=True)),
                ('Recommendations_RecommendationLetter', models.CharField(max_length=255, null=True)),
            ],
            options={
                'db_table': 'FullTime_YourPortal_January_2019_Attachments',
            },
        ),
        migrations.CreateModel(
            name='EducationalQualifications',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UUID', models.CharField(max_length=255)),
                ('DegreeDescription_Degree', models.CharField(max_length=31, null=True)),
                ('DegreeDescription_Discipline', models.CharField(max_length=63, null=True)),
                ('DegreeDescription_CollegeName', models.CharField(max_length=127, null=True)),
                ('DegreeDescription_StartDate', models.DateField(null=True)),
                ('DegreeDescription_EndingDate', models.DateField(null=True)),
                ('DegreeDescription_CGPA', models.FloatField(blank=True, null=True)),
                ('DegreeDescription2_Degree2', models.CharField(max_length=31, null=True)),
                ('DegreeDescription2_Discipline2', models.CharField(max_length=63, null=True)),
                ('DegreeDescription2_CollegeName2', models.CharField(max_length=127, null=True)),
                ('DegreeDescription2_StartDate2', models.DateField(null=True)),
                ('DegreeDescription2_EndingDate2', models.DateField(null=True)),
                ('DegreeDescription2_CGPA2', models.FloatField(blank=True, null=True)),
                ('DegreeFromIITs_DegreeFromIIT', models.BooleanField(null=True)),
                ('GateDetails_GateQualiFicationYear', models.IntegerField(blank=True, null=True)),
                ('GateDetails_GateScore', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'FullTime_YourPortal_January_2019_EducationalQualifications',
            },
        ),
        migrations.CreateModel(
            name='PersonalDetails',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UUID', models.CharField(max_length=255)),
                ('NameDescription_Name', models.CharField(max_length=127, null=True)),
                ('PrimaryAddressDescription_PrimaryAddress', models.CharField(max_length=255, null=True)),
                ('PrimaryAddressDescription_PrimaryAddressState', models.CharField(max_length=31, null=True)),
                ('PrimaryAddressDescription_PrimaryAddressPinCode', models.IntegerField(blank=True, null=True)),
                ('SecondaryAddressDescription_SecondaryAddress', models.CharField(max_length=255, null=True)),
                ('SecondaryAddressDescription_SecondaryAddressState', models.CharField(max_length=31, null=True)),
                ('SecondaryAddressDescription_SecondaryAddressPinCode', models.IntegerField(blank=True, null=True)),
                ('PrimaryEmailDescription_PrimaryEmail', models.CharField(max_length=63, null=True)),
                ('SecondaryEmailDescription_SecondaryEmail', models.CharField(max_length=63, null=True)),
                ('PrimaryContactDescription_PrimaryContact', models.BigIntegerField(blank=True, null=True)),
                ('SecondaryContactDescription_SecondaryContact', models.BigIntegerField(blank=True, null=True)),
                ('CategoryDescription_Category', models.CharField(max_length=31, null=True)),
                ('GenderDescription_Gender', models.CharField(max_length=15, null=True)),
            ],
            options={
                'db_table': 'FullTime_YourPortal_January_2019_PersonalDetails',
            },
        ),
        migrations.CreateModel(
            name='WorkExperience',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('UUID', models.CharField(max_length=255)),
                ('Designation', models.CharField(max_length=63, null=True)),
                ('OrganizationName', models.CharField(max_length=255, null=True)),
                ('JoiningDate', models.DateField(null=True)),
                ('LeavingDate', models.DateField(null=True)),
            ],
            options={
                'db_table': 'FullTime_YourPortal_January_2019_WorkExperience',
            },
        ),
    ]
