from django.contrib import admin

from lms.djangoapps.onboarding.models import (
    RoleInsideOrg,
    Currency,
    OrgSector,
    OperationLevel,
    FocusArea,
    TotalEmployee,
    PartnerNetwork,
    EducationLevel,
    EnglishProficiency,
    Organization,
    UserExtendedProfile,
    FunctionArea,
    OrganizationPartner,
)


class BaseDropdownOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'code', 'label',)


class RoleInsideOrgAdmin(BaseDropdownOrderAdmin):
    pass


class OrgSectorAdmin(BaseDropdownOrderAdmin):
    pass


class OperationLevelAdmin(BaseDropdownOrderAdmin):
    pass


class FocusAreaAdmin(BaseDropdownOrderAdmin):
    pass


class TotalEmployeeAdmin(BaseDropdownOrderAdmin):
    pass


class PartnerNetworkAdmin(BaseDropdownOrderAdmin):
    list_display = ('order', 'code', 'label', 'is_partner_affiliated')


class EducationLevelAdmin(BaseDropdownOrderAdmin):
    pass


class EnglishProficiencyAdmin(BaseDropdownOrderAdmin):
    pass


class FunctionAreaAdmin(BaseDropdownOrderAdmin):
    pass


class CurrencyAdmin(admin.ModelAdmin):
    list_display = ('country', 'name', 'alphabetic_code', )


class OraganizationAdmin(admin.ModelAdmin):
    list_display = ('label', 'admin', 'country', 'unclaimed_org_admin_email', 'founding_year', )


class UserExtendedProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'organization', 'country_of_employment', 'role_in_org', 'hours_per_week', )


class OrganizationPartnerAdmin(admin.ModelAdmin):
    list_display = ('organization', 'partner', 'start_date', 'end_date',)
    list_filter = ('organization', 'partner', 'start_date', 'end_date',)


admin.site.register(Currency, CurrencyAdmin)
admin.site.register(RoleInsideOrg, RoleInsideOrgAdmin)
admin.site.register(OrgSector, OrgSectorAdmin)
admin.site.register(OperationLevel, OperationLevelAdmin)
admin.site.register(FocusArea, FocusAreaAdmin)
admin.site.register(TotalEmployee, TotalEmployeeAdmin)
admin.site.register(PartnerNetwork, PartnerNetworkAdmin)
admin.site.register(EducationLevel, EnglishProficiencyAdmin)
admin.site.register(EnglishProficiency, EnglishProficiencyAdmin)
admin.site.register(Organization, OraganizationAdmin)
admin.site.register(UserExtendedProfile, UserExtendedProfileAdmin)
admin.site.register(FunctionArea, FunctionAreaAdmin)
admin.site.register(OrganizationPartner, OrganizationPartnerAdmin)
