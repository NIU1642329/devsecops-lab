# devsecops-lab

DevOps Assignment 9 (DevSecOps fundamentals) - Laia Alcalde Maria, F11515010.

A small Flask dice service used to practise security checks in CI:

| Check | Tool | Where |
|---|---|---|
| Linting + security rules (A) | flake8 + flake8-bandit | `.github/workflows/ci.yml` |
| Software composition analysis (E) | GitHub Dependabot | `.github/dependabot.yml` |
| SAST (O) | GitHub CodeQL | `.github/workflows/codeql.yml` |

> Lab project only: it is never deployed. Some dependencies are pinned to old
> versions on purpose so that Dependabot has something to report.
