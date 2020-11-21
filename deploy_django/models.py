import secrets

from django.db import models
from django.utils.translation import ugettext_lazy as _


TOKEN_LEN = 256
CHALLANGE_LEN = 256


class DeployClientModel(models.Model):
    name = models.CharField(
        max_length=128,
        unique=True,
        db_index=True,
        help_text=('Service name of the external services')
    )
    secret_auth_token = models.CharField(
        max_length=TOKEN_LEN,
        editable=False,
        help_text=_('Secret for authentication. Will be automaticly generated.')
    )

    def __str__(self):
        return self.name

    def save(self, **kwargs):
        if not self.secret_auth_token:
            self.secret_auth_token = secrets.token_urlsafe(nbytes=TOKEN_LEN)

        super().save(**kwargs)


class DeployRequestsModel(models.Model):
    client = models.ForeignKey(
        DeployClientModel, on_delete=models.SET_NULL,
        null=True,
    )
    challange = models.CharField(
        max_length=CHALLANGE_LEN,
    )

    # TODO: create_dt=
    # TODO: remote_ip=
    # TODO: post_dt=

    def save(self, **kwargs):
        if not self.challange:
            self.challange = secrets.token_urlsafe(nbytes=TOKEN_LEN)

        super().save(**kwargs)
