from datetime import datetime
from logging import getLogger

import pytz
from django.db import IntegrityError

from common.lib.surveygizmo_client.client import SurveyGizmoClient
from lms.djangoapps.third_party_surveys.models import ThirdPartySurvey

log = getLogger(__name__)


def get_third_party_surveys():
    """
    Periodic Task that will run on daily basis and will sync the response data
    of all surveys thorough Survey Gizmo APIs
    We are scheduling this task through Jenkins instead of celery beat.
    """
    try:
        last_survey = ThirdPartySurvey.objects.latest('request_date')
        filters = [('datesubmitted', '>', last_survey.request_date)]
    except ThirdPartySurvey.DoesNotExist:
        filters = []

    survey_responses = SurveyGizmoClient().get_filtered_survey_responses(survey_filters=filters)
    save_responses(survey_responses)


def save_responses(survey_responses):
    for response in survey_responses:
        if not response.get('[url("edx_uid")]'):
            continue

        date = datetime.strptime(response['datesubmitted'], "%Y-%m-%d %H:%M:%S")

        third_party_survey = ThirdPartySurvey(
            response=response,
            user_id=response['[url("edx_uid")]'],
            request_date=date,
            survey_type=response['[url("app")]']
        )

        # Pass the exception if the user=sguid doesn't exist in the Database
        try:
            third_party_survey.save()
        except (IntegrityError, ValueError) as exc:
            log.error(exc)
