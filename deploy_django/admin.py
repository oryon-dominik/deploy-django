from django.contrib import admin

from deploy_django.models import DeployClientModel


@admin.register(DeployClientModel)
class DeployClientModelAdmin(admin.ModelAdmin):
    fields = ('name', 'secret_auth_token')
    readonly_fields = ('secret_auth_token',)
