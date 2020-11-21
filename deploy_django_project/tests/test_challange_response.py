import hashlib
from django.test import TestCase

from deploy_django.models import DeployClientModel


class DeployChallangeResponse(TestCase):
    def test_basic(self):
        # The User must first add a new client:
        deploy_client = DeployClientModel.objects.create(
            name='test-client'
        )
        # This secret token must be copy&paste into the client (e.g.: github action secrets)
        secret_auth_token = deploy_client.secret_auth_token


        # First client request: get the challange:
        response = self.client.get('/deploy/?client_name=test-client')
        assert response.status_code == 200

        get_data = response.json()
        assert 'challange' in get_data
        challange_request = get_data['challange']

        challange_response = hashlib.sha256(
            bytes(secret_auth_token + challange_request, encoding='ASCII')
        ).hexdigest()

        response = self.client.post('/deploy/', data={
            'client_name': 'test-client',
            'challange': challange_response
        })
        assert response.status_code == 200
