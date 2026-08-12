# Incident Response Runbook

## Severity model

- **P0:** complete outage or severe customer impact. Immediate response and broad escalation.
- **P1:** major degradation with significant customer impact. Immediate triage and mitigation.
- **P2:** limited degradation with workaround available.

## First 10 minutes

1. Acknowledge the alert and record the incident start time.
2. Confirm impact using health checks, request rate, 5xx rate and p95 latency.
3. Check recent deployments and infrastructure changes.
4. Identify whether the issue is application, dependency, network or capacity related.
5. Prefer fast mitigation over deep diagnosis: rollback, scale out, disable a failing dependency or shift traffic when appropriate.
6. Escalate if impact is not reduced quickly.

## High error rate

Useful signals:

```promql
sum(rate(demo_http_requests_total{status=~"5.."}[5m]))
/
clamp_min(sum(rate(demo_http_requests_total[5m])), 0.001)
```

Actions:

1. Check application container health and logs.
2. Compare the error increase with recent deployment timestamps.
3. Verify dependency/network reachability.
4. If a release introduced the failure, roll back to the last known-good image.
5. If failures correlate with load, review CPU/memory saturation and scale capacity.

## High p95 latency

```promql
histogram_quantile(
  0.95,
  sum(rate(demo_http_request_duration_seconds_bucket[5m])) by (le)
)
```

Actions:

1. Verify CPU/memory saturation and request concurrency.
2. Check dependency latency and network errors.
3. Compare against request volume and recent releases.
4. Scale horizontally if the service is healthy but saturated.
5. Roll back if latency increased after a deployment.

## AWS/ECS checks

```bash
aws ecs describe-services --cluster sre-observability-lab --services sre-observability-lab
aws ecs list-tasks --cluster sre-observability-lab --service-name sre-observability-lab
aws logs tail /ecs/sre-observability-lab --follow
```

Review CloudWatch alarms for ECS CPU and ALB 5xx errors, then check target health behind the load balancer.

## Resolution and post-incident review

After restoring service:

- Confirm metrics have returned to normal.
- Record customer impact and duration.
- Create a timeline of detection, response, mitigation and recovery.
- Document root cause and contributing factors.
- Add follow-up actions with owners.
- Improve monitoring, tests or automation when the incident exposed a detection gap.
