# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models
import model_utils.fields
import django.db.models.deletion
import lms.djangoapps.onboarding.models
import django.utils.timezone
from django.conf import settings
import django.core.validators


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Currency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=255)),
                ('alphabetic_code', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='EducationLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('label', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='EnglishProficiency',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('label', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='FocusArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('label', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='FunctionArea',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('label', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='OperationLevel',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('label', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='Organization',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('label', models.CharField(max_length=255, db_index=True)),
                ('country', models.CharField(max_length=255, null=True, blank=True)),
                ('city', models.CharField(max_length=255, null=True, blank=True)),
                ('unclaimed_org_admin_email', models.EmailField(max_length=254, unique=True, null=True, blank=True)),
                ('url', models.URLField(blank=True, max_length=255, null=True, validators=[lms.djangoapps.onboarding.models.SchemaOrNoSchemaURLValidator])),
                ('founding_year', models.PositiveSmallIntegerField(null=True, blank=True)),
                ('registration_number', models.CharField(max_length=30, null=True, blank=True)),
                ('org_type', models.CharField(max_length=10, null=True, blank=True)),
                ('level_of_operation', models.CharField(max_length=10, null=True, blank=True)),
                ('focus_area', models.CharField(max_length=10, null=True, blank=True)),
                ('total_employees', models.CharField(max_length=10, null=True, blank=True)),
                ('alternate_admin_email', models.EmailField(max_length=254, null=True, blank=True)),
                ('admin', models.ForeignKey(related_name='organization', on_delete=django.db.models.deletion.SET_NULL, blank=True, to=settings.AUTH_USER_MODEL, null=True)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationAdminHashKeys',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('suggested_admin_email', models.EmailField(unique=True, max_length=254)),
                ('is_hash_consumed', models.BooleanField(default=False)),
                ('activation_hash', models.CharField(max_length=32)),
                ('organization', models.ForeignKey(related_name='suggested_admins', to='onboarding.Organization')),
                ('suggested_by', models.ForeignKey(to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationMetric',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('submission_date', models.DateTimeField(auto_now_add=True)),
                ('actual_data', models.NullBooleanField(choices=[(1, b"Actual - My answers come directly from my organization's official documentation"), (0, b'Estimated - My answers are my best guesses based on my knowledge of the organization')])),
                ('effective_date', models.DateField(null=True, blank=True)),
                ('total_clients', models.PositiveIntegerField(null=True, blank=True)),
                ('total_employees', models.PositiveIntegerField(null=True, blank=True)),
                ('local_currency', models.CharField(max_length=10, null=True, blank=True)),
                ('total_revenue', models.BigIntegerField(null=True, blank=True)),
                ('total_donations', models.BigIntegerField(null=True, blank=True)),
                ('total_expenses', models.BigIntegerField(null=True, blank=True)),
                ('total_program_expenses', models.BigIntegerField(null=True, blank=True)),
                ('org', models.ForeignKey(related_name='organization_metrics', to='onboarding.Organization')),
                ('user', models.ForeignKey(related_name='organization_metrics', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='OrganizationPartner',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_date', models.DateTimeField()),
                ('end_date', models.DateTimeField()),
                ('organization', models.ForeignKey(related_name='organization_partners', to='onboarding.Organization')),
            ],
        ),
        migrations.CreateModel(
            name='OrgSector',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('label', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='PartnerNetwork',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('label', models.CharField(max_length=255)),
                ('is_partner_affiliated', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='RoleInsideOrg',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('label', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='TotalEmployee',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('code', models.CharField(unique=True, max_length=10)),
                ('label', models.CharField(max_length=256)),
            ],
        ),
        migrations.CreateModel(
            name='UserExtendedProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', model_utils.fields.AutoCreatedField(default=django.utils.timezone.now, verbose_name='created', editable=False)),
                ('modified', model_utils.fields.AutoLastModifiedField(default=django.utils.timezone.now, verbose_name='modified', editable=False)),
                ('country_of_employment', models.CharField(max_length=255, null=True)),
                ('not_listed_gender', models.CharField(max_length=255, null=True, blank=True)),
                ('city_of_employment', models.CharField(max_length=255, null=True)),
                ('english_proficiency', models.CharField(max_length=10, null=True)),
                ('level_of_education', models.CharField(max_length=10, null=True)),
                ('start_month_year', models.CharField(max_length=100, null=True)),
                ('role_in_org', models.CharField(max_length=10, null=True)),
                ('hours_per_week', models.PositiveIntegerField(default=0, verbose_name=b'Typical Number of Hours Worked per Week*', validators=[django.core.validators.MaxValueValidator(168)])),
                ('function_strategy_planning', models.SmallIntegerField(default=0, verbose_name=b'Strategy and planning')),
                ('function_leadership_governance', models.SmallIntegerField(default=0, verbose_name=b'Leadership and governance')),
                ('function_program_design', models.SmallIntegerField(default=0, verbose_name=b'Program design and development')),
                ('function_measurement_eval', models.SmallIntegerField(default=0, verbose_name=b'Measurement, evaluation, and learning')),
                ('function_stakeholder_engagement', models.SmallIntegerField(default=0, verbose_name=b'Stakeholder engagement and partnerships')),
                ('function_human_resource', models.SmallIntegerField(default=0, verbose_name=b'Human resource management')),
                ('function_financial_management', models.SmallIntegerField(default=0, verbose_name=b'Financial management')),
                ('function_fundraising', models.SmallIntegerField(default=0, verbose_name=b'Fundraising and resource mobilization')),
                ('function_marketing_communication', models.SmallIntegerField(default=0, verbose_name=b'Strategy and planning')),
                ('function_system_tools', models.SmallIntegerField(default=0, verbose_name=b'Systems, tools, and processes')),
                ('interest_strategy_planning', models.SmallIntegerField(default=0, verbose_name=b'Strategy and planning')),
                ('interest_leadership_governance', models.SmallIntegerField(default=0, verbose_name=b'Leadership and governance')),
                ('interest_program_design', models.SmallIntegerField(default=0, verbose_name=b'Program design and development')),
                ('interest_measurement_eval', models.SmallIntegerField(default=0, verbose_name=b'Measurement, evaluation, and learning')),
                ('interest_stakeholder_engagement', models.SmallIntegerField(default=0, verbose_name=b'Stakeholder engagement and partnerships')),
                ('interest_human_resource', models.SmallIntegerField(default=0, verbose_name=b'Human resource management')),
                ('interest_financial_management', models.SmallIntegerField(default=0, verbose_name=b'Financial management')),
                ('interest_fundraising', models.SmallIntegerField(default=0, verbose_name=b'Fundraising and resource mobilization')),
                ('interest_marketing_communication', models.SmallIntegerField(default=0, verbose_name=b'Marketing, communications, and PR')),
                ('interest_system_tools', models.SmallIntegerField(default=0, verbose_name=b'Systems, tools, and processes')),
                ('learners_same_region', models.SmallIntegerField(default=0, verbose_name=b'Learners from my region or country')),
                ('learners_similar_oe_interest', models.SmallIntegerField(default=0, verbose_name=b'Learners interested in same areas of organization effectiveness')),
                ('learners_similar_org', models.SmallIntegerField(default=0, verbose_name=b'Learners working for similar organizations')),
                ('learners_diff_who_are_different', models.SmallIntegerField(default=0, verbose_name=b'Learners who are different from me')),
                ('goal_contribute_to_org', models.SmallIntegerField(default=0, verbose_name=b'Help improve my organization')),
                ('goal_gain_new_skill', models.SmallIntegerField(default=0, verbose_name=b'Develop new skills')),
                ('goal_improve_job_prospect', models.SmallIntegerField(default=0, verbose_name=b'Get a job')),
                ('goal_relation_with_other', models.SmallIntegerField(default=0, verbose_name=b'Build relantionships with other nonprofit leaders')),
                ('is_interests_data_submitted', models.BooleanField(default=False)),
                ('is_organization_metrics_submitted', models.BooleanField(default=False)),
                ('organization', models.ForeignKey(related_name='extended_profile', on_delete=django.db.models.deletion.SET_NULL, blank=True, to='onboarding.Organization', null=True)),
                ('user', models.OneToOneField(related_name='extended_profile', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='organizationpartner',
            name='partner',
            field=models.ForeignKey(related_name='organization_partners', to='onboarding.PartnerNetwork'),
        ),
    ]
