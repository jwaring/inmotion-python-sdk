from inmotion.api import InMotionMqttDeployment, InMotionSession
from inmotion.models import MqttDeploymentRegistrationModel, MqttDeploymentUpdateModel
from inmotion.utils import request_json, stringify


class InMotionMqttDeploymentImpl(InMotionMqttDeployment):

    def __init__(self, session: InMotionSession):
        self._session = session
        self._prefix_path = f"{session.base_url}{session.api_path}/mqtt-deployment"

    def register_mqtt_deployment(self, account_key: str, registration: MqttDeploymentRegistrationModel) -> dict:
        registration_data = stringify(registration)
        return request_json('POST', f"{self._prefix_path}/{account_key}",
                             self._session.build_headers(content=registration_data),
                             registration_data,
                             'Failed to register MQTT deployment')

    def list_mqtt_deployments(self, account_key: str) -> dict:
        return request_json('GET', f"{self._prefix_path}/{account_key}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to list MQTT deployments')

    def update_mqtt_deployment(self, account_key: str, deployment_id: str, update: MqttDeploymentUpdateModel) -> dict:
        update_data = stringify(update)
        return request_json('POST', f"{self._prefix_path}/{account_key}/{deployment_id}",
                             self._session.build_headers(content=update_data),
                             update_data,
                             'Failed to update MQTT deployment')

    def delete_mqtt_deployment(self, account_key: str, deployment_id: str) -> dict:
        return request_json('DELETE', f"{self._prefix_path}/{account_key}/{deployment_id}",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to delete MQTT deployment')

    def repoint_mqtt_deployment(self, account_key: str, deployment_id: str) -> dict:
        return request_json('POST', f"{self._prefix_path}/{account_key}/{deployment_id}/repoint",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to re-point MQTT deployment')

    def rotate_mqtt_deployment_key(self, account_key: str, deployment_id: str) -> dict:
        return request_json('POST', f"{self._prefix_path}/{account_key}/{deployment_id}/rotate-key",
                             self._session.build_headers(content=''),
                             '',
                             'Failed to rotate MQTT deployment key')
