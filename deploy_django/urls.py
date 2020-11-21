from django.urls import path

from deploy_django.views import DeployTriggerView


urlpatterns = [
    path('', DeployTriggerView.as_view(), name='deploy'),
]
