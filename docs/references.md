# Reference inputs

Keep reference inputs fixed for a study and its repeat runs. They do not need
routine updates when a provider publishes a newer release. Changing an annotation
can change gene IDs and counts.

| Input | Purpose | How it is provided |
| --- | --- | --- |
| `References/mouse_rrna.fasta` | HTStream rRNA measurement | Included in this repository; mouse reference from the UC Davis RNA-seq workshop |
| `GRCm39.primary_assembly.genome.fa` | STAR genome | Downloaded during reference setup; default GENCODE mouse M35 primary assembly |
| `gencode.vM35.annotation.gtf` | Gene models and splice junctions | Downloaded during reference setup; default GENCODE mouse M35 comprehensive annotation |
| `ensembl_mm_112.txt` | Gene annotation table in original R analyses | Not included; obtain the recorded Ensembl 112 export before using those analyses. Not needed for STAR counts |
| Study metadata spreadsheets | Sample identities, groups and covariates for R analyses | Supplied for the study; not included in the reusable workflow |

The genome and GTF are stored in the configured REF_DIR, not in References/.
The STAR index is built from them. Reuse those files for matching runs. For a
different annotation release, select GENCODE_RELEASE in run_settings.sh, confirm
its assembly, and use a new reference directory, index and WORKDIR.

Release page: https://www.gencodegenes.org/mouse/release_M35.html
Download directory: https://ftp.ebi.ac.uk/pub/databases/gencode/Gencode_mouse/release_M35/
rRNA source: https://ucdavis-bioinformatics-training.github.io/2025-June-RNA-Seq-Analysis/data_reduction/mouse_rrna.fasta

`run.sh references` downloads the selected release, checks compressed MD5 values
from GENCODE, fully decompresses the files, and records SHA-256, sizes, and URLs.
A reference already present without matching recorded provenance is rejected.
The index manifest records STAR version, overhang, reference-manifest digest,
and hashes for the required index files. An incomplete index is not reused.

The original scripts refer to `combined_genome.fa` and `combined_annotation.gtf`.
Their exact contents were not recovered. GENCODE M35 reproduced the earlier
study closely, but did not produce an identical matrix. The default inputs are
not an exact reconstruction of those original combined files.

The historical `ensembl_mm_112.txt` file is not the GTF used for alignment. Its
original export query and full provenance still need confirmation. For a new R
analysis, obtain a release-specific Ensembl/BioMart export with named attributes,
save the query and checksums, and check gene-ID coverage. Do not replace it with
an unrecorded current export merely to make an old R Markdown file execute.
