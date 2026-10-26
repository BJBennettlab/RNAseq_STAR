# Copy to run_settings.sh and edit paths/account before running.
EXECUTOR="slurm"
SOFTWARE_MODE="modules"
WORKDIR="/90daydata/YOUR_PROJECT/rnaseq_run"
LANE_DIRS=(
    "/project/YOUR_PROJECT/study/raw/lane1"
    "/project/YOUR_PROJECT/study/raw/lane2"
)
SLURM_ACCOUNT="YOUR_PROJECT"
SLURM_PARTITION="ceres"
SLURM_MAIL=""
SAMPLE_NAME_STYLE="illumina"
GENCODE_RELEASE="M35"
STAR_SJDB_OVERHANG="auto"
COUNT_COLUMN="auto"
# Optional: put references in a shared, writable reference directory.
# REF_DIR="/90daydata/YOUR_PROJECT/references/gencode_m35"
# STAR_CPUS=8
# STAR_MEMORY="48G"
# INDEX_CPUS=16
# INDEX_MEMORY="128G"
