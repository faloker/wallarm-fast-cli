FROM python:alpine

RUN pip install wallarm-fast-cli

ENTRYPOINT [ "fast-cli" ]