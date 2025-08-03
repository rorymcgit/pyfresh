"""Configuration management for the Python Project Generator."""

import os
from pathlib import Path
from typing import Dict, Any, Optional
import yaml


class Config:
    """Configuration manager for project generator."""
    
    DEFAULT_CONFIG = {
        "author": {
            "name": "Your Name",
            "email": "your.email@example.com"
        },
        "templates": {
            "standard": {
                "description": "Standard Python project with common tools",
                "dependencies": ["pandas>=2.3.1,<3.0.0"],
                "dev_dependencies": {
                    "poetry": ["pytest^7.4.0", "black^24.0.0", "mypy^1.8.0"],
                    "uv": ["pytest>=7.4.0", "black>=24.0.0", "mypy>=1.8.0"]
                },
                "files": ["gitignore", "readme", "makefile", "main", "test"]
            },
            "minimal": {
                "description": "Minimal Python project structure",
                "dependencies": [],
                "dev_dependencies": {
                    "poetry": ["pytest^7.4.0"],
                    "uv": ["pytest>=7.4.0"]
                },
                "files": ["gitignore", "readme", "main"]
            },
            "cli": {
                "description": "CLI application template",
                "dependencies": ["click>=8.0.0"],
                "dev_dependencies": {
                    "poetry": ["pytest^7.4.0", "black^24.0.0"],
                    "uv": ["pytest>=7.4.0", "black>=24.0.0"]
                },
                "files": ["gitignore", "readme", "makefile", "cli_main", "test"]
            },
            "web": {
                "description": "Web application template",
                "dependencies": ["fastapi>=0.100.0", "uvicorn>=0.20.0"],
                "dev_dependencies": {
                    "poetry": ["pytest^7.4.0", "black^24.0.0", "httpx^0.24.0"],
                    "uv": ["pytest>=7.4.0", "black>=24.0.0", "httpx>=0.24.0"]
                },
                "files": ["gitignore", "readme", "makefile", "web_main", "test"]
            }
        },
        "python_version": ">=3.11"
    }
    
    def __init__(self, data: Dict[str, Any]):
        """Initialize configuration with data."""
        self.data = data
    
    @classmethod
    def load(cls, config_path: Optional[Path] = None) -> "Config":
        """Load configuration from file or use defaults."""
        config_data = cls.DEFAULT_CONFIG.copy()
        
        if config_path and config_path.exists():
            with open(config_path, 'r') as f:
                user_config = yaml.safe_load(f)
                if user_config:
                    cls._deep_merge(config_data, user_config)
        
        # Override with environment variables
        if os.getenv("PROJECT_AUTHOR_NAME"):
            config_data["author"]["name"] = os.getenv("PROJECT_AUTHOR_NAME")
        if os.getenv("PROJECT_AUTHOR_EMAIL"):
            config_data["author"]["email"] = os.getenv("PROJECT_AUTHOR_EMAIL")
        
        return cls(config_data)
    
    @staticmethod
    def _deep_merge(base: Dict[str, Any], override: Dict[str, Any]) -> None:
        """Deep merge override dict into base dict."""
        for key, value in override.items():
            if key in base and isinstance(base[key], dict) and isinstance(value, dict):
                Config._deep_merge(base[key], value)
            else:
                base[key] = value
    
    def get(self, key: str, default: Any = None) -> Any:
        """Get configuration value by dot notation key."""
        keys = key.split('.')
        value = self.data
        
        for k in keys:
            if isinstance(value, dict) and k in value:
                value = value[k]
            else:
                return default
        
        return value
    
    def get_template(self, template_name: str) -> Dict[str, Any]:
        """Get template configuration."""
        templates = self.get("templates", {})
        if template_name not in templates:
            raise ValueError(f"Unknown template: {template_name}")
        return templates[template_name]
    
    def get_author_info(self) -> Dict[str, str]:
        """Get author information."""
        return self.get("author", {})
    
    def save_example_config(self, path: Path) -> None:
        """Save an example configuration file."""
        with open(path, 'w') as f:
            yaml.dump(self.DEFAULT_CONFIG, f, default_flow_style=False, indent=2)
