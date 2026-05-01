import dataclasses
import json
from base64 import b64encode
from datetime import datetime
from hashlib import md5

from Crypto.Hash import HMAC
from Crypto.Hash import SHA1

def stringify(o):
    if dataclasses.is_dataclass(o):
        return json.dumps(dataclasses.asdict(o), separators=(',', ':'))
    else:
        return json.dumps(o, separators=(',', ':'))


def create_signature(secret_key, string) -> str:
    hmac = HMAC.new(secret_key, string.encode('utf-8'), SHA1)
    return b64encode(hmac.digest()).decode('utf-8')


def build_im_headers(dev_key: str, dev_secret: str, content: str ='', extra_name: str='', extra_value: str ='') -> dict[str, str]:
    now = datetime.now()
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



