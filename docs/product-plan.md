# DataGuard AI Product and GTM Plan

## Positioning
DataGuard AI helps telecom data, billing, and revenue-assurance teams detect missing files, ETL failures, replication lag, and abnormal revenue variance before they create billing errors, reporting surprises, or revenue leakage.

## Ideal customer profile
The initial ICP is a mid-sized or enterprise telecom operator, MVNO, or digital telecom brand with high-volume batch pipelines, billing feeds, revenue metrics, and manual monitoring across data engineering and revenue assurance teams.

## Primary users and buyers
- Primary users: data engineers, revenue assurance analysts, billing operations managers, BI/reporting teams, and NOC/operations teams.
- Economic buyers: Head of Revenue Assurance, VP Data Engineering, Chief Data Officer, Head of Billing Operations, CIO, and CFO for strategic accounts.

## Three urgent problems
1. Missing or late billing, usage, recharge, roaming, or payment files.
2. Abnormal revenue variance that may indicate leakage or delayed recognition.
3. Batch lag, replication failures, and busy queues that make downstream reporting unreliable.

## Essential MVP features
- Critical feed registry with owner, SLA, file pattern, and revenue context.
- Missing-file and late-file detection.
- ETL job status and runtime anomaly monitoring.
- Revenue variance detection against historical baselines.
- Business-impact estimation in dollars.
- Alerting through email, Slack, Microsoft Teams, and webhooks.
- Executive-readable dashboard for pipeline health, open alerts, and revenue at risk.
- Audit history and role-based access control for enterprise readiness.

## Later features
- Schema monitoring and data distribution drift.
- Kafka and streaming observability.
- Advanced lineage and automated root-cause analysis.
- Automated remediation and runbook execution.
- Additional industries such as banking, insurance, retail, utilities, and logistics.

## High-level architecture
1. Customer-hosted or SaaS metadata collectors gather file metadata, ETL status, and aggregated business metrics.
2. Ingestion services normalize events into feeds, jobs, and metrics.
3. Monitoring rules detect missing files, late arrivals, job failures, and runtime anomalies.
4. Anomaly detection compares revenue metrics against historical baselines.
5. A business-impact engine estimates revenue at risk from feed criticality and historical revenue.
6. Alerting services route incidents to dashboards and collaboration tools.
7. The web dashboard exposes pipeline health, revenue risk, and incident details.

## Integrations and data inputs
Initial integrations should prioritize SFTP/file shares, cloud object storage, SQL databases, Airflow, Control-M/Autosys exports, cron logs, and webhook ingestion. The MVP should ingest metadata, row counts, file sizes, timestamps, job status, and aggregated metrics rather than raw customer-level billing records.

## Security controls
The MVP should use data minimization, TLS in transit, encryption at rest, role-based access control, audit logging, IP allowlisting, secret management, and SSO-ready authentication. Enterprise packages should support customer-cloud or private deployment and prepare for SOC 2.

## 90-day validation plan
- Days 1-30: complete 25-35 telecom discovery interviews across revenue assurance, data engineering, billing, BI, and operations.
- Days 31-60: validate prototype screens, integration requirements, pilot scope, and buyer willingness to pay.
- Days 61-90: run one structured 60-90 day pilot monitoring 3-5 critical feeds, 1-2 revenue metrics, and one alert channel.

Success evidence before expansion: at least two qualified pilots, one paid pilot, detection accuracy above 90%, false positives below 15%, 50% faster detection, and buyer confirmation that business-impact estimates are valuable.

## Pricing and packaging
- Paid pilot: $10,000-$50,000 for 60-90 days.
- Mid-market telecom: $3,000-$8,000 per month for up to 25 feeds and 10 metrics.
- Enterprise telecom: $10,000-$25,000 per month for larger deployments, SSO, audit logs, and private deployment options.
- Strategic enterprise: $300,000-$750,000+ annually for global or multi-country operators.

The $99 and $499 monthly tiers are too low for enterprise telecom buying behavior and would signal a lightweight SMB tool. The $5,000-$20,000 monthly range is more credible for enterprise revenue-protection positioning.

## First five customers
Acquire the first five customers through founder-led sales using Vodafone credibility: former Vodafone contacts, adjacent telecom operators, MVNOs, telecom revenue-assurance consultancies, and warm referrals from data engineering or billing leaders. Lead with specific telecom pain: missing files, revenue variance, batch lag, replication failures, and busy queues.

## One-year roadmap
- Q1: discovery, prototype, MVP build, one pilot commitment, and $10K-$50K pilot revenue.
- Q2: execute 1-2 pilots, monitor 5-15 feeds, improve alert accuracy, and build annual-contract pipeline.
- Q3: convert at least one pilot to annual contract, launch 2-3 more pilots, and reach $100K-$250K ARR.
- Q4: harden security, add deployment automation and customer-hosted agent, reach 3-5 paying customers, and target $300K-$750K ARR.
