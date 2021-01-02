import json

import pytest
from bugyocloudproxy import app


@pytest.fixture()
def apigw_event():
    """ Generates API GW Event"""
    return {
        "version": "2.0",
        "routeKey": "$default",
        "rawPath": "/my/path",
        "rawQueryString": "",
        "cookies": [],
        "headers": {},
        "queryStringParameters": {},
        "requestContext": {
            "accountId": "123456789012",
            "apiId": "api-id",
            "domainName": "id.execute-api.us-east-1.amazonaws.com",
            "domainPrefix": "id",
            "http": {
                "method": "POST",
                "path": "/my/path",
                "protocol": "HTTP/1.1",
                "sourceIp": "IP",
                "userAgent": "agent"
            },
            "requestId": "id",
            "routeKey": "$default",
            "stage": "$default",
            "time": "12/Mar/2020:19:03:58 +0000",
            "timeEpoch": 1583348638390
        },
        "body": json.dumps({
            "tenant_code": "12345",
            "login_id": "oneuser",
            "password": "pass",
            "clock_type": "clock_in"
        }),
        "pathParameters": {},
        "isBase64Encoded": False,
        "stageVariables": {}
    }


def test_lambda_handler(apigw_event, mocker):

    ret = app.lambda_handler(apigw_event, "")
    data = json.loads(ret["body"])

    assert ret["statusCode"] == 200
    assert "message" in ret["body"]
    assert data["message"] == "hello world"
    # assert "location" in data.dict_keys()
