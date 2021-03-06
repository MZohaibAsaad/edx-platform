from openedx.core.djangoapps.timed_notification.core import get_course_link
from student.models import ENROLL_STATUS_CHANGE, EnrollStatusChange
from xmodule.modulestore.django import modulestore
from django.dispatch import receiver
from common.lib.mandrill_client.client import MandrillClient


@receiver(ENROLL_STATUS_CHANGE)
def enrollment_confirmation(sender, event=None, user=None, **kwargs):
    if event == EnrollStatusChange.enroll:
        course = modulestore().get_course(kwargs.get('course_id'))
        context = {
            'course_name': course.display_name,
            # TODO: find a way to move this code to PhilU overrides
            'course_url': get_course_link(course_id=course.id),
            'full_name': user.first_name + " " + user.last_name
        }
        MandrillClient().send_mail(
            MandrillClient.ENROLLMENT_CONFIRMATION_TEMPLATE,
            user.email,
            context
        )

