from django.urls import path

from bootstrap.views.branding import (
    SiteBrandingView,
    InstituteBrandingView,
    MaintainersBrandingView,
)

app_name = 'bootstrap'

urlpatterns = [
    path('site_branding/',
         SiteBrandingView.as_view(),
         name='site_branding'),
    path('institute_branding/',
         InstituteBrandingView.as_view(),
         name='institute_branding'),
    path('maintainers_branding/',
         MaintainersBrandingView.as_view(),
         name='maintainers_branding'),
]
