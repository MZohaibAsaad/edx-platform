"""
The urls for on-boarding app.
"""
from django.conf.urls import patterns, url

from onboarding import views


urlpatterns = [
    url(r"^recommendations/$", views.recommendations, name="recommendations"),
    url(r"^user_info/$", views.user_info, name="user_info"),  # signup step 1
    url(r"^interests/$", views.interests, name="interests"),  # signup step 2
    url(r"^organization/$", views.organization, name="organization"),  # signup step 3
    url(r"^get_country_names/$", views.get_country_names, name="get_country_names"),
    url(r"^get_languages/$", views.get_languages, name="get_languages"),
    url(r"^account_settings/$", views.update_account_settings, name="update_account_settings"),
    url(r"^get_user_organizations/$", views.get_user_organizations, name="get_user_organizations"),
    url(r"^get_currencies/$", views.get_currencies, name="get_currencies"),
    url(r"^organization_detail/$", views.org_detail_survey, name="org_detail_survey"), # signup step 4
    url(r"^delete_account/$", views.delete_my_account, name="delete_my_account"), # signup step 4
    url(r"^admin_activate/(?P<org_id>[^/]*)/(?P<activation_key>[^/]*)$", views.admin_activation, name="admin_activation"),
    url(r"^admin_change_request/$", views.admin_change, name="admin_change"),
    url(r"^admin_change_request/(?P<confirmation>[0-1])/(?P<username>[^/]*)$",
        views.admin_change_confirmation, name="admin_change_confirmation")
]
