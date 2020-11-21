import hashlib
import logging

from django.http import HttpResponse, HttpResponseForbidden, JsonResponse
from django.views import View

from deploy_django.models import DeployClientModel, DeployRequestsModel


CHALLANGE_LEN = 128
CHALLANGE_KEY = 'challange'

logger = logging.getLogger(__name__)


class ChallangeNotValid(Exception):
    pass


def check_challange(secret_auth_token, challange_request, challange_response):

    # TODO: hashlib.pbkdf2_hmac()
    test = hashlib.sha256(
        bytes(secret_auth_token + challange_request, encoding='ASCII')
    ).hexdigest()

    if test != challange_response:
        raise ChallangeNotValid()


class DeployTriggerView(View):
    def get(self, request):
        """
        return challange
        """
        client_name = request.GET['client_name']

        deploy_client = DeployClientModel.objects.get(name=client_name)

        # TODO: Check if DeployRequestsModel exists
        deploy_request = DeployRequestsModel.objects.create(client=deploy_client)

        challange_request = deploy_request.challange

        return JsonResponse({
            CHALLANGE_KEY: challange_request
        })

    def post(self, request):
        """
        check challange
        """
        if CHALLANGE_KEY not in request.POST:
            logger.error('no callange in POST')
            return HttpResponseForbidden()

        challange_response = request.POST[CHALLANGE_KEY]
        # TODO: Check length

        client_name = request.POST['client_name']
        deploy_client = DeployClientModel.objects.get(name=client_name)

        deploy_request = DeployRequestsModel.objects.get(client=deploy_client)

        # TODO: Check remote_ip
        # TODO: Check if request is outdated

        challange_request = deploy_request.challange

        secret_auth_token = deploy_client.secret_auth_token

        try:
            check_challange(secret_auth_token, challange_request, challange_response)
        except ChallangeNotValid:
            # TODO: POST failed
            return HttpResponseForbidden()

        return HttpResponse()
