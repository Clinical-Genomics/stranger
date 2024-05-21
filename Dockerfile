###############################################
# Dockerfile to build Stranger container image
#   docker build -t clinical-genomics/stranger:v0.9.0 . --platform linux/amd64
#   docker push clinical-genomics/stranger:v0.9.0
#   docker run -v $PWD:$PWD clinical-genomics/stranger:v0.9.0 stranger --help
#   docker run -v $PWD:$PWD clinical-genomics/stranger:v0.9.0 stranger -f /bin/stranger/stranger/resources/variant_catalog_hg38.json $PWD/sample.joint.repeats.merged.vcf.gz > $PWD/sample.repeats.stranger.vcf
###############################################
FROM continuumio/miniconda3:23.3.1-0-alpine

# Install git
RUN conda install -c anaconda git && \
    cd /bin && \
    git clone --depth 1 https://github.com/Clinical-Genomics/stranger.git && \
    cd stranger && \
    pip install --editable .

ENTRYPOINT ["stranger"]
