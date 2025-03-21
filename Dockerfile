FROM python:3.13-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /bin/

WORKDIR /app

COPY . .

RUN apt-get update && apt-get install -y libzbar0 libgl1-mesa-glx
RUN uv sync --frozen

EXPOSE 8080

CMD ["uv", "run", "gunicorn", "--bind", "0.0.0.0:8080", "app:app"]
