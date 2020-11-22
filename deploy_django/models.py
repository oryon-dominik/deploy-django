from bx_py_utils.models.timetracking import TimetrackingBaseModel
from django.db import models
from django.utils.translation import ugettext_lazy as _


class DeployProtocol(TimetrackingBaseModel):
    logging_output = models.TextField(
        help_text=_('The output of the deployment')
    )
