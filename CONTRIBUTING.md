Contributing

感谢你为本项目贡献代码！本文件提供本地开发、代码规范和 PR 流程的快速指南。

快速开始

1. 环境
   - 推荐使用虚拟环境：

     ```bash
     python3 -m venv .venv
     source .venv/bin/activate
     pip install --upgrade pip
     pip install -r requirements.txt
     pip install -r requirements-dev.txt
     ```

2. 代码风格
   - 使用 `flake8` 进行风格检查。
   - 使用 `mypy` 做静态类型检查（可选，但推荐）。

3. 测试
   - 单元测试使用 `pytest`。本仓库中的 `tests/` 包含示例和如何 mock 硬件的测试。
   - 运行测试：

     ```bash
     pytest
     ```

4. 提交 PR
   - 新功能分支命名：`feature/<描述>`。
   - 修复命名：`bugfix/<描述>`。
   - 提交前请确保：
     - 本地运行了相关单元测试
     - 运行了 linter（`flake8`）
     - 在 PR 描述中写明改动目的与测试方法

5. CI
   - 项目使用 GitHub Actions（示例）在 PR/Push 时自动运行 lint 与 tests。

谢谢你！
