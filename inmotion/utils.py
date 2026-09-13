import dataclasses
import json
from base64 import b64encode
from datetime import datetime, timezone
from hashlib import md5
from typing import Optional, Type, TypeVar

import marshmallow_dataclass
import requests
from Crypto.Hash import HMAC
from Crypto.Hash import SHA1

from inmotion.exceptions import InMotionAPIError, InMotionConnectionError

DEFAULT_TIMEOUT_SECONDS = 30

_http_session = requests.Session()

T = TypeVar('T')

def stringify(o):
    if dataclasses.is_dataclass(o):
        return json.dumps(dataclasses.asdict(o), separators=(',', ':'))
    else:
        return json.dumps(o, separators=(',', ':'))


def stringify_model(o) -> str:
    """ Serialize a dataclass instance via its marshmallow schema, so fields that remap to a
    different JSON key (e.g. a Python-reserved word like 'from' aliased to 'from_') are
    serialized under their real API name rather than their Python attribute name. """
    schema = marshmallow_dataclass.class_schema(type(o))()
    return json.dumps(schema.dump(o), separators=(',', ':'))


def create_signature(secret_key, string) -> str:
    hmac = HMAC.new(secret_key, string.encode('utf-8'), SHA1)
    return b64encode(hmac.digest()).decode('utf-8')


def build_im_headers(dev_key: str, dev_secret: str, content: str ='', extra_name: str='', extra_value: str ='') -> dict[str, str]:
    now = datetime.now(timezone.utc)
    content_md5 = md5(content.encode('utf-8')).hexdigest()
    datetime_str = now.strftime('%Y-%m-%dT%H:%M:%S')
    hmac_content = datetime_str + "\n" + content_md5
    headers = {
        'im-content-md5': content_md5,
        'im-hmac': dev_key + ':' + create_signature(bytes(dev_secret, 'utf-8'), hmac_content),
        'im-request-date': datetime_str
    }

    if extra_name and extra_value:
        headers[extra_name] = extra_value

    return headers


def _send_request(method: str, url: str, headers: dict[str, str], data: str | bytes, error_message: str,
                   timeout: int):
    try:
        r = _http_session.request(method, url, headers=headers, data=data if data else None, timeout=timeout)
    except requests.RequestException as e:
        raise InMotionConnectionError(f"{error_message}: unable to reach inMotion") from e

    if r.status_code // 100 != 2:
        server_detail = None
        try:
            body = r.json()
            if isinstance(body, dict):
                server_detail = body.get('error') or body.get('message')
        except ValueError:
            pass
        detail = f": {server_detail}" if server_detail else f" (HTTP {r.status_code})"
        raise InMotionAPIError(f"{error_message}{detail}", status_code=r.status_code)

    return r


def request_json(method: str, url: str, headers: dict[str, str], data: str | bytes, error_message: str,
                  model: Optional[Type[T]] = None, timeout: int = DEFAULT_TIMEOUT_SECONDS,
                  many: bool = False) -> T:
    r = _send_request(method, url, headers, data, error_message, timeout)

    if model is None:
        return r.json()

    try:
        return marshmallow_dataclass.class_schema(model)(many=many).load(r.json())
    except Exception as e:
        raise InMotionAPIError(f"Malformed response received from inMotion for: {error_message}") from e


def request_json_map(method: str, url: str, headers: dict[str, str], data: str | bytes, error_message: str,
                      model: Type[T], timeout: int = DEFAULT_TIMEOUT_SECONDS) -> dict[str, T]:
    """ Like request_json, but for endpoints whose JSON response is a genuine map of key -> model
    instance (e.g. upload uuid -> UploadMetadataModel) rather than a single object or a list. """
    raw = request_json(method, url, headers, data, error_message, model=None, timeout=timeout)
    schema = marshmallow_dataclass.class_schema(model)()
    try:
        return {key: schema.load(value) for key, value in raw.items()}
    except Exception as e:
        raise InMotionAPIError(f"Malformed response received from inMotion for: {error_message}") from e


def request_raw(method: str, url: str, headers: dict[str, str], data: str | bytes, error_message: str,
                 timeout: int = DEFAULT_TIMEOUT_SECONDS) -> bytes:
    """ Issue a request and return the raw response body, for endpoints that don't return JSON. """
    r = _send_request(method, url, headers, data, error_message, timeout)
    return r.content

