FROM python:3.11-slim

# Working Directory
WORKDIR /app

# Copy source code to working directory
COPY webapp_code /app/
COPY requirements.txt /app/

# Install packages from requirements.txt
# hadolint ignore=DL3013
RUN pip install --no-cache-dir --upgrade pip &&\
    pip install --no-cache-dir -r requirements.txt

# Don't run the web server as root
RUN useradd --system --no-create-home app
USER app

ENV PORT=8080
EXPOSE ${PORT}
ENV DASH_PORT ${PORT}

ENTRYPOINT [ "python" ]
CMD ["-u", "app.py"]
