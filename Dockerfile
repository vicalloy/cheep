FROM python:3.11-bullseye

RUN sed -i 's/deb.debian.org/mirrors.huaweicloud.com/g' /etc/apt/sources.list

RUN set -ex \
	&& mkdir /root/.pip \
	&& echo '[global]' > /root/.pip/pip.conf \
	&& echo 'index-url = https://mirrors.bfsu.edu.cn/pypi/web/simple/' >> /root/.pip/pip.conf

RUN apt-get update && apt-get install -y \
		patchelf \
		clang \
		llvm \
		ccache \
		python3-dev \
    	rustc \
		cargo \
		build-essential \
		libssl-dev \
		libffi-dev \
		--no-install-recommends


RUN pip install --upgrade pip setuptools
RUN pip install --upgrade cryptography==39.0.2
RUN pip install --upgrade poetry

RUN mkdir /app
WORKDIR /app

COPY ./poetry.lock ./
COPY ./pyproject.toml ./
RUN poetry config virtualenvs.create false
RUN poetry install --only main
RUN pip install nuitka ordered-set
