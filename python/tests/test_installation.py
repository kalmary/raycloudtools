import subprocess
import sys

from raycloud_tools.trees import executable_path


def test_installed_command_runs_bundled_native_executable(tmp_path):
    assert executable_path().is_file()
    result = subprocess.run(
        [sys.executable, "-c", "from raycloud_tools import main; main()", "--help"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
    )

    assert result.returncode == 1
    assert "rayextract trees cloud.ply ground_mesh.ply" in result.stdout
    assert result.stderr == ""
