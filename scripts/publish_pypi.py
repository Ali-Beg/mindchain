#!/usr/bin/env python
"""
PyPI Deployment Script

This script helps publish the MindChain project to PyPI.
It handles version increments, building, and publishing.

Prerequisites:
1. Poetry installed
2. PyPI API token configured (via .env file or environment variable)

Usage:
    python scripts/publish_pypi.py --bump patch|minor|major
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def run_command(command, description=None):
    """Run a shell command and print its output."""
    if description:
        print(f"\n{description}...")
    
    result = subprocess.run(
        command, 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    if result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False, result.stderr
    
    if result.stdout:
        print(result.stdout)
    
    return True, result.stdout

def publish_to_pypi(repo_path, bump_type):
    """Publish the project to PyPI."""
    # Ensure we're in the project root directory
    os.chdir(repo_path)
    
    # Check if PYPI_API_TOKEN is set
    pypi_token = os.environ.get('PYPI_API_TOKEN')
    if not pypi_token:
        print("Error: PYPI_API_TOKEN environment variable not set.")
        print("Please set it in a .env file or directly in your environment.")
        return False
    
    # Configure Poetry with PyPI token
    success, _ = run_command(
        f"poetry config pypi-token.pypi {pypi_token}",
        "Configuring Poetry with PyPI token"
    )
    if not success:
        return False
    
    # Bump the version if requested
    if bump_type:
        success, _ = run_command(
            f"poetry version {bump_type}",
            f"Bumping {bump_type} version"
        )
        if not success:
            return False
    
    # Get the current version
    success, version_output = run_command(
        "poetry version",
        "Getting current version"
    )
    if not success:
        return False
    
    # Extract the version number
    current_version = version_output.split()[1]
    
    # Build the package
    success, _ = run_command(
        "poetry build",
        "Building package"
    )
    if not success:
        return False
    
    # Publish to PyPI
    success, _ = run_command(
        "poetry publish",
        "Publishing to PyPI"
    )
    if not success:
        return False
    
    print(f"\nSuccess! Published MindChain v{current_version} to PyPI.")
    print("The package should be available at https://pypi.org/project/mindchain/")
    return True

def main():
    parser = argparse.ArgumentParser(description="Publish MindChain to PyPI")
    parser.add_argument(
        "--bump", 
        choices=["patch", "minor", "major"], 
        help="Bump the version (patch, minor, or major)"
    )
    args = parser.parse_args()
    
    # Get the absolute path to the project root
    repo_path = Path(__file__).parent.parent.absolute()
    
    print(f"Publishing MindChain to PyPI")
    print(f"Project path: {repo_path}")
    
    # Get the current version
    os.chdir(repo_path)
    success, version_output = run_command("poetry version", "Current version")
    if not success:
        return
    
    # Confirm with user
    if args.bump:
        print(f"This will bump the {args.bump} version and publish to PyPI.")
    else:
        print(f"This will publish the current version to PyPI.")
    
    response = input("Continue with publishing? [y/N]: ")
    if response.lower() != 'y':
        print("Publishing cancelled.")
        return
    
    # Run publish
    publish_to_pypi(repo_path, args.bump)

if __name__ == "__main__":
    main()