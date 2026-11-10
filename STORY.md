# My Accessible Conference Day — cloud9

## Before

Recorded 2026-11-09 16:58 MST, before the first GitOps deployment.

[Radar Checks for team-cloud9](https://app.radarhq.io/checks?scope=FZrBD2cWvvQ&namespace=team-cloud9)

Summary: 0 critical, 0 high, 3 medium, 0 low findings.

- Medium / Security: `automountServiceAccountToken` — Deployment/team-cloud9/app.
- Medium / Reliability: `missingPDB` — Deployment/team-cloud9/app.
- Medium / Reliability: `missingTopologySpread` — Deployment/team-cloud9/app.

These findings describe the platform starter currently running. Review their applicability after the project deploys; platform components in other namespaces are outside the team's remediation scope.

## Project

Commit `d223103` replaces the Node starter with a single-file Python standard-library planner and a `python:3.12-slim` image. Local HTTP checks passed for all three health endpoints, topic/access filtering and quiet breaks. The Service and namespace configuration are unchanged.

Deployment is pending a successful GitHub Actions build. The earlier setup build was rejected before any steps ran because GitHub reported an account billing lock. No new image has been verified live.
