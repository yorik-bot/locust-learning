FROM python:3.12-slim-bullseye

WORKDIR /locust

RUN --mount=type=cache,target=/root/.cache/pip  \
    python -m venv /venv && \
    . /venv/bin/activate && \
    pip install locust

ENV PATH="/venv/bin:$PATH"

COPY locustfile.py locustfile.py

EXPOSE 8089

ENTRYPOINT ["locust", "--processes", "-1"]
