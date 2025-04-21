# Deployment Guide

This document describes how to deploy MindChain to PyPI and manage releases.

## Prerequisites

1. You must have Poetry installed (`pip install poetry`)
2. You must have permissions to publish to PyPI under the "mindchain" package name
3. You must have a PyPI API token

## Manual Deployment

### Step 1: Set up your PyPI token

Create a PyPI token at https://pypi.org/manage/account/token/ and add it to your environment:

```bash
# Add to your .env file
PYPI_API_TOKEN=your_token_here

# Or set temporarily in your shell
export PYPI_API_TOKEN=your_token_here
```

### Step 2: Configure Poetry with your PyPI token

```bash
poetry config pypi-token.pypi $PYPI_API_TOKEN
```

### Step 3: Increment the version

Edit the version in `pyproject.toml`:

```toml
[tool.poetry]
name = "mindchain"
version = "0.1.1"  # Update this version
```

Or use Poetry's version command:

```bash
poetry version patch  # Increments the patch version (0.1.0 -> 0.1.1)
poetry version minor  # Increments the minor version (0.1.0 -> 0.2.0)
poetry version major  # Increments the major version (0.1.0 -> 1.0.0)
```

### Step 4: Build the package

```bash
poetry build
```

This will create distribution files in the `dist/` directory.

### Step 5: Publish to PyPI

```bash
poetry publish
```

Or build and publish in one command:

```bash
poetry publish --build
```

## Automated Deployment with GitHub Actions

The deployment process is automated using GitHub Actions in the `.github/workflows/publish.yml` workflow.

### How to trigger an automated release:

1. Create a new GitHub release through the GitHub UI
2. Tag it with the same version number as in `pyproject.toml`
3. The publish workflow will automatically trigger and deploy to PyPI

### Setting up GitHub Secrets

Make sure to set up the `PYPI_API_TOKEN` secret in your GitHub repository:

1. Go to your GitHub repository
2. Click on "Settings" > "Secrets and variables" > "Actions"
3. Click "New repository secret"
4. Name: `PYPI_API_TOKEN`
5. Value: Your PyPI API token

## Release Process Best Practices

1. Update the CHANGELOG.md with details of changes
2. Update version number in pyproject.toml
3. Create and merge a PR with these changes
4. Create a GitHub release and tag it with the version number 
5. Write detailed release notes in the GitHub release
6. The CI will handle testing, building, and publishing to PyPI