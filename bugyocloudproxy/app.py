import json
from logging import Logger, getLogger
from typing import Any

from bugyocloudclient import AuthInfo, BugyoCloudClient
from bugyocloudclient.models.punchinfo import ClockType, PunchInfo
from bugyocloudclient.tasks.logintask import LoginTask
from bugyocloudclient.tasks.punchtask import PunchTask

logger = getLogger(__name__)


class EventBody:
    def __init__(self, event: dict) -> None:
        if 'body' not in event:
            logger.critical('"body" is not presented.')

        self._body = json.loads(event['body'])

    def __getattr__(self, name: str) -> Any:
        if name not in self._body:
            logger.critical('"{}" is not presented'.format(name))
        return self._body[name]


def create_client(tenant_code: str) -> BugyoCloudClient:
    return BugyoCloudClient(tenant_code)


def create_logintask(login_id: str, password: str) -> LoginTask:
    auth_info = AuthInfo(login_id, password)
    return LoginTask(auth_info)


def create_punchtask(clock_type: str) -> PunchTask:
    punch_info = PunchInfo()
    punch_info.clock_type = ClockType[clock_type]
    punch_info.latitude = 35.6812
    punch_info.longitude = 139.7742
    return PunchTask(punch_info)


def lambda_handler(event, context):
    """Bugyo Cloud proxy

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    body = EventBody(event)
    client = create_client(body.tenant_code)
    login_task = create_logintask(body.login_id, body.password)
    punch_task = create_punchtask(body.clock_type)

    client.exec(login_task)
    client.exec(punch_task)

    return {
        "statusCode": 200,
        "body": json.dumps({
            "result": "OK",
        }),
    }
