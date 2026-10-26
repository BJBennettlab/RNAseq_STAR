# RNAseq_STAR

Paired-end mouse RNA-seq: combine sequencing lanes, preprocess with HTStream,
align with STAR, and produce checked gene counts and BAM files.

## Setup and run

On **Ceres (SCINet)**, use **Clusters > Ceres Shell Access** in
[Open OnDemand](https://scinet.usda.gov/guides/use/open-ondemand), or connect by SSH.
Work in a directory you can write to under your project allocation. Raw data
belongs in persistent project storage; processing outputs can go under `/90daydata`.

Clone the repository:

```bash
git clone https://github.com/BJBennettlab/RNAseq_STAR.git
cd RNAseq_STAR
```

Keep raw FASTQs in separate lane directories. Each lane must contain the same
samples and its provider's `@md5Sum.md5` file. If a study was sequenced as
separate pools on different lanes, run each pool as its own run and join the
validated count tables afterwards with `scripts/combine_runs.py` (see
[SETUP_INSTRUCTIONS.txt](SETUP_INSTRUCTIONS.txt)). Continue on Ceres:

```bash
cp examples/ceres.sh run_settings.sh
nano run_settings.sh
python3 0_Setup/4_fetch_star.py
./run.sh scan
./run.sh check
./run.sh all --dry-run
./run.sh all
./run.sh status
```

Set the output directory, raw lane paths and Slurm account in `run_settings.sh`.
`scan` shows filenames and sample naming; `check` checks settings and software.
`all` submits dependent Slurm jobs. The numbered scripts still perform each stage.
The STAR setup downloads a fixed, checksum-verified Linux build into this copy.

On **another Linux system**, use `examples/linux.sh`. Install or activate Python
3.11+, HTStream, STAR, SAMtools and GNU command-line tools first. Local mode runs
one sample at a time without Slurm; keep the process running until it finishes.
A workstation needs enough RAM for the mouse index and BAM sorting, typically at
least 48 GiB. Another Slurm cluster can use either site modules or programs on PATH.

[SETUP_INSTRUCTIONS.txt](SETUP_INSTRUCTIONS.txt) covers each setting, stage-by-stage
commands, checks and recovery. [Runtime setup](docs/runtime.md) describes software
installation and recorded builds. A new study needs a new output directory.

## Results

| Run directory | Contents |
| --- | --- |
| `03-Counts/counts.txt` | Integer gene-by-sample count matrix |
| `02-STAR_alignment/` | Sorted BAMs, BAM indexes, STAR count tables and logs |
| `summary_htstream.txt`, `mapping_qc.tsv`, `strandedness.tsv` | Per-sample QC |
| `count_validation.json`, `bam_validation.json` | Count comparison and BAM checks |
| `samples.txt`, `input_manifest.tsv` | Sample order and exact inputs from every lane |
| `run_records/` | Source snapshot, configuration and executable identities |
| `jobs.tsv` or `local_jobs.json`, `slurmout/` | Task records and output/error logs |

Each FASTQ is assigned to a sample by its full name (`<sample>_S<n>_L<lane>_R1_001.fastq.gz`
by default), so a name that begins another name, such as `MOUSE_1` and `MOUSE_10`,
always keeps its own files. `input_manifest.tsv` records the exact file used for
every sample and lane.

Processing does not modify raw files. Missing mates, different sample sets, name collisions,
failed source checks and failed pipeline commands stop processing. Finalization
compares every count cell with its STAR table, checks BAMs and builds indexes.
Require successful task completion and passed validation reports. An empty error
log alone is not a completion check. [Validation commands](docs/validation.md)
show how to repeat the checks.

## References and analysis choices

The default is GRCm39 / GENCODE M35. The reference stage downloads the genome and
gene annotation and checks GENCODE's MD5 list. `References/mouse_rrna.fasta` is
already included for HTStream's rRNA measurement. Keep these inputs fixed within
a study; they do not need routine updates. A different annotation release needs
a new reference directory, index and run. See [reference inputs](docs/references.md)
for what is included, what is downloaded, and the separate inputs needed by the
original R analyses.

Sample names retain underscores by default. Any number of lanes is supported.
`COUNT_COLUMN=auto` checks strand estimates per sample and stops if they disagree;
confirm the library preparation when interpreting this choice. HTStream's original
duplicate removal and trimming are retained. rRNA is measured, not removed.
Trimmed singletons are saved but not aligned by this paired-read workflow.

`4_DE_Analysis/` contains the original study-specific R analyses. They are not run
by `all`; they need their own metadata, design and contrasts. GBRS and QTL mapping
are separate analyses. [CHANGELOG.md](CHANGELOG.md) records pipeline changes.
