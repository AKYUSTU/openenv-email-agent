# Email Triage OpenEnv

## Description

This environment simulates email handling in a company.

## Tasks

- Easy: basic support email
- Medium: ambiguous email
- Hard: legal/critical email

## Action Space

- classify
- reply
- escalate
- ignore

## Setup

docker build -t email-env .
docker run email-env
