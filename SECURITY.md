# 🔐 Security Policy

## Supported Versions

| Version | Supported          |
| ------- | ------------------ |
| 1.0.x   | :white_check_mark: |

## Reporting a Vulnerability

If you discover a security vulnerability in AITrader, please report it responsibly.

### How to Report

**DO NOT** open a public GitHub issue for security vulnerabilities.

Instead, please email: **darshanjain15062002@gmail.com**

Include:
- Description of the vulnerability
- Steps to reproduce
- Potential impact
- Suggested fix (if any)

### What to Expect

- **Response Time**: Within 48 hours
- **Updates**: Every 72 hours on progress
- **Resolution**: Security patches released ASAP
- **Credit**: Security researchers will be credited (if desired)

## Security Best Practices

### API Key Management

**NEVER commit API keys to GitHub!**

❌ **BAD:**
```python
genai.configure(api_key="AIzaSyAfjsA-tRRq6iBmlvX1abOmZgIDweq_Hwg")
```

✅ **GOOD:**
```python
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
```

### Steps to Secure Your Installation

1. **Move API Keys to Environment Variables**

Create `.env` file:
```bash
GEMINI_API_KEY=your_api_key_here
MONGODB_URI=your_mongodb_uri_here
```

2. **Update Your Code**

```python
# agent/gemini_agent.py
import os
from dotenv import load_dotenv

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
```

3. **Add .env to .gitignore**

The `.gitignore` file already includes `.env`

4. **Rotate Compromised Keys**

If you've committed an API key:
- Immediately revoke it in Google AI Studio
- Generate a new key
- Update your local configuration
- Use `git filter-branch` or BFG Repo-Cleaner to remove from history

### Financial Data Security

- **Account Data**: Keep `account.json` secure (contains portfolio)
- **Backups**: Store backups in encrypted storage
- **Access Control**: Limit who can access the trading system
- **Logging**: Review logs regularly for suspicious activity

### Network Security

- **API Server**: Don't expose to public internet without authentication
- **HTTPS**: Use HTTPS in production
- **Rate Limiting**: Implement rate limiting on API endpoints
- **Authentication**: Add authentication for API access

### MongoDB Security

If using MongoDB:
- Use strong passwords
- Enable authentication
- Use connection string with credentials
- Restrict network access
- Regular backups

### Production Deployment

For production use:

1. **Environment Isolation**
```bash
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```

2. **Secure Configuration**
- Use environment variables for all secrets
- Implement proper authentication
- Use HTTPS/TLS
- Regular security updates

3. **Monitoring**
- Log all trades
- Monitor for unusual activity
- Set up alerts for large losses
- Regular security audits

## Known Security Considerations

### Current Issues

1. **Hardcoded API Key** (Priority: HIGH)
   - Status: Needs immediate fix
   - Impact: API key exposed in code
   - Fix: Move to environment variables

2. **No API Authentication** (Priority: MEDIUM)
   - Status: Open
   - Impact: Anyone with URL can access API
   - Fix: Implement JWT or API key auth

3. **Account Data in JSON** (Priority: MEDIUM)
   - Status: By design
   - Impact: Sensitive portfolio data in plaintext
   - Fix: Consider encryption or database storage

### Mitigations

Until these are fixed:
- Don't expose API server publicly
- Keep API keys rotated
- Monitor account activity
- Use in trusted networks only

## Disclosure Policy

- **Private Disclosure**: 90 days before public disclosure
- **Coordinated Release**: Security fixes released with advisory
- **CVE Assignment**: For critical vulnerabilities
- **Credits**: Security researchers credited in release notes

## Security Updates

Subscribe to security updates:
- Watch this repository for releases
- Check CHANGELOG.md for security fixes
- Follow [@darshan15062002](https://github.com/darshan15062002) for announcements

## Questions?

For security questions: darshanjain15062002@gmail.com

---

**Remember**: This is trading software handling financial data. Take security seriously!
