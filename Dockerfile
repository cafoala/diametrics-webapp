FROM python:3.10-slim-bullseye

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY code /app/
COPY requirements.txt /app/

# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir --trusted-host pypi.python.org -r requirements.txt

EXPOSE 80
ENV DASH_PORT 80

ENTRYPOINT [ "python" ]
CMD ["-u", "tabs-app.py"]
