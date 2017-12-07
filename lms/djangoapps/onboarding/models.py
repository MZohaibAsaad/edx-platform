import logging
import uuid

import re

from django.contrib.auth.models import User
from model_utils.models import TimeStampedModel
from simple_history.models import HistoricalRecords
from django.core.validators import MaxValueValidator, URLValidator
from django.db import models

log = logging.getLogger("edx.onboarding")


class SchemaOrNoSchemaURLValidator(URLValidator):
    regex = re.compile(
        r'((([A-Za-z]{3,9}:(?:\/\/)?)(?:[-;:&=\+\$,\w]+@)?[A-Za-z0-9.-]'
        r'+|(?:www.|[-;:&=\+\$,\w]+@)[A-Za-z0-9.-]+)((?:\/[\+~%\/.\w-]*)'
        r'?\??(?:[-\+=&;%@.\w_]*)#?(?:[\w]*))?)',
        re.IGNORECASE
    )


class TimeStampedModelWithHistoryFields(TimeStampedModel):
    """
    Maintain history for a model each field
    """
    history = HistoricalRecords()
    __history_start_date = None
    __history_end_date = None

    def _history_start_date(self):
        return self.__history_start_date

    def _history_end_date(self):
        return self.__history_end_date

    def __str__(self):
        return self.label


class OrgSector(models.Model):
    """
    Specifies what sector the organization is working in.
    """
    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=256)

    def __str__(self):
        return self.label


class OperationLevel(models.Model):
    """
    Specifies the level of organization like national, international etc.
    """
    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=256)

    def __str__(self):
        return self.label


class FocusArea(models.Model):
    """
    The are of focus of an organization.
    """
    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=256)

    def __str__(self):
        return self.label


class TotalEmployee(models.Model):
    """
    Total employees in an organization.
    """
    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=256)

    def __str__(self):
        return self.label


class PartnerNetwork(models.Model):
    """
    Specifies about the partner network being used in an organization.
    """
    name = models.CharField(max_length=255)

    is_partner_affiliated = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Currency(models.Model):
    name = models.CharField(max_length=255)
    alphabetic_code = models.CharField(max_length=255)


class EducationLevel(models.Model):
    """
    Models education level of the user
    """
    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=256)

    def __str__(self):
        return self.label


class EnglishProficiency(models.Model):
    """
    Models english proficiency level of the user.
    """
    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=256)

    def __str__(self):
        return self.label


class FunctionArea(models.Model):
    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=255)

    def __str__(self):
        return self.label


class Organization(TimeStampedModelWithHistoryFields):
    """
    Represents an organization.
    """

    label = models.CharField(max_length=255, db_index=True)
    admin = models.ForeignKey(User, related_name='organization', blank=True, null=True, on_delete=models.SET_NULL)
    country = models.CharField(max_length=255, null=True)
    city = models.CharField(max_length=255, null=True)
    unclaimed_org_admin_email = models.EmailField(unique=True, null=True)
    url = models.URLField(max_length=255, blank=True, null=True, validators=[SchemaOrNoSchemaURLValidator])
    founding_year = models.PositiveSmallIntegerField(blank=True, null=True)
    registration_number = models.CharField(max_length=30, null=True)
    org_type = models.ForeignKey(OrgSector, related_name="organization", null=True)
    level_of_operation = models.ForeignKey(OperationLevel, related_name='organization', null=True)
    focus_area = models.ForeignKey(FocusArea, related_name='organization', null=True)
    total_employees = models.ForeignKey(TotalEmployee, related_name='organization', null=True)
    alternate_admin_email = models.EmailField(blank=True, null=True)

    def is_first_signup_in_org(self):
        return UserExtendedProfile.objects.filter(organization=self).count() == 1


class OrganizationPartner(models.Model):
    """
    The model to save the organization partners.
    """
    organization = models.ForeignKey(Organization, related_name='organization_partners')
    partner = models.ManyToManyField(PartnerNetwork)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()


class RoleInsideOrg(models.Model):
    """
    Specifies what is the role of a user inside the organization.
    """
    code = models.CharField(max_length=10, unique=True)
    label = models.CharField(max_length=256)

    def __str__(self):
        return self.label


class OrganizationAdminHashKeys(TimeStampedModel):
    """
    Model to hold hash keys for users that are suggested as admin for an organization
    """
    organization = models.ForeignKey(Organization, related_name='suggested_admins')
    suggested_by = models.ForeignKey(User)
    suggested_admin_email = models.EmailField(unique=True)
    is_hash_consumed = models.BooleanField(default=False)
    activation_hash = models.CharField(max_length=32)

    def __str__(self):
        return "%s-%s" % (self.suggested_admin_email, self.activation_key_for_admin)

    @classmethod
    def assign_hash(cls, organization, suggested_by, suggested_admin_email):
        return cls.objects.create(organization=organization, suggested_by=suggested_by,
                                  suggested_admin_email=suggested_admin_email, activation_hash=uuid.uuid4().hex)

