# Contributing to MindChain

First off, thank you for considering contributing to MindChain! It's people like you who make this framework a powerful tool for AI agent development.

This document outlines how you can contribute to the project and the process for reviewing and merging your changes.

## Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Types of Contributions](#types-of-contributions)
- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Repository Structure](#repository-structure)
- [Branching Strategy](#branching-strategy)
- [Coding Standards](#coding-standards)
- [Pull Request Process](#pull-request-process)
- [AI Component Guidelines](#ai-component-guidelines)
- [Documentation Guidelines](#documentation-guidelines)
- [Community and Communication](#community-and-communication)

## Code of Conduct

This project and everyone participating in it is governed by the [MindChain Code of Conduct](CODE_OF_CONDUCT.md). By participating, you are expected to uphold this code.

## Types of Contributions

We're looking for various types of contributions:

### 🐛 Bug Fixes
- Fixing issues in existing functionality
- Addressing edge cases
- Improving error handling

### ✨ Feature Implementations
- Adding new capabilities to components
- Implementing planned roadmap items
- Extending existing functionality

### 📚 Documentation
- Improving explanations and examples
- Adding tutorials
- Fixing typos or clarifying language
- Creating architecture diagrams

### 🔧 Tools
- Adding new tools to the ecosystem
- Enhancing existing tools
- Creating connectors to external systems

### 🧠 Memory Systems
- Implementing new memory types
- Optimizing existing memory implementations
- Adding memory persistence mechanisms

### 🧪 Testing
- Adding test cases
- Improving test coverage
- Creating benchmarks

### 🌟 Examples
- Creating new example applications
- Demonstrating real-world use cases
- Showcasing framework capabilities

## Getting Started

1. Fork the repository on GitHub
2. Clone your fork locally: `git clone https://github.com/yourusername/mindchain.git`
3. Set up the development environment as described in the next section
4. Create a branch for your changes: `git checkout -b feature/your-feature-name`

## Development Setup

1. Set up Poetry environment (recommended):
   ```bash
   # Install Poetry if not already installed
   pip install poetry
   
   # Configure Poetry to create virtual environment in project directory
   poetry config virtualenvs.in-project true
   
   # Install dependencies
   poetry install
   
   # Activate the virtual environment
   poetry shell
   ```

   Or create a traditional virtual environment:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -e ".[dev,docs]"
   ```

2. Install pre-commit hooks:
   ```bash
   pre-commit install
   ```

3. Run tests to ensure everything is working:
   ```bash
   pytest
   ```

4. Set up environment variables:
   Create a `.env` file in the project root with necessary API keys:
   ```
   OPENAI_API_KEY=your_openai_api_key_here
   # Add other provider keys as needed
   ```

## Repository Structure

Our repository is organized as follows:

```
mindchain/
├── .github/                           # GitHub specific files
├── docs/                              # Documentation
├── examples/                          # Example code
├── src/                               # Source code
│   └── mindchain/                     # Main package
│       ├── mcp/                       # Master Control Program
│       ├── core/                      # Core components
│       ├── memory/                    # Memory systems
│       ├── tools/                     # Tool implementations
│       ├── interfaces/                # Developer interfaces
│       └── utils/                     # Utilities
└── tests/                             # Tests
```

For a detailed breakdown of the repository structure, please see our [Repository Structure](docs/architecture/repository_structure.md) documentation.

## Branching Strategy

We follow a structured branching strategy:

- `main` branch is the stable release branch
- `develop` branch is the integration branch for upcoming releases
- Feature branches should be created from `develop`

### Branch Naming Conventions

- Features: `feature/brief-description`
- Bug fixes: `fix/brief-description`
- Documentation: `docs/brief-description`
- Performance improvements: `perf/brief-description`

## Coding Standards

- Follow PEP 8 style guide
- Use type hints wherever possible
- Write docstrings in Google style format
- Run code formatters before committing:
  ```bash
  black src tests
  isort src tests
  ```

Example with type hints and docstrings:
```python
from typing import Dict, List, Optional

def retrieve_by_similarity(query: str, k: int = 5) -> List[Dict[str, any]]:
    """
    Retrieve memory items by semantic similarity to the query.
    
    Args:
        query: The query string to match against
        k: The number of results to return
        
    Returns:
        A list of memory items sorted by similarity
    """
    # Implementation
```

## Pull Request Process

1. Update the README.md or documentation with details of changes if appropriate
2. Update the CHANGELOG.md with a description of your changes
3. Ensure all tests pass and add new tests for new functionality
4. Submit a pull request with a clear title and description
5. Request review from maintainers

### PR Requirements Checklist

- [ ] Code follows the style guidelines
- [ ] Tests for the changes have been added
- [ ] Documentation has been updated
- [ ] CI pipeline passes
- [ ] PR has been linked to relevant issues

## AI Component Guidelines

When contributing to AI components in MindChain:

### Safety First
- All agent capabilities must respect safety boundaries
- Include appropriate guardrails, especially for MCP policy enforcement
- Document potential risks and mitigations
- Implement proper input validation and error handling

### Model Compatibility
- Document which LLM providers your code works with
- Specify minimum model capabilities required
- Test with multiple providers when possible
- Handle provider-specific edge cases

### Resource Usage
- Consider efficiency and provide resource usage estimates
- Document memory requirements for large operations
- Implement resource constraints where appropriate
- Use token counting for LLM operations

### Testing
- Include both unit tests and integration tests
- Use mock LLMs for testing when appropriate
- Test edge cases and potential failure modes
- Create benchmarks for performance-critical components

### Prompt Templates
- Keep prompt templates organized and documented
- Make templates configurable where possible
- Consider token efficiency in prompt design
- Use structured prompting techniques

## Documentation Guidelines

We prioritize comprehensive documentation:

### Style
- Use clear, concise language
- Prefer active voice over passive
- Make documentation accessible to developers of all experience levels
- Use code examples whenever appropriate

### Structure
- Follow the existing documentation structure in the docs/ directory
- Use consistent headers and formatting
- Include a table of contents for longer documents
- Link related documentation sections for improved navigation

### MkDocs Integration
- All documentation is built with MkDocs
- Preview changes locally before submitting:
  ```bash
  cd docs
  mkdocs serve
  ```
- Use available markdown extensions for better formatting
- Test documentation links to ensure they work

### Examples
- Include code examples when relevant
- Ensure examples are correct and tested
- Show both basic and advanced usage
- Use the examples/ directory for complete, runnable examples

## Community and Communication

We have several channels for communication:

- **GitHub Issues**: For bug reports and feature requests
- **GitHub Discussions**: For questions, ideas, and community discussions

## Issue Reporting

- Use the issue tracker to report bugs or request features
- Check existing issues before creating a new one
- Provide detailed information when reporting bugs:
  - Steps to reproduce
  - Expected behavior
  - Actual behavior
  - Environment details (OS, Python version, etc.)

## Recognition

We value all contributions and recognize contributors in several ways:

- All contributors are acknowledged in our release notes
- Significant contributions will be specifically highlighted
- Regular contributors may be invited to join as maintainers

---

Thank you for contributing to MindChain and helping build the future of AI agent frameworks!
