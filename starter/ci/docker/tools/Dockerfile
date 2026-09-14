FROM docker:cli@sha256:eccaacfeed644c7de222ff047483568cb988dde95476fbaaf10ea2d04921bb66 AS dockercli
FROM python:3.12-slim
COPY --from=dockercli /usr/local/bin/docker /usr/local/bin/docker
COPY manage.py /app/manage.py
ENV PYTHONUNBUFFERED=1
ENTRYPOINT ["python", "/app/manage.py"]
