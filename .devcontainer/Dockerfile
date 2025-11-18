# syntax=docker/dockerfile:1
FROM mambaorg/micromamba:1.4.0

WORKDIR /workspaces/amplicon-haplotyping

# Install python, samtools, pbaa, pbtk and snakemake from conda-forge / bioconda via micromamba
RUN micromamba install -n base -y -c conda-forge -c bioconda \
    python=3.11 samtools pbaa snakemake biopython && \
    micromamba clean --all --yes

# Ensure conda bin is in PATH
ENV PATH=/opt/conda/bin:$PATH

# Create workspace directory and drop privileges to a non-root user (uid 1000)
RUN mkdir -p /workspaces/amplicon-haplotyping && chown -R 1000:1000 /workspaces

USER 1000

CMD ["bash"]
