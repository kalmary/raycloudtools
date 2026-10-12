import os
import subprocess
from pathlib import Path


def run_trees(
    cloud_path: str | os.PathLike[str],
    ground_path: str | os.PathLike[str],
    *,
    height_min: float,
    max_diameter: float,
    crop_length: float,
    distance_limit: float,
    girth_height_ratio: float,
    gravity_factor: float,
    global_taper: float | None = None,
    global_taper_factor: float | None = None,
    grid_width: float | None = None,
    use_rays: bool = False,
    segment_branches: bool = False,
    workdir: str | os.PathLike[str] | None = None,
) -> Path:
    cloud_path = Path(cloud_path)
    command = [
        "rayextract",
        "trees",
        os.fspath(cloud_path),
        os.fspath(ground_path),
        "--height_min",
        str(height_min),
        "--max_diameter",
        str(max_diameter),
        "--crop_length",
        str(crop_length),
        "--distance_limit",
        str(distance_limit),
        "--girth_height_ratio",
        str(girth_height_ratio),
        "--gravity_factor",
        str(gravity_factor),
    ]
    if global_taper is not None:
        command.extend(("--global_taper", str(global_taper)))
    if global_taper_factor is not None:
        command.extend(("--global_taper_factor", str(global_taper_factor)))
    if grid_width is not None:
        command.extend(("--grid_width", str(grid_width)))
    if use_rays:
        command.append("--use_rays")
    if segment_branches:
        command.append("--branch_segmentation")

    result = subprocess.run(
        command,
        capture_output=True,
        text=True,
        cwd=workdir,
        check=False,
    )
    if result.returncode != 0:
        raise RuntimeError(
            f"rayextract failed (exit {result.returncode}):\n"
            f"{result.stdout or ''}{result.stderr or '(no output)'}"
        )

    return cloud_path.with_name(f"{cloud_path.stem}_segmented.ply")
