# Snakemake workflow: `amplicon-haplotyping`

[![Snakemake](https://img.shields.io/badge/snakemake-≥8.0.0-brightgreen.svg)](https://snakemake.github.io)
[![GitHub actions status](https://github.com/adknaupp/amplicon-haplotyping/workflows/Tests/badge.svg?branch=main)](https://github.com/adknaupp/amplicon-haplotyping/actions?query=branch%3Amain+workflow%3ATests)
[![run with conda](http://img.shields.io/badge/run%20with-conda-3EB049?labelColor=000000&logo=anaconda)](https://docs.conda.io/en/latest/)
[![workflow catalog](https://img.shields.io/badge/Snakemake%20workflow%20catalog-darkgreen)](https://snakemake.github.io/snakemake-workflow-catalog/docs/workflows/adknaupp/amplicon-haplotyping)

A Snakemake workflow for detecting any given two-SNP haplotype from a long-read amplicon dataset using PacBio Amplicon Analysis.

- [Usage](#usage)
- [Deployment](#deployment)
- [Workflow execution](#workflow-execution)
- [Authors](#authors)
- [References](#references)

## Usage

The usage of this workflow is described in the [Snakemake Workflow Catalog](https://snakemake.github.io/snakemake-workflow-catalog/docs/workflows/adknaupp/amplicon-haplotyping).

Detailed information about input data and workflow configuration can also be found in the [`config/README.md`](config/README.md).

If you use this workflow in a paper, don't forget to give credits to the authors by citing the URL of this repository or its DOI.

## Deployment

Download the workflow files to your system by cloning the git repo and use conda 
to install dependencies.

### Use conda

To run this workflow, you *have* to have `conda` installed (unless SMRT Link is 
installed on your system, but even then, it's more convenient to follow the 
recommendations below).
This is because `pbaa` (the most important tool in the workflow) is only available 
via bioconda (or SMRT Link, as noted above).
Once you have `conda` installed, just install `snakemake`, then all other 
dependencies will be installed by `snakemake` when you run the workflow.

## Workflow execution

Once you have the workflow on your system, change the working directory to 
`amplicon-haplotyping` and provide a config file with the `--configfile` option.
To avoid having to manually install software dependencies (or even manually 
build and select conda environments), use the `--sdm conda` option with each run.

```bash
cd path/to/amplicon-haplotyping
snakemake --cores 1 --sdm conda --configfile .test/test.yaml
```

### Configuring the workflow with your parameters

Workflow parameters (described in `config/schemas/config.schema.yaml`) are defined 
in a YAML file and passed to the workflow using the `--configfile` option.
Example config files are provided for ADRB1 and ADRB2 haplotypes.

## Software dependencies

- python
- biopython
- samtools 
- pbaa (as a standalone package, `pbaa` is only available via bioconda (otherwise, `pbaa` is included with SMRT Link)).

Although the dependencies are already defined within the workflow, if you want to manually 
install them, you can run:
```
conda install -n amplicon-haplotyping -y -c conda-forge -c bioconda \
    python=3.11 samtools pbaa snakemake biopython
```

## Development

To enable development on Windows, a Dockerfile as been prepared which includes all necessary dependencies. Build the container image using `.devcontainer/Dockerfile`. If you use VS Code, you can use this as a Devcontainer (defined in `.devcontainer/devcontainer.json`) which includes the snakemake language extension.

Test data referenced from `.test/test.yaml` is included for ease of development.

## Authors

- Ammon Knaupp
  - BYU Genomic and Bioinformatic Center
  - [ORCiD profile](https://orcid.org/0000-0001-6131-6672)
  - [adknaupp.github.io](adknaupp.github.io)

## References

> Köster, J., Mölder, F., Jablonski, K. P., Letcher, B., Hall, M. B., Tomkins-Tinch, C. H., Sochat, V., Forster, J., Lee, S., Twardziok, S. O., Kanitz, A., Wilm, A., Holtgrewe, M., Rahmann, S., & Nahnsen, S. _Sustainable data analysis with Snakemake_. F1000Research, 10:33, 10, 33, **2021**. https://doi.org/10.12688/f1000research.29032.2.
