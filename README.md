# inmotion-python-sdk

A Python Software Development Kit (SDK) for integration with inMotion APIs.

This is still a fledgling project as only a handful of endpoints have been implemented.

# Prerequisites

* Python 3.6 or higher
* uvicorn

# Build

To build the SDK, you can use the following command:

```bash
uv build
```

# Integration Tests

* Ensure that there is an inMotion integration test environment available.
* Configure the environment file (`.env.test` in the root directory) with the necessary credentials and URLs.

```dotenv
BASE_URL="http://localhost:9000"
DEV_KEY="xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
DEV_SECRET="xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
API_KEY="xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
ACCOUNT="xxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
```

The `DEV_KEY`, `DEV_SECRET` can be created using the inMotion `Settings ...` menu under the right hand side. If the account allows the
creation of keys, a tab called `Dev Keys` will be shown. Create the key / secret and copy the values.

The `API_KEY` can be created using the `API Keys` tab. The `ACCOUNT` key and will need to be copied. Note that it is recommended that the
API Key be at least `Consumer` authority to support the text.

Please run the tests in a virtual environment to avoid dependency conflicts.

```bash
source .venv/bin/activate
uv pip install -e .
python3 scripts/test.py
```

# Example

An example program is provided in the `examples` directory will load the [Australian Bureau of Meteorology](http://www.bom.gov.au/)
climatology weather data into inMotion test environment. Downloaded from the [BoM FTP server]().

Before running the application, ensure that the environment variables are set in the `.env.bom` file as described above. With the following additions:

```dotenv
DRY_RUN=false   # Set to true if you want to try without uploading
ROOT_DIR="<download-folder>/climate_data/tables"
```

Please run the importation example in a virtual environment using the commands below:

```bash
source .venv/bin/activate
uv pip install -e .
python3 eexamples/process_stations.py
```

Finally
```bash
