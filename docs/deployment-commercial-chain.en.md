# Deployment and Commercial Chain

Public stage: `0.08`

## What GitHub Pages Does

GitHub Pages is a static hosting surface. It can serve:

- HTML;
- CSS;
- JavaScript that runs in the visitor's browser;
- images;
- video files;
- documentation.

It does not run your backend code. It does not host databases, login systems, task queues, paid API logic, location services, or model inference.

For this repository, GitHub Pages is the right place for:

- the product landing page;
- the Remotion demo video;
- release copy;
- benchmark visuals;
- links to GitHub releases and docs.

## Resource Usage

GitHub Pages does not use your own server. Visitors load static files from GitHub's Pages infrastructure.

Practical limits still exist:

- repository and site size limits;
- build and deployment limits;
- bandwidth/traffic limits under GitHub's current policy;
- GitHub account and terms-of-service boundaries.

So GitHub Pages is good for awareness and lead capture, not for heavy product execution.

## What Needs Real Server Infrastructure

Your material-intelligence design platform is different from this landing page. A full platform usually needs:

- frontend app hosting;
- backend API;
- database;
- object storage for files and generated artifacts;
- authentication;
- billing;
- job queue;
- GPU/CPU workers;
- observability and logs;
- location or region-aware service if required;
- privacy and compliance controls.

## Business Loop

The commercial chain should be:

1. GitHub repo proves credibility.
2. GitHub Pages explains the value in one minute.
3. Remotion video makes the idea shareable.
4. Diagnostics and benchmarks create evidence.
5. Privacy guard creates trust.
6. Users star, try, and report issues.
7. Serious users enter a hosted product or paid consulting path.
8. The material-intelligence platform becomes the high-value paid surface.

## Recommended Infrastructure Split

| Layer | Best platform | Purpose |
| --- | --- | --- |
| Static launch page | GitHub Pages | Public awareness and SEO. |
| Documentation | GitHub repo + Pages | Trust and developer adoption. |
| Demo video | GitHub release asset + Pages embed | Social proof. |
| Hosted product frontend | Vercel, Cloudflare Pages, or similar | Interactive SaaS UI. |
| Backend API | Fly.io, Render, Railway, AWS, Azure, or GCP | Accounts, billing, workflows. |
| Database | Postgres-compatible service | Users, jobs, metadata. |
| Object storage | S3-compatible storage | PDFs, videos, generated materials. |
| Compute workers | GPU/CPU worker pool | Materials simulation, ML, distillation, analysis. |

## Boundary

Do not put secrets, private routes, account states, or production queues into GitHub Pages. It is public static hosting.
