"""Core project generation logic."""

import os
import shutil
import subprocess
from pathlib import Path
from typing import Dict, Any, Optional

from .config import Config
from .templates import TemplateRenderer


class ProjectGenerator:
    """Main project generator class."""
    
    def __init__(self, config: Config):
        """Initialize generator with configuration."""
        self.config = config
        self.renderer = TemplateRenderer(config)
    
    def generate(
        self,
        project_name: str,
        author: Optional[str] = None,
        email: Optional[str] = None,
        description: Optional[str] = None,
        template: str = "standard",
        tool: str = "poetry",
        output_dir: Path = Path.cwd(),
        force: bool = False,
        dry_run: bool = False
    ) -> bool:
        """Generate a new Python project."""
        
        # Sanitize project name
        project_name = project_name.strip().replace(" ", "_")
        package_name = project_name.lower().replace("-", "_")
        
        # Get author info
        author_info = self.config.get_author_info()
        if not author:
            author = self._prompt_if_needed("Author name", author_info.get("name", ""))
        if not email:
            email = self._prompt_if_needed("Author email", author_info.get("email", ""))
        
        if not description:
            description = f"A Python project generated with project-generator"
        
        # Create project context
        context = {
            "project_name": project_name,
            "package_name": package_name,
            "author": author,
            "email": email,
            "description": description,
            "tool": tool,
            "python_version": self.config.get("python_version", ">=3.11")
        }
        
        # Get template configuration
        try:
            template_config = self.config.get_template(template)
        except ValueError as e:
            print(f"❌ {e}")
            return False
        
        # Setup project directory
        project_dir = output_dir / project_name
        
        if project_dir.exists():
            if not force:
                print(f"❌ Project directory '{project_dir}' already exists. Use --force to overwrite.")
                return False
            elif not dry_run:
                shutil.rmtree(project_dir)
        
        if dry_run:
            print(f"🔍 Dry run - would create project '{project_name}' in '{project_dir}'")
            print(f"📋 Template: {template} ({template_config.get('description', 'No description')})")
            print(f"🔧 Tool: {tool}")
            print(f"👤 Author: {author} <{email}>")
            print("\n📁 Files that would be created:")
        else:
            print(f"🚀 Creating project '{project_name}' in '{project_dir}'")
            project_dir.mkdir(parents=True, exist_ok=True)
        
        # Create project structure
        success = self._create_project_structure(
            project_dir, context, template_config, tool, dry_run
        )
        
        if success and not dry_run:
            # Initialize git repository
            self._init_git_repo(project_dir)
            
            print(f"✅ Project '{project_name}' created successfully!")
            print(f"📁 Location: {project_dir}")
            print(f"\n🎯 Next steps:")
            print(f"   cd {project_name}")
            if tool == "poetry":
                print(f"   poetry install")
            else:  # uv
                print(f"   uv sync")
            print(f"   make test")
            print(f"   git add . && git commit -m 'Initial commit'")
        
        return success
    
    def _prompt_if_needed(self, prompt: str, default: str) -> str:
        """Prompt user for input if default is not suitable."""
        if not default or default in ["Your Name", "your.email@example.com"]:
            try:
                value = input(f"{prompt}: ").strip()
                return value if value else default
            except (EOFError, KeyboardInterrupt):
                return default
        return default
    
    def _create_project_structure(
        self,
        project_dir: Path,
        context: Dict[str, Any],
        template_config: Dict[str, Any],
        tool: str,
        dry_run: bool
    ) -> bool:
        """Create the project directory structure and files."""
        
        package_name = context["package_name"]
        
        # Create directories
        directories = [
            f"src/{package_name}",
            "tests"
        ]
        
        for dir_path in directories:
            full_dir = project_dir / dir_path
            if dry_run:
                print(f"   📁 {dir_path}/")
            else:
                full_dir.mkdir(parents=True, exist_ok=True)
        
        # Generate files based on template
        files_to_create = template_config.get("files", [])
        
        # Always include pyproject.toml
        if "pyproject" not in files_to_create:
            files_to_create = files_to_create + ["pyproject"]
        
        for file_type in files_to_create:
            try:
                file_content = self.renderer.render_file(
                    file_type, context, template_config, tool
                )
                
                # Determine file path
                file_path = self._get_file_path(file_type, context)
                full_path = project_dir / file_path
                
                if dry_run:
                    print(f"   📄 {file_path}")
                else:
                    # Ensure parent directory exists
                    full_path.parent.mkdir(parents=True, exist_ok=True)
                    
                    with open(full_path, 'w') as f:
                        f.write(file_content)
                        
            except Exception as e:
                print(f"❌ Error creating {file_type}: {e}")
                return False
        
        return True
    
    def _get_file_path(self, file_type: str, context: Dict[str, Any]) -> str:
        """Get the file path for a given file type."""
        package_name = context["package_name"]
        
        file_paths = {
            "gitignore": ".gitignore",
            "readme": "README.md",
            "makefile": "Makefile",
            "main": f"src/{package_name}/main.py",
            "cli_main": f"src/{package_name}/cli.py",
            "web_main": f"src/{package_name}/app.py",
            "test": "tests/test_main.py",
            "pyproject": "pyproject.toml"
        }
        
        # Always include pyproject.toml
        if file_type not in file_paths:
            file_paths[file_type] = f"{file_type}"
        
        return file_paths.get(file_type, file_type)
    
    def _init_git_repo(self, project_dir: Path) -> None:
        """Initialize a git repository in the project directory."""
        try:
            # Check if git is available
            subprocess.run(["git", "--version"], 
                         capture_output=True, check=True, cwd=project_dir)
            
            # Initialize git repo
            subprocess.run(["git", "init"], 
                         capture_output=True, check=True, cwd=project_dir)
            
            print("🔧 Initialized git repository")
            
        except (subprocess.CalledProcessError, FileNotFoundError):
            print("⚠️  Git not available - skipping repository initialization")
