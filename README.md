# ECL-Plugin-OnlineGame

EuoraCraft Launcher 的联机普通插件：建房、加入、玩家管理、端口检测、NAT 检测、节点设置与联机页面。

| 项目 | 值 |
| --- | --- |
| 插件标识 | `ECL-Plugin-OnlineGame` |
| API 版本 | v2 Worker |
| 版本 | `1.0.0-beta` |
| 宿主 | [EuoraCraft Launcher](https://github.com/ECLTeam/EuoraCraft-Launcher) |

插件不声明对 `ECL-Plugin-QomicexCompatible` 的依赖：缺少它时基础联机仍可用，只是没有 QomicEX 扩展协议。

## 安装

在启动器的插件目录中放置本目录，或使用构建产物：

```bash
# 需要启动器仓库提供 ECL.plugins.package_archive
PYTHONPATH=/path/to/EuoraCraft-Launcher python package.py --download
PYTHONPATH=/path/to/EuoraCraft-Launcher python package.py
```

`--download` 按 `locks/*.txt` 校验版本与哈希，把 wheel 放到 `wheels/<目标>/`，不向宿主环境安装依赖。产物为 `output/ECL-Plugin-OnlineGame.eclplugin`。

## 开发

插件运行在启动器提供的 Worker 环境中，`ECL.plugin_api` 由宿主注入，因此本仓库不包含该 SDK：

```bash
pip install -r requirements-test.txt
PYTHONPATH=/path/to/EuoraCraft-Launcher python -m pytest --tb=short -q
ruff check .
```

原生联机能力依赖 `easytier-pyo3`，未安装时相关用例自动跳过；完整验收仍需在 Windows 启动器中实际建房、加入与退出。

## 结构

| 路径 | 内容 |
| --- | --- |
| `main.py` | 插件入口，业务命令与生命周期 |
| `onlinegame/service.py` | 联机会话、节点与端口检测 |
| `onlinegame/nodes.py` | 节点配置模型 |
| `onlinegame/extensions.py` | 联机扩展协议注册与分发 |
| `onlinegame/florolding/` | Florolding 对端实现，许可证见 `Florolding-LICENSE` |
| `ui/` | 联机页面模板与样式 |
| `locks/` | 各目标平台的二进制依赖锁 |

## 许可证

GPL-3.0，见 [LICENSE](LICENSE)。Florolding 部分遵循其原始许可证。
