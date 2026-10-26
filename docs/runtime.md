# STAR runtime setup

From a copied pipeline directory on Linux x86_64:

```bash
python3 0_Setup/4_fetch_star.py
./run.sh check
```

The setup downloads STAR 2.7.11b's official static Linux x86_64 binary and license
from source commit `b1edc1208d91a53bf40ebae8669f71d50b994851`. It checks pinned SHA-256
values before making the files available. An existing different file causes an
error. No administrator access or system installation is needed.

The setup creates `tools/` in the repository directory. `tools/star_runtime.json`
records the URLs and hashes. Git excludes these downloaded files. Run the setup
command after a fresh clone. If moving an installed copy, keep tools/ with it;
the module and activation script locate STAR relative to their own files.

`config.sh` selects this installation when no module override is already set.
With SOFTWARE_MODE=modules it uses the local module. With SOFTWARE_MODE=path it
adds the checked binary directory to PATH without calling module.
An explicit `MODULE_STAR` in the environment or run_settings.sh can select another
site module. Without a local installation, the configured site module remains the
fallback. Configure and validate the runtime before submitting a new run.

For a shared installation, `--tools-dir /path/to/tools` selects another location.
Source that location's star_runtime.sh from run_settings.sh; automatic discovery
only checks tools/ beside config.sh.

The Ceres STAR 2.7.11b build inspected on September 10, 2026 had `-O0 -g3` compiler
records. The official release produced identical count tables and non-time mapping
metrics in a complete two-lane pilot and selected slow-read comparisons. This
establishes those comparisons, not equality for every possible input or platform.
Changing the build, reference, read processing or resource settings needs a new
matched-input check appropriate to that change.

Record the selected executable's checksum and version with each run. Inspect it in
a terminal from this directory:

```bash
source config.sh
load_software "$MODULE_STAR"
command -v STAR
STAR --version
sha256sum "$(command -v STAR)"
```

The pinned binary SHA-256 is:
`36e94b899a56b0ea5de5d65e722f55bc552b6713bd2d1e83a5c2abbd06c9881a`.
The activation script also checks this hash before selecting the local module.
Counts, QC, job completion and retained-file checks remain required.

Sources: [STAR release](https://github.com/alexdobin/STAR/releases/tag/2.7.11b),
[STAR source](https://github.com/alexdobin/STAR/tree/b1edc1208d91a53bf40ebae8669f71d50b994851),
[Lmod module paths](https://lmod.readthedocs.io/en/latest/100_modulefile_examples.html#relative-paths).

## Other Linux systems

Use examples/linux.sh and activate the required tools in the same terminal before
running run.sh. The numbered .slurm files are Bash scripts; local mode executes
them sequentially and records exit codes in local_jobs.json. Slurm directives are
comments when run through Bash. Local processing requires GNU tools, Bash 4+,
Python 3.11+, SAMtools and HTStream in addition to STAR.

Use the tool maintainers' installation instructions for a compatible build:
[HTStream](https://github.com/ibest/HTStream),
[SAMtools](https://www.htslib.org/download/),
[STAR](https://github.com/alexdobin/STAR).
The included installer supplies only the pinned STAR Linux x86_64 build. Other
architectures and native macOS are not covered by that binary. Container execution
has not been validated. Keep a new software environment separate until a matched
input run passes the same count, BAM and QC checks.

Other Slurm sites may use SOFTWARE_MODE=path after activating software, or set
MODULE_PYTHON, MODULE_HTSTREAM, MODULE_STAR and MODULE_SAMTOOLS to their module names.
An empty Slurm account or partition uses the site's default, when allowed.
[Slurm's sbatch reference](https://slurm.schedmd.com/sbatch.html) describes command-line
resource options and environment export.

HTStream's Ceres module also contains Python 3.10.9. In module mode, the loader
reselects the configured Python after loading other tools. In path mode, activate
Python 3.11+ last and check python3 --version. The preflight rejects older Python.
