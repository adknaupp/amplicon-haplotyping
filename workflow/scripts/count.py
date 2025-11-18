import os
import re
from Bio.Align import PairwiseAligner
from Bio.Seq import Seq

# Prefer Snakemake's config when this script is executed from a workflow.
try:
    CONFIG = snakemake.config  # provided by Snakemake when running within a rule
except NameError:
    # Fallback: load `config.yaml` from the current working directory.
    import yaml
    config_path = os.path.join(os.getcwd(), 'config.yaml')
    if not os.path.exists(config_path):
        raise FileNotFoundError('config.yaml not found in current directory')
    with open(config_path, 'r') as _f:
        CONFIG = yaml.safe_load(_f)

HAPLOTYPES = CONFIG['haplotypes']
GENE = CONFIG['gene']
POS_1 = CONFIG['SNP_1']
POS_2 = CONFIG['SNP_2']

def get_cluster_stats(cluster_data):
    label, seq = cluster_data.split('\n', 1)
    read_count = re.search(r'ReadCount-(\d+)', label).group(1)
    cluster_name = re.search(r'cluster-(\d+)', label).group(1)
    frequency = re.search(r'cluster_freq:(\d+\.\d+)', label).group(1)
    possibly_chimeric = True if not 'uchime_score:-1' in label else False # ignore at high volume
    return cluster_name, seq.strip(), int(read_count), float(frequency)

def get_clusters(sample):
    '''Gets all clusters from output files of pbaa'''
    with open(f'results/pbaa/{sample}/{sample}_passed_cluster_sequences.fasta', 'r') as f:
        passed_filters = True
        for cluster in f.read().split('>')[1:]:
            yield *get_cluster_stats(cluster), passed_filters

    with open(f'results/pbaa/{sample}/{sample}_failed_cluster_sequences.fasta', 'r') as f:
        passed_filters = False
        for cluster in f.read().split('>')[1:]:
            yield *get_cluster_stats(cluster), passed_filters

def get_num_input_reads(sample):
    with open(f'results/pbaa/{sample}/{sample}_read_info.txt', 'r') as f:
        # count num newlines in file
        return sum(1 for _ in f)

def get_total_num_reads(sample):
    with open(f'results/fastq/{sample}.fastq.fai', 'r') as f:
        # count num newlines in file
        return sum(1 for _ in f)

ALIGNER = PairwiseAligner()
ALIGNER.mode = 'local' # in case the sequences are not the same length
ALIGNER.match_score = 1
ALIGNER.mismatch_score = 0.9

with open(CONFIG['guide'], 'r') as f:
    lines = f.readlines()
    REF_SEQ = ''.join([l.strip() for l in lines[1:]])

def _get_alignment(query):
    alignment = ALIGNER.align(REF_SEQ, query)[0]
    rev_comp_alignment = ALIGNER.align(REF_SEQ, Seq(query).reverse_complement())[0]
    if alignment.score < rev_comp_alignment.score:
        alignment = rev_comp_alignment
    return alignment

def _get_haplotype(seq):
    if seq == 'NNNNNNNNNN':
        return None
    alignment = _get_alignment(seq)
    snp_1, snp_2 = alignment[1, POS_1], alignment[1, POS_2]
    haplotype = (snp_1 + snp_2).lower()
    return haplotype

def write_clusters(rows):
    path = f'results/{GENE}.clusters_by_haplotype.csv'
    with open(path, 'w') as f:
        header = ('sample_name', 'cluster_name', 'haplotype')
        f.write(','.join(header) + '\n')
        for row in rows:
            if None in row:
                continue
            f.write(','.join(row) + '\n')

def write_counts(rows):
    path = f'results/{GENE}.haplotype_counts.csv'
    with open(path, 'w') as f:
        header = ('sample_name', 'total_reads', 'failed_qc', 'failed_filters', 'failed_haplotyping') + \
            tuple('haplotype_' + ht + '_reads' for ht in HAPLOTYPES)
        f.write(','.join(header) + '\n')
        for row in rows:
            f.write(','.join(str(x) for x in row) + '\n')

def main():
    cluster_rows = []
    rows = []
    for sample_name in os.listdir('results/pbaa'):
        total_reads = get_total_num_reads(sample_name)
        passed_qc = get_num_input_reads(sample_name)
        failed_qc = total_reads - passed_qc
        ht_counts = {ht: 0 for ht in HAPLOTYPES}
        failed_filters = 0
        failed_haplotyping = 0
        for cluster_name, seq, read_count, freq, passed_filters in get_clusters(sample_name):
            if not passed_filters:
                failed_filters += read_count
            haplotype = _get_haplotype(seq)
            if haplotype in HAPLOTYPES:
                ht_counts[haplotype] += read_count
            else:
                failed_haplotyping += read_count
            cluster_rows.append((sample_name, cluster_name, str(haplotype)))
        rows.append(
            (sample_name, total_reads, failed_qc, failed_filters, failed_haplotyping) + tuple(ht_counts[ht] for ht in HAPLOTYPES)
        )

    write_clusters(cluster_rows)
    write_counts(rows)

if __name__ == '__main__' or 'snakemake' in globals():
    main()