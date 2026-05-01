FROM python:3.14-alpine

RUN apk add g++ cargo gcc python3-dev libffi-dev musl-dev zlib-dev jpeg-dev

# Install UV
RUN pip install uv hatch

# Set working directory
WORKDIR /app

ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Copy UV configuration files
COPY pyproject.toml uv.lock ./

# Install dependencies using UV
RUN uv sync --no-install-project --no-dev

# Copy application code
COPY . .

RUN uv sync --frozen

# Run the application
CMD ./bin/process-stations.sh
