from dotenv import dotenv_values

from inmotion.apikey_client import InMotionAPIKeyClient
from inmotion.models import ActivitySearchFilterModel


def main():
    config = dotenv_values(".env.test")
    client = InMotionAPIKeyClient(config['BASE_URL'], config['DEV_KEY'], config['DEV_SECRET'],
                                  config['API_KEY'])
    session = client.get_session(config['ACCOUNT'])

    print(session.activities().find_activities(ActivitySearchFilterModel()))

if __name__ == "__main__":
    main()
