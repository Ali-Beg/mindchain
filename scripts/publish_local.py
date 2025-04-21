#!/usr/bin/env python
"""
Local PyPI Deployment Script

This script helps publish the MindChain project to PyPI directly from your local machine.
It runs the tests first to make sure everything passes.

Prerequisites:
1. Poetry installed
2. PyPI API token configured (via .env file or environment variable)

Usage:
    python scripts/publish_local.py --no-tests      # Skip running tests
    python scripts/publish_local.py --bump patch    # Bump patch version
    python scripts/publish_local.py --bump minor    # Bump minor version
    python scripts/publish_local.py --bump major    # Bump major version
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def run_command(command, description=None, check=True):
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
    
    if check and result.returncode != 0:
        print(f"Error: {result.stderr}")
        return False, result.stderr
    
    if result.stdout:
        print(result.stdout)
    
    return True, result.stdout

def publish_to_pypi(project_root, bump_type=None, skip_tests=False):
    """Publish the project to PyPI."""
    # Ensure we're in the project root directory
    os.chdir(project_root)
    
    # Check if PYPI_API_TOKEN is set
    pypi_token = os.environ.get('PYPI_API_TOKEN')
    if not pypi_token:
        print("Error: PYPI_API_TOKEN environment variable not set.")
        print("Please set it in a .env file or directly in your environment.")
        return False
    
    # Run tests first if not skipped
    if not skip_tests:
        print("Running tests before publishing...")
        success, _ = run_command("poetry run pytest", "Running tests")
        if not success:
            print("Tests failed. Aborting publish.")
            return False
        print("All tests passed!")
    
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
    
    # Commit and tag the version in git if requested
    git_tag = input(f"Would you like to commit and tag this version (v{current_version}) in git? [y/N]: ")
    if git_tag.lower() == 'y':
        # Add and commit the changes
        run_command('git add pyproject.toml', "Adding pyproject.toml to git", check=False)
        run_command(f'git commit -m "Bump version to {current_version}"', "Committing version change", check=False)
        
        # Create a tag
        run_command(f'git tag -a v{current_version} -m "Version {current_version}"', 
                    f"Creating git tag v{current_version}", check=False)
        
        # Ask about pushing
        git_push = input("Would you like to push the commits and tags to origin? [y/N]: ")
        if git_push.lower() == 'y':
            run_command('git push origin main', "Pushing commits", check=False)
            run_command('git push origin --tags', "Pushing tags", check=False)
    
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
    parser.add_argument(
        "--no-tests",
        action="store_true",
        help="Skip running tests before publishing"
    )
    args = parser.parse_args()
    
    # Get the absolute path to the project root
    project_root = Path(__file__).parent.parent.absolute()
    
    print(f"Publishing MindChain to PyPI")
    print(f"Project path: {project_root}")
    
    # Get the current version
    os.chdir(project_root)
    success, version_output = run_command("poetry version", "Current version")
    if not success:
        return
    
    # Confirm with user
    if args.bump:
        print(f"This will bump the {args.bump} version and publish to PyPI.")
    else:
        print(f"This will publish the current version to PyPI.")
    
    if args.no_tests:
        print("Warning: Tests will be skipped.")
    
    response = input("Continue with publishing? [y/N]: ")
    if response.lower() != 'y':
        print("Publishing cancelled.")
        return
    
    # Run publish
    publish_to_pypi(project_root, args.bump, args.no_tests)

if __name__ == "__main__":
    main()