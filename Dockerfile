###############################################
# Dockerfile to build Stranger container image
#   docker build -t clinical-genomics/stranger:v0.9.0 . --platform linux/amd64
#   docker push clinical-genomics/stranger:v0.9.0
#   docker run -v $PWD:$PWD clinical-genomics/stranger:v0.9.0 stranger --help
#   docker run -v $PWD:$PWD clinical-genomics/stranger:v0.9.0 stranger -f /bin/stranger/stranger/resources/variant_catalog_hg38.json $PWD/sample.joint.repeats.merged.vcf.gz > $PWD/sample.repeats.stranger.vcf
###############################################
FROM ghcr.io/astral-sh/uv:python3.13-alpine

# Copy the project into the image
ADD . /app

# Sync the project into a new environment, using the frozen lockfile
WORKDIR /app
RUN uv sync --frozen


ENTRYPOINT ["uv", "run", "stranger"]