class UserExtendedProfile(TimeStampedModelWithHistoryFields):
    """
    Extra profile fields that we don't want to enter in user_profile to avoid code conflicts at edx updates
    """

    INTERESTS_LABELS = {
        "interest_strategy_planning": "Strategy and planning",
        "interest_leadership_governance": "Leadership and governance",
        "interest_program_design": "Program design and development",
        "interest_measurement_eval": "Measurement, evaluation, and learning",
        "interest_stakeholder_engagement": "Stakeholder engagement and partnerships",
        "interest_human_resource": "Human resource management",
        "interest_financial_management": "Financial management",
        "interest_fundraising": "Fundraising and resource mobilization",
        "interest_marketing_communication": "Marketing, communications, and PR",
        "interest_system_tools": "Systems, tools, and processes",
    }

    user = models.OneToOneField(User, unique=True, db_index=True, related_name='extended_profile')
    organization = models.ForeignKey(Organization, related_name='extended_profile', blank=True, null=True,
                                     on_delete=models.SET_NULL)
    country_of_employment = models.CharField(max_length=255, null=True)
    city_of_employment = models.CharField(max_length=255, null=True)
    english_proficiency = models.CharField(max_length=10, null=True)
    level_of_education = models.CharField(max_length=10, null=True)
    start_month_year = models.CharField(max_length=100, null=True)
    role_in_org = models.ForeignKey(RoleInsideOrg, related_name='extended_profile', null=True)
    hours_per_week = models.PositiveIntegerField(validators=[MaxValueValidator(168)], null=True)

    # hold the status if user has completed all on-boarding surveys
    is_all_surveys_completed = models.BooleanField(default=False)

    # User functions related fields
    function_strategy_planning = models.SmallIntegerField("Strategy and planning", default=0)
    function_leadership_governance = models.SmallIntegerField("Leadership and governance", default=0)
    function_program_design = models.SmallIntegerField("Program design and development", default=0)
    function_measurement_eval = models.SmallIntegerField("Measurement, evaluation, and learning", default=0)
    function_stakeholder_engagement = models.SmallIntegerField("Stakeholder engagement and partnerships", default=0)
    function_human_resource = models.SmallIntegerField("Human resource management", default=0)
    function_financial_management = models.SmallIntegerField("Financial management", default=0)
    function_fundraising = models.SmallIntegerField("Fundraising and resource mobilization", default=0)
    function_marketing_communication = models.SmallIntegerField("Marketing, communications, and PR", default=0)
    function_system_tools = models.SmallIntegerField("Systems, tools, and processes", default=0)

    # User interests related fields
    interest_strategy_planning = models.SmallIntegerField(INTERESTS_LABELS["interest_strategy_planning"], default=0)
    interest_leadership_governance = models.SmallIntegerField(INTERESTS_LABELS["interest_leadership_governance"], default=0)
    interest_program_design = models.SmallIntegerField(INTERESTS_LABELS["interest_program_design"], default=0)
    interest_measurement_eval = models.SmallIntegerField(INTERESTS_LABELS["interest_measurement_eval"], default=0)
    interest_stakeholder_engagement = models.SmallIntegerField(INTERESTS_LABELS["interest_stakeholder_engagement"], default=0)
    interest_human_resource = models.SmallIntegerField(INTERESTS_LABELS["interest_human_resource"], default=0)
    interest_financial_management = models.SmallIntegerField(INTERESTS_LABELS["interest_financial_management"], default=0)
    interest_fundraising = models.SmallIntegerField(INTERESTS_LABELS["interest_fundraising"], default=0)
    interest_marketing_communication = models.SmallIntegerField(INTERESTS_LABELS["interest_marketing_communication"], default=0)
    interest_system_tools = models.SmallIntegerField(INTERESTS_LABELS["interest_system_tools"], default=0)

    # Learners related field
    learners_same_region = models.SmallIntegerField("Is learner interested in learners from same region", default=0)
    learners_similar_oe_interest = models.SmallIntegerField("Is learner interested in learners with similar org eff "
                                                            "interests", default=0)
    learners_similar_org = models.SmallIntegerField("Is learner interested in learners from similar organizations",
                                                    default=0)
    learners_diff_who_are_different = models.SmallIntegerField("Is learner interested in learners who are different",
                                                               default=0)

    # User goals related fields
    goal_contribute_to_org = models.SmallIntegerField("Is learner's goal is to contribute to his organization's "
                                                      "capacity", default=0)
    goal_gain_new_skill = models.SmallIntegerField("Is learner's goal is to gain new skill", default=0)
    goal_improve_job_prospect = models.SmallIntegerField("Is learner's goal is to improve job prospects", default=0)
    goal_relation_with_other = models.SmallIntegerField("Is learner's goal is to build relationship with other "
                                                        "learners", default=0)

    def get_user_selected_interests(self):
        return [label for field_name, label in self.INTERESTS_LABELS.items() if getattr(self, field_name) == 1]

    @property
    def attended_surveys(self):
        """Return list of user's attended onboarding surveys"""
        attended_list = []
        if self.level_of_education and self.start_month_year and self.english_proficiency:
           attended_list.append("first")
        elif self.get_user_selected_interests():
            attended_list.append("second")

        return attended_list

    @property
    def is_organization_admin(self):
        return self.user == self.organization.admin


class OrganizationMetric(TimeStampedModel):
    """
    Model to save organization metrics
    """
    ACTUAL_DATA_CHOICES = (
        (1, "Actual - My answers come directly from my organization's official documentation"),
        (0, "Estimated - My answers are my best guesses based on my knowledge of the organization")
    )

    org = models.ForeignKey(Organization, related_name="organization_metrics")
    user = models.ForeignKey(User, related_name="organization_metrics")
    submission_date = models.DateTimeField(auto_now_add=True)
    actual_data= models.NullBooleanField(choices=ACTUAL_DATA_CHOICES, blank=True, null=True)
    effective_date = models.DateField(blank=True, null=True)
    total_clients = models.PositiveIntegerField(blank=True, null=True)
    total_employees = models.PositiveIntegerField(blank=True, null=True)
    local_currency = models.ForeignKey(Currency, on_delete=models.SET_NULL, blank=True, null=True,
                                       related_name='organization_metics')
    total_revenue = models.BigIntegerField(blank=True, null=True)
    total_donations = models.BigIntegerField(blank=True, null=True)
    total_expenses = models.BigIntegerField(blank=True, null=True)
    total_program_expenses = models.BigIntegerField(blank=True, null=True)



