# Security policy

## Protect credentials

- Never commit `.env`, Streamlit secrets, API keys, access tokens, or private logs.
- Use `.env.example` only as a template and keep its values empty or non-sensitive.
- Revoke and replace any credential immediately if it is exposed in Git history, screenshots, logs, or issue reports.
- Review staged files before every commit.

## Report a vulnerability

Do not include credentials or other sensitive information in a public issue. If GitHub private vulnerability reporting is enabled for this repository, use it to report security issues. Otherwise, contact the repository owner privately with a minimal reproduction and redact all secrets.
