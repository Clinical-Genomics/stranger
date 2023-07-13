###############################################
# Dockerfile to build Stranger container image
#   docker build -t gvcn/stranger:v0.8.1 . --platform linux/amd64
#   docker push gvcn/stranger:v0.8.1
#   docker run -v $PWD:$PWD gvcn/stranger:v0.8.1 stranger --help
#   docker run -v $PWD:$PWD gvcn/stranger:v0.8.1 stranger -f /bin/stranger/stranger/resources/variant_catalog_hg38.json $PWD/sample.joint.repeats.merged.vcf.gz > $PWD/sample.repeats.stranger.vcf
###############################################
FROM continuumio/miniconda3:23.3.1-0-alpine

# Install git
RUN conda install -c anaconda git && \
    cd /bin && \
    git clone --branch v0.8.1 --depth 1 https://github.com/Clinical-Genomics/stranger.git && \
    cd stranger && \
    pip install --editable .

ENTRYPOINT ["stranger"]
