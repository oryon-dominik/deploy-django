from django.contrib import admin

from deploy_django.models import DeployProtocol


@admin.register(DeployProtocol)
class DeployProtocolAdmin(admin.ModelAdmin):
    pass
