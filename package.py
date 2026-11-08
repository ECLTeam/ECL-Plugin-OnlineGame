"""构建本插件的 .eclplugin 归档，并按锁文件准备二进制依赖。

打包使用宿主提供的 ECL.plugins.package_archive，因此运行前需要把启动器仓库
放在 PYTHONPATH 中，例如：

    PYTHONPATH=/path/to/EuoraCraft-Launcher python package.py --download
"""

from __future__ import annotations

import argparse
import json
import shutil
import subprocess
import sys
from pathlib import Path
from tempfile import TemporaryDirectory

from ECL.plugins.package_archive import build_plugin_package

plugin_root = Path(__file__).resolve().parent
staging_ignore = shutil.ignore_patterns("__pycache__", "*.pyc", ".git", ".github", "output", "tests", "wheels")


def download_wheels(target_name: str | None) -> None:
    """
    只下载锁文件中已固定版本和哈希的二进制依赖，不向宿主环境安装。

    :param target_name: 只准备指定目标；省略时处理全部锁文件
    """
    for lock_path in sorted((plugin_root / "locks").glob("*.txt")):
        if target_name is not None and lock_path.stem != target_name:
            continue
        python_version = lock_path.stem.rsplit("-cp", 1)[1]
        platforms = (
            ("win_amd64",)
            if lock_path.stem.startswith("windows-")
            else ("manylinux_2_28_x86_64", "manylinux_2_17_x86_64", "manylinux2014_x86_64")
        )
        subprocess.run(
            [
                sys.executable,
                "-m",
                "pip",
                "download",
                "--only-binary=:all:",
                "--require-hashes",
                "--no-deps",
                "--implementation=cp",
                f"--python-version={python_version}",
                f"--abi=cp{python_version}",
                *(f"--platform={platform}" for platform in platforms),
                "--dest",
                str(plugin_root / "wheels" / lock_path.stem),
                "--requirement",
                str(lock_path),
            ],
            check=True,
        )


def main() -> int:
    """
    生成插件归档；缺少 wheel 时先提示准备依赖。

    :return: 成功为 0
    """
    parser = argparse.ArgumentParser(description="构建 ECL-Plugin-OnlineGame")
    parser.add_argument("--output", type=Path, default=plugin_root / "output")
    parser.add_argument("--download", action="store_true", help="按锁文件下载 Windows/Linux 的二进制依赖")
    parser.add_argument(
        "--download-target",
        choices=("windows-x86_64-cp311", "windows-x86_64-cp312", "linux-x86_64-cp312"),
        help="只准备指定目标的依赖，需同时使用 --download",
    )
    arguments = parser.parse_args()
    if arguments.download_target is not None and not arguments.download:
        parser.error("--download-target 需要同时使用 --download")
    if arguments.download:
        download_wheels(arguments.download_target)
    metadata = json.loads((plugin_root / "plugin.json").read_text(encoding="utf-8"))
    if metadata.get("pythonDependencies") and not any((plugin_root / "wheels").glob("*/*.whl")):
        parser.error("尚未准备 wheel，请先使用 --download")
    arguments.output.mkdir(parents=True, exist_ok=True)
    with TemporaryDirectory(prefix="ecl-plugin-") as staging_directory:
        staging_path = Path(staging_directory) / metadata["name"]
        shutil.copytree(plugin_root, staging_path, ignore=staging_ignore)
        archive_path = arguments.output / f"{metadata['name']}.eclplugin"
        build_plugin_package(staging_path, archive_path)
    print(f"插件包已校验：{archive_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
