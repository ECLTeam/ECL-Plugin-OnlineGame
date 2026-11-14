# ============================================================
# EuoraCraft Launcher
# ECLTeam © 2026 GPL-3.0 License
# https://github.com/ECLTeam/EuoraCraft-Launcher
#
# 文件作用：插件入口模块的导入冒烟测试。
#
# 公开接口：
#   - test_entry_module_imports() -> None
#   - test_remote_extensions_module_imports() -> None
# ============================================================

from __future__ import annotations

import main
import onlinegame.remote_extensions


def test_entry_module_imports() -> None:
    """
    宿主加载入口走 import 链路；SDK 路径漂移（如 ECL.plugin_api 旧路径）必须在本仓库 CI 被拦截。
    """
    assert main.Plugin.__name__ == "Plugin"


def test_remote_extensions_module_imports() -> None:
    """
    remote_extensions 与入口共享 SDK 导入路径，漂移同样会在启用时刻以 PLUGIN_ENABLE_FAILED 暴露。
    """
    assert onlinegame.remote_extensions.RemoteExtensions is not None
