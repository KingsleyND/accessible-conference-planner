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

GitHub Actions remains blocked by the account billing lock. Direct GitOps deployment bypasses image builds: the Deployment runs public `python:3.12-slim` with the Python file mounted from a Kustomize-generated ConfigMap. Service `app` on port 80 remains unchanged.

## Live deployment

Verified 2026-11-09 17:08 MST: Argo CD synced deployment commit `38ed272`; both new Python replicas are ready and available. The public URL https://cloud9.cnh.radarhq.io serves My Accessible Conference Day, version `d223103-direct`. All three public health endpoints return OK, and the AI/captions/quiet-break itinerary works.

For this deployment path, keep `deploy/server.py` identical to `app/server.py` when editing the app. Kustomize hashes the ConfigMap content so code changes trigger a rollout. The Dockerfile remains available when image builds resume. The Actions billing lock is a remaining CI limitation, not a blocker for this GitOps path.
