"""Tests for the project generator."""

import tempfile
from pathlib import Path
import pytest

from project_generator.config import Config
from project_generator.generator import ProjectGenerator


def test_config_loading():
    """Test configuration loading with defaults."""
    config = Config.load()
    assert config.get("python_version") == ">=3.11"
    assert "standard" in config.get("templates", {})


def test_project_generation_dry_run(tmp_path):
    """Test project generation in dry-run mode."""
    config = Config.load()
    generator = ProjectGenerator(config)
    
    success = generator.generate(
        project_name="test-project",
        author="Test Author",
        email="test@example.com",
        template="minimal",
        tool="poetry",
        output_dir=tmp_path,
        dry_run=True
    )
    
    assert success
    # In dry-run mode, no files should be created
    assert not (tmp_path / "test-project").exists()


def test_project_generation_real(tmp_path):
    """Test actual project generation."""
    config = Config.load()
    generator = ProjectGenerator(config)
    
    success = generator.generate(
        project_name="test-project",
        author="Test Author",
        email="test@example.com",
        template="minimal",
        tool="poetry",
        output_dir=tmp_path,
        dry_run=False
    )
    
    assert success
    
    project_dir = tmp_path / "test-project"
    assert project_dir.exists()
    assert (project_dir / "README.md").exists()
    assert (project_dir / ".gitignore").exists()
    assert (project_dir / "pyproject.toml").exists()
    assert (project_dir / "src" / "test_project").exists()


def test_template_validation():
    """Test template validation."""
    config = Config.load()
    generator = ProjectGenerator(config)
    
    # Valid template should work
    success = generator.generate(
        project_name="test-project",
        author="Test Author",
        email="test@example.com",
        template="standard",
        dry_run=True
    )
    assert success
    
    # Invalid template should fail
    success = generator.generate(
        project_name="test-project",
        author="Test Author",
        email="test@example.com",
        template="nonexistent",
        dry_run=True
    )
    assert not success
