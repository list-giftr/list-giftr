FROM python:3.11

ARG PROJECT_HOME=/opt/unnamed-web-project
WORKDIR ${PROJECT_HOME}

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.7.1 \
    PYTHONUNBUFFERED=1

RUN apt-get update \
    && curl -fsSL https://deb.nodesource.com/setup_18.x | bash - \
    && apt-get install -y nodejs \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
RUN pip install "poetry==${POETRY_VERSION}" \
    && poetry config virtualenvs.create false
COPY poetry.lock pyproject.toml .
RUN poetry install --no-interaction --without dev

# Copy application source code
COPY . .

# Build CSS files
RUN cd unnamed_web_project \
    && python ./manage.py tailwind install \
    && python ./manage.py tailwind build

ENTRYPOINT ["./entrypoint.sh"]
