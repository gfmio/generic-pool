ARG tag="3.9-buster"
ARG workdir="/src"
ARG user="vscode"
ARG poetry_version="1.1.13"
ARG task_version="v3.12.1"

FROM python:${tag}

ARG workdir
ARG user
ARG poetry_version
ARG task_version

ENV DEBIAN_FRONTEND=noninteractive
ENV LC_ALL C.UTF-8
ENV LANG C.UTF-8

WORKDIR /tmp

# Install common packages

RUN apt-get update --allow-releaseinfo-change && \
    apt-get -y install --no-install-recommends zsh curl git sudo vim ca-certificates

# Set the root password

RUN echo "root:root" | chpasswd

# Add the non-root user

RUN adduser ${user} --shell /bin/zsh
RUN adduser ${user} sudo
RUN echo "${user}:${user}" | chpasswd

# Install Oh My Zsh for the user

RUN su ${user} -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"

# Install Taskfile

RUN sh -c "$(curl --location https://taskfile.dev/install.sh)" -- -d -b /usr/local/bin ${task_version}

# Install poetry

RUN mkdir /opt/poetry
ENV POETRY_HOME=/opt/poetry
ENV PATH="/opt/poetry/bin:$PATH"
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/${poetry_version}/get-poetry.py | python - --version ${poetry_version}

# Change the owner of the poetry installation to vscode

RUN chown -R ${user} /opt/poetry

# Set venv

ENV VIRTUAL_ENV="${workdir}/.venv"
ENV PATH="$VIRTUAL_ENV/bin:$PATH"

WORKDIR ${workdir}

USER ${user}
