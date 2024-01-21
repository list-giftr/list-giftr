ARG PROJECT_HOME="/opt/list-giftr"

FROM node:18-bullseye AS staticfile_builder

ARG PROJECT_HOME

WORKDIR "${PROJECT_HOME}/theme/src"
COPY ./wishlists/theme/static_src ./

RUN npm install && npm run build:clean && npm run build:tailwind


FROM python:3.11-alpine

ARG PROJECT_HOME
WORKDIR "${PROJECT_HOME}"

ENV DEBIAN_FRONTEND=noninteractive \
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    POETRY_VERSION=1.7.1 \
    PYTHONUNBUFFERED=1

# Install Python dependencies
RUN pip install "poetry==${POETRY_VERSION}" \
    && poetry config virtualenvs.create false

COPY poetry.lock pyproject.toml ./
RUN poetry install --no-interaction --without dev

# Copy application source code
COPY . .

# Build CSS files
COPY --from=staticfile_builder "${PROJECT_HOME}/theme/static" "${PROJECT_HOME}/wishlists/theme/static"

ENTRYPOINT ["poetry", "run", "./entrypoint.sh"]
