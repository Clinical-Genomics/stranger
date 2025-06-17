###############################################
# Dockerfile to build Stranger container image
#   docker build -t clinical-genomics/stranger:v0.9.0 . --platform linux/amd64
#   docker push clinical-genomics/stranger:v0.9.0
#   docker run -v $PWD:$PWD clinical-genomics/stranger:v0.9.0 stranger --help
#   docker run -v $PWD:$PWD clinical-genomics/stranger:v0.9.0 stranger -f /bin/stranger/stranger/resources/variant_catalog_hg38.json $PWD/sample.joint.repeats.merged.vcf.gz > $PWD/sample.repeats.stranger.vcf
###############################################
FROM ghcr.io/astral-sh/uv:python3.13-alpine AS builder
ENV UV_COMPILE_BYTECODE=1 UV_LINK_MODE=copy

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --locked --no-dev

FROM ghcr.io/astral-sh/uv:python3.13-alpine

RUN addgroup app && adduser -D -s /sbin/nologin -G app app

WORKDIR /home/worker/app

COPY --from=builder --chown=app:app /app /app

ENV PATH="/app/.venv/bin:$PATH"

USER app

ENTRYPOINT ["stranger"]
