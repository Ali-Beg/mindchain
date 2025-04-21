# Security Policy

## Supported Versions

Use this section to tell people about which versions of your project are
currently being supported with security updates.

| Version | Supported          |
| ------- | ------------------ |
| 0.1.x   | :white_check_mark: |

## Reporting a Vulnerability

We take the security of MindChain seriously. If you believe you've found a security vulnerability, please follow these steps:

1. **Do not disclose the vulnerability publicly**
2. **Email us at [mbeg937@gmail.com](mailto:mbeg937@gmail.com)** with:
   - Description of the vulnerability
   - Steps to reproduce
   - Potential impact
   - Any suggestions for mitigation

We will acknowledge your email within 48 hours and provide a more detailed response within 7 days, including:
- Confirmation of the vulnerability
- Our plans for addressing it
- Potential timeline for a fix

## Security Measures

MindChain includes several security features:

1. **Agent Sandboxing**: Agent execution is isolated to prevent unauthorized access
2. **Permission Management**: Granular control over tool access
3. **Input Validation**: All inputs are validated before processing
4. **Secure Defaults**: Security-conscious default settings
5. **Policy Enforcement**: MCP enforces security policies on agent behavior

## Best Practices

When using MindChain:

1. Keep your dependencies updated
2. Apply the principle of least privilege to agent tool access
3. Regularly review agent logs for unexpected behavior
4. Use secure API keys with limited permissions
5. Be cautious when allowing custom code execution through agents
