from pathlib import Path
from subprocess import CompletedProcess

import pytest

from raycloud_tools import run_trees


def test_run_trees_builds_supported_command(monkeypatch, tmp_path):
    recorded = {}

    def run(command, **kwargs):
        recorded["command"] = command
        recorded["kwargs"] = kwargs
        return CompletedProcess(command, 0, "", "")

    monkeypatch.setattr("raycloud_tools.trees.subprocess.run", run)

    output = run_trees(
        tmp_path / "cloud.ply",
        tmp_path / "ground.ply",
        height_min=2.0,
        max_diameter=0.9,
        crop_length=1.0,
        distance_limit=0.3,
        girth_height_ratio=0.12,
        gravity_factor=0.75,
        global_taper=0.024,
        use_rays=True,
        segment_branches=True,
        workdir=tmp_path,
    )

    assert recorded["command"] == [
        "rayextract",
        "trees",
        str(tmp_path / "cloud.ply"),
        str(tmp_path / "ground.ply"),
        "--height_min",
        "2.0",
        "--max_diameter",
        "0.9",
        "--crop_length",
        "1.0",
        "--distance_limit",
        "0.3",
        "--girth_height_ratio",
        "0.12",
        "--gravity_factor",
        "0.75",
        "--global_taper",
        "0.024",
        "--use_rays",
        "--branch_segmentation",
    ]
    assert recorded["kwargs"]["cwd"] == tmp_path
    assert output == tmp_path / "cloud_segmented.ply"


def test_run_trees_reports_process_failure(monkeypatch):
    def run(command, **kwargs):
        return CompletedProcess(command, 3, "output", "error")

    monkeypatch.setattr("raycloud_tools.trees.subprocess.run", run)

    with pytest.raises(RuntimeError, match=r"rayextract failed \(exit 3\)"):
        run_trees(
            Path("cloud.ply"),
            Path("ground.ply"),
            height_min=2.0,
            max_diameter=0.9,
            crop_length=1.0,
            distance_limit=0.3,
            girth_height_ratio=0.12,
            gravity_factor=0.75,
        )
