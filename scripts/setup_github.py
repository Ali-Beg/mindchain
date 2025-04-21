#!/usr/bin/env python
"""
GitHub Repository Setup Script

This script helps set up a new GitHub repository for the MindChain project.
It creates the necessary initial commit and pushes it to GitHub.

Prerequisites:
1. Git installed and configured with your GitHub credentials
2. GitHub CLI installed (gh) or GitHub access token available
3. Repository already created on GitHub (empty)

Usage:
    python scripts/setup_github.py --repo Ali-Beg/mindchain --branch main
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path

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
        return False
    
    if result.stdout:
        print(result.stdout)
    
    return True

def setup_repository(repo_path, repo_url, branch):
    """Set up the Git repository and push to GitHub."""
    # Ensure we're in the project root directory
    os.chdir(repo_path)
    
    # Initialize Git if not already initialized
    if not Path(".git").is_dir():
        if not run_command("git init", "Initializing Git repository"):
            return False
    
    # Add remote if not already added
    result = subprocess.run(
        "git remote -v", 
        shell=True, 
        stdout=subprocess.PIPE, 
        stderr=subprocess.PIPE,
        text=True
    )
    
    if "origin" not in result.stdout:
        if not run_command(f"git remote add origin {repo_url}", "Adding GitHub remote"):
            return False
    
    # Add all files
    if not run_command("git add .", "Adding files to Git"):
        return False
    
    # Commit files
    if not run_command("git commit -m 'Initial commit of MindChain framework'", "Committing files"):
        return False
    
    # Push to GitHub
    if not run_command(f"git push -u origin {branch}", f"Pushing to {branch} branch"):
        return False
    
    print("\nSuccess! The MindChain repository has been set up and pushed to GitHub.")
    print(f"Repository URL: https://github.com/{repo_url}")
    return True

def main():
    parser = argparse.ArgumentParser(description="Set up GitHub repository for MindChain")
    parser.add_argument("--repo", required=True, help="GitHub repository in the format username/repo")
    parser.add_argument("--branch", default="main", help="Branch name (default: main)")
    args = parser.parse_args()
    
    # Get the absolute path to the project root
    repo_path = Path(__file__).parent.parent.absolute()
    
    # Construct the Git URL
    repo_url = f"git@github.com:{args.repo}.git"
    
    print(f"Setting up MindChain repository at {repo_url}")
    print(f"Project path: {repo_path}")
    
    # Confirm with user
    response = input("Continue with setup? [y/N]: ")
    if response.lower() != 'y':
        print("Setup cancelled.")
        return
    
    # Run setup
    setup_repository(repo_path, repo_url, args.branch)

if __name__ == "__main__":
    main()