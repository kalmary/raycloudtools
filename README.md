# Raycloudtools fork for BRIK

This is the BRIK fork of
[CSIRO Raycloudtools](https://github.com/csiro-robotics/raycloudtools), kept in
sync with the upstream C++ project and extended with a small Python wrapper.
The repository is used as a nested submodule of Tree-Clustering:

```text
git@github.com:kalmary/raycloudtools.git
```

Clone it with its pinned build dependency:

```bash
git clone --recurse-submodules git@github.com:kalmary/raycloudtools.git
```

## Native build

Initialize the pinned build dependency first:

```bash
git submodule update --init --recursive
```

On Ubuntu, install `build-essential`, `cmake`, and `libeigen3-dev`, then follow
the source-build stages in `docker/Dockerfile` or the BRIK composition
Dockerfile.

On Apple Silicon or Intel macOS, install the compatible dependencies and run
the verified build helper:

```bash
brew install cmake eigen@3 libomp
./scripts/build_macos.sh
```

Add the reported executable directory to `PATH` and the reported library
directory to `DYLD_LIBRARY_PATH`. BRIK uses only the following workflow:

```bash
rayextract trees cloud.ply ground.ply
```

The BRIK Dockerfile performs the Linux build directly from the checked-out
fork. Its multi-architecture base builds natively on Linux and with Docker
Desktop on Intel or Apple Silicon macOS.

## Python wrapper

The Python package is intentionally limited to the tree-extraction command.
Install it from this checkout:

```bash
uv sync --group basic
```

Then call the installed `rayextract` executable through Python:

```python
from pathlib import Path

from raycloud_tools import run_trees

output_path = run_trees(
    Path("cloud.ply"),
    Path("ground.ply"),
    height_min=1.0,
    max_diameter=0.9,
    crop_length=0.1,
    distance_limit=0.2,
    girth_height_ratio=0.4,
    gravity_factor=0.3,
)
```

`run_trees()` forwards the supported options, runs the command in the supplied
working directory, raises `RuntimeError` when it fails, and returns the expected
`*_segmented.ply` path. It does not start containers or manage temporary files.

Run the focused wrapper tests with:

```bash
uv sync --group test
uv run --group test pytest python/tests
```

Upstream license and attribution files remain unchanged.
