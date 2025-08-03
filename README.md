# Python Project Generator

A configurable, extensible Python project generator that supports multiple templates and dependency management tools.

## Features

- **Multiple Templates**: Standard, minimal, CLI, and web application templates
- **Tool Support**: Both Poetry and uv dependency managers
- **Configurable**: YAML configuration files and CLI arguments
- **Extensible**: Plugin-ready architecture for future tools
- **Modern**: Follows current Python packaging best practices
- **Tested**: Includes test structure and configuration

## Installation

```bash
# Install from source
git clone https://github.com/yourusername/project-generator.git
cd project-generator
poetry install

# Or install globally
poetry build
pip install dist/*.whl
```

## Quick Start

```bash
# Generate a standard Python project
project-generator my-awesome-project

# Generate with specific template and tool
project-generator my-cli-app --template cli --tool uv

# Use custom configuration
project-generator my-project --config my-config.yaml
```

## Templates

- **standard**: Full-featured project with common dependencies and tools
- **minimal**: Lightweight project with basic structure
- **cli**: Command-line application with Click
- **web**: Web application with FastAPI

## Configuration

Create a `config.yaml` file to customize defaults:

```yaml
author:
  name: "Your Name"
  email: "your.email@example.com"

templates:
  standard:
    dependencies:
      - "requests>=2.31.0"
      - "click>=8.0.0"
    dev_dependencies:
      poetry:
        - "pytest^7.4.0"
        - "black^24.0.0"
```

## CLI Options

```
usage: project-generator [-h] [--author AUTHOR] [--email EMAIL] 
                        [--description DESCRIPTION] [--template {standard,minimal,cli,web}]
                        [--tool {poetry,uv}] [--config CONFIG] [--output-dir OUTPUT_DIR]
                        [--force] [--dry-run] [--version]
                        project_name

Generate Python project structures with configurable templates

positional arguments:
  project_name          Name of the project to create

optional arguments:
  -h, --help            show this help message and exit
  --author AUTHOR       Project author name
  --email EMAIL         Project author email
  --description DESCRIPTION
                        Project description
  --template {standard,minimal,cli,web}
                        Project template to use (default: standard)
  --tool {poetry,uv}    Dependency management tool (default: poetry)
  --config CONFIG       Path to configuration file
  --output-dir OUTPUT_DIR
                        Output directory for the project
  --force               Overwrite existing project directory
  --dry-run             Show what would be created without creating files
  --version             show program's version number and exit
```

## Development

```bash
# Clone the repository
git clone https://github.com/yourusername/project-generator.git
cd project-generator

# Install dependencies
poetry install

# Run tests
make test

# Format code
make lint

# Run the generator locally
poetry run project-generator --help
```

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Add tests for your changes
5. Run the test suite (`make test`)
6. Commit your changes (`git commit -m 'Add amazing feature'`)
7. Push to the branch (`git push origin feature/amazing-feature`)
8. Open a Pull Request

## Roadmap

- [ ] Plugin system for custom templates
- [ ] Support for additional tools (pip-tools, pipenv, etc.)
- [ ] Interactive template selection
- [ ] Template validation and testing
- [ ] GitHub Actions workflow templates
- [ ] Docker support

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Inspired by modern Python packaging practices
- Built with Poetry and designed for the Python community
