# Service Level Objectives

This lab treats reliability as a measurable engineering requirement instead of a vague goal.

## Availability SLI

**SLI:** successful requests / total requests.

A successful request is an HTTP response below 500.

**Target SLO:** 99.9% monthly availability.

**Error budget:** 0.1% of requests may fail during the measurement window.

Example PromQL:

```promql
1 - (
  sum(rate(demo_http_requests_total{status=~"5.."}[30d]))
  /
  sum(rate(demo_http_requests_total[30d]))
)
```

## Latency SLI

**SLI:** p95 request duration.

**Target SLO:** 95% of requests complete in less than 500 ms.

Example PromQL:

```promql
histogram_quantile(
  0.95,
  sum(rate(demo_http_request_duration_seconds_bucket[5m])) by (le)
)
```

## Alerting strategy

- Page when the 5xx error ratio is above 5% for 2 minutes.
- Warn when p95 latency remains above 500 ms for 5 minutes.
- In production, use multi-window burn-rate alerts so paging is tied to error-budget consumption instead of isolated spikes.

## Reliability review

After a significant incident:

1. Confirm customer impact and SLO impact.
2. Build a timeline from metrics, logs and deployment events.
3. Identify contributing technical and process factors.
4. Define corrective actions with owners and due dates.
5. Convert repeated failure modes into automation, tests or actionable alerts.
