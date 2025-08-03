"""Template rendering for project files."""

from typing import Any


class TemplateRenderer:
    """Renders project file templates."""

    def __init__(self, config: Any) -> None:
        """Initialize renderer with configuration."""
        self.config = config

    def render_file(
        self, file_type: str, context: dict, template_config: dict, tool: str
    ) -> str:
        """Render a file template with the given context."""

        # Always render pyproject.toml
        if file_type not in [
            "gitignore",
            "readme",
            "makefile",
            "main",
            "cli_main",
            "web_main",
            "test",
        ]:
            file_type = "pyproject"

        method_name = f"_render_{file_type}"
        if hasattr(self, method_name):
            return str(getattr(self, method_name)(context, template_config, tool))
        else:
            raise ValueError(f"Unknown file type: {file_type}")

    def _render_gitignore(self, context: dict, template_config: dict, tool: str) -> str:
        """Render .gitignore file."""
        return """__pycache__/
*.pyc
*.pyo
*.pyd
.Python
env/
pip-log.txt
pip-delete-this-directory.txt
.tox
.coverage
.coverage.*
.cache
nosetests.xml
coverage.xml
*.cover
*.log
.git
.mypy_cache
.pytest_cache
.hypothesis

.DS_Store
.vscode/
.idea/

.env
.venv/
venv/
ENV/

dist/
build/
*.egg-info/
*.egg

.pdm-python
.pdm-build/
"""

    def _render_readme(self, context: dict, template_config: dict, tool: str) -> str:
        """Render README.md file."""
        project_name = context["project_name"]
        description = context["description"]
        package_name = context["package_name"]

        install_cmd = "poetry install" if tool == "poetry" else "uv sync"
        run_cmd = (
            f"poetry run python -m {package_name}"
            if tool == "poetry"
            else f"uv run python -m {package_name}"
        )

        return f"""# {project_name}

{description}

## Installation

```bash
{install_cmd}
```

## Usage

```bash
{run_cmd}
```

## Development

```bash
# Install dependencies
{install_cmd}

# Run tests
make test

# Format code
make lint
```

## License

MIT License
"""

    def _render_makefile(self, context: dict, template_config: dict, tool: str) -> str:
        """Render Makefile."""
        if tool == "poetry":
            return """install:
\tpoetry install

lint:
\tpoetry run black src tests
\tpoetry run mypy src

test:
\tpoetry run pytest

clean:
\tfind . -type f -name "*.pyc" -delete
\tfind . -type d -name "__pycache__" -delete

.PHONY: install lint test clean
"""
        else:  # uv
            return """install:
\tuv sync

lint:
\tuv run black src tests
\tuv run mypy src

test:
\tuv run pytest

clean:
\tfind . -type f -name "*.pyc" -delete
\tfind . -type d -name "__pycache__" -delete

.PHONY: install lint test clean
"""

    def _render_main(self, context: dict, template_config: dict, tool: str) -> str:
        """Render main.py file."""
        return """def main():
    \"\"\"Main entry point.\"\"\"
    print("Hello from main!")


if __name__ == "__main__":
    main()
"""

    def _render_cli_main(self, context: dict, template_config: dict, tool: str) -> str:
        """Render CLI main file."""
        return """import click


@click.command()
@click.option('--name', default='World', help='Name to greet.')
def main(name):
    \"\"\"Simple CLI application.\"\"\"
    click.echo(f'Hello {name}!')


if __name__ == '__main__':
    main()
"""

    def _render_web_main(self, context: dict, template_config: dict, tool: str) -> str:
        """Render web application main file."""
        return """from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/health")
async def health():
    return {"status": "healthy"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
"""

    def _render_test(self, context: dict, template_config: dict, tool: str) -> str:
        """Render test file."""
        package_name = context["package_name"]

        # Determine what to import based on template
        if "cli_main" in template_config.get("files", []):
            import_line = f"from {package_name}.cli import main"
            test_content = '''def test_main():
    """Test CLI main function."""
    from click.testing import CliRunner
    runner = CliRunner()
    result = runner.invoke(main, ['--name', 'Test'])
    assert result.exit_code == 0
    assert 'Hello Test!' in result.output'''
        elif "web_main" in template_config.get("files", []):
            import_line = f"from {package_name}.app import app"
            test_content = '''def test_root():
    """Test web app root endpoint."""
    from fastapi.testclient import TestClient
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert response.json() == {"message": "Hello World"}'''
        else:
            import_line = f"from {package_name}.main import main"
            test_content = '''def test_main(capsys):
    """Test main function."""
    main()
    captured = capsys.readouterr()
    assert "Hello" in captured.out'''

        return f"""{import_line}


{test_content}
"""

    def _render_pyproject(self, context: dict, template_config: dict, tool: str) -> str:
        """Render pyproject.toml file."""
        project_name = context["project_name"]
        package_name = context["package_name"]
        author = context["author"]
        email = context["email"]
        description = context["description"]
        python_version = context["python_version"]

        dependencies = template_config.get("dependencies", [])
        dev_deps = template_config.get("dev_dependencies", {}).get(tool, [])

        if tool == "poetry":
            return self._render_poetry_pyproject(
                project_name,
                package_name,
                author,
                email,
                description,
                python_version,
                dependencies,
                dev_deps,
            )
        else:  # uv
            return self._render_uv_pyproject(
                project_name,
                package_name,
                author,
                email,
                description,
                python_version,
                dependencies,
                dev_deps,
            )

    def _render_poetry_pyproject(
        self,
        project_name: str,
        package_name: str,
        author: str,
        email: str,
        description: str,
        python_version: str,
        dependencies: list,
        dev_deps: list,
    ) -> str:
        """Render Poetry pyproject.toml."""
        deps_str = (
            "\n".join([f'"{dep}"' for dep in dependencies]) if dependencies else ""
        )
        dev_deps_str = "\n".join([f'{dep.split("^")[0]} = "{dep}"' for dep in dev_deps])

        return f"""[tool.poetry]
name = "{package_name}"
version = "0.1.0"
description = "{description}"
authors = ["{author} <{email}>"]
readme = "README.md"
packages = [{{include = "{package_name}", from = "src"}}]

[tool.poetry.dependencies]
python = "{python_version}"
{deps_str}

[tool.poetry.group.dev.dependencies]
{dev_deps_str}

[build-system]
requires = ["poetry-core>=1.0.0"]
build-backend = "poetry.core.masonry.api"

[tool.black]
line-length = 88
target-version = ['py311']

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
"""

    def _render_uv_pyproject(
        self,
        project_name: str,
        package_name: str,
        author: str,
        email: str,
        description: str,
        python_version: str,
        dependencies: list,
        dev_deps: list,
    ) -> str:
        """Render uv pyproject.toml."""
        deps_str = (
            "\n".join([f'    "{dep}",' for dep in dependencies]) if dependencies else ""
        )
        dev_deps_str = "\n".join([f'    "{dep}",' for dep in dev_deps])

        return f"""[project]
name = "{package_name}"
version = "0.1.0"
description = "{description}"
authors = [
    {{name = "{author}", email = "{email}"}}
]
readme = "README.md"
requires-python = "{python_version}"
dependencies = [
{deps_str}
]

[project.optional-dependencies]
dev = [
{dev_deps_str}
]

[build-system]
requires = ["hatchling"]
build-backend = "hatchling.build"

[tool.uv]
dev-dependencies = [
{dev_deps_str}
]

[tool.black]
line-length = 88
target-version = ['py311']

[tool.mypy]
python_version = "3.11"
warn_return_any = true
warn_unused_configs = true
"""
