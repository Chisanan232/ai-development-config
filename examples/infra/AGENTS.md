# Infrastructure Directory Configuration

This file provides infrastructure-specific context and conventions for Windsurf Cascade.

---

## Infrastructure Technology Stack

**[PROJECT-SPECIFIC]** Define infrastructure technologies:

* **Cloud provider**: [e.g., AWS, GCP, Azure, DigitalOcean]
* **IaC tool**: [e.g., Terraform, Pulumi, CloudFormation, CDK]
* **Container orchestration**: [e.g., Kubernetes, ECS, Cloud Run, Docker Swarm]
* **CI/CD platform**: [e.g., GitHub Actions, GitLab CI, Jenkins, CircleCI]

---

## Infrastructure as Code (IaC)

**[PROJECT-SPECIFIC]** Define IaC conventions:

### IaC Organization

* **IaC location**: [e.g., infra/, terraform/, pulumi/]
* **Module structure**: [e.g., "Environment-based", "Service-based", "Layer-based"]
* **State management**: [e.g., "S3 backend", "Terraform Cloud", "GCS backend"]

### IaC Commands

* **Initialize**: [e.g., `terraform init`, `pulumi login`]
* **Plan**: [e.g., `terraform plan`, `pulumi preview`]
* **Apply**: [e.g., `terraform apply`, `pulumi up`]
* **Destroy**: [e.g., `terraform destroy`, `pulumi destroy`]

### IaC Best Practices

* **Modules**: [e.g., "Reusable modules in modules/", "Versioned modules"]
* **Variables**: [e.g., "Use variables for environment-specific values", "Sensitive vars in secrets"]
* **Outputs**: [e.g., "Export important resource IDs", "Export connection strings"]
* **State locking**: [e.g., "Enable state locking", "Use DynamoDB for locks"]

---

## Container Configuration

**[PROJECT-SPECIFIC]** Define container conventions:

### Dockerfile Standards

* **Base images**: [e.g., "Use official images", "Pin versions", "Use slim/alpine variants"]
* **Multi-stage builds**: [e.g., "Use for production builds", "Separate build and runtime stages"]
* **Layer optimization**: [e.g., "Order layers by change frequency", "Combine RUN commands"]

### Container Registry

* **Registry**: [e.g., Docker Hub, ECR, GCR, ACR, GitHub Container Registry]
* **Image naming**: [e.g., `registry/project/service:tag`]
* **Tagging strategy**: [e.g., "Use git SHA", "Use semantic versioning", "Use latest for dev"]

---

## Kubernetes Configuration

**[PROJECT-SPECIFIC]** Define Kubernetes conventions if applicable:

### Kubernetes Resources

* **Manifests location**: [e.g., k8s/, kubernetes/, helm/]
* **Organization**: [e.g., "By service", "By environment", "By resource type"]
* **Configuration tool**: [e.g., "Raw YAML", "Helm", "Kustomize", "Jsonnet"]

### Resource Standards

* **Namespaces**: [e.g., "One per environment", "One per service"]
* **Labels**: [e.g., "app, version, environment, component"]
* **Resource limits**: [e.g., "Always set CPU/memory limits", "Use requests and limits"]
* **Health checks**: [e.g., "Define liveness and readiness probes"]

### Helm Charts

* **Chart location**: [e.g., helm/, charts/]
* **Values files**: [e.g., values.yaml, values-prod.yaml, values-staging.yaml]
* **Chart versioning**: [e.g., "Semantic versioning", "Match app version"]

---

## Deployment Strategies

**[PROJECT-SPECIFIC]** Define deployment approaches:

### Deployment Method

* **Strategy**: [e.g., "Rolling update", "Blue-green", "Canary"]
* **Rollback procedure**: [e.g., "Automated rollback on failure", "Manual rollback"]
* **Zero-downtime**: [e.g., "Required", "Best effort"]

### Environment Promotion

* **Environments**: [e.g., dev, staging, production]
* **Promotion flow**: [e.g., dev → staging → production]
* **Approval gates**: [e.g., "Manual approval for production", "Automated for staging"]

---

## Secrets Management

**[PROJECT-SPECIFIC]** Define secrets handling:

### Secrets Storage

* **Tool**: [e.g., AWS Secrets Manager, HashiCorp Vault, GCP Secret Manager, Azure Key Vault]
* **Access pattern**: [e.g., "Injected as env vars", "Mounted as files", "Fetched at runtime"]

### Secrets Rotation

* **Rotation frequency**: [e.g., "90 days", "On-demand"]
* **Rotation procedure**: [e.g., "Automated rotation", "Manual rotation with checklist"]

### Secrets in Code

* **Never**: [e.g., "Commit secrets to git", "Hardcode secrets", "Log secrets"]
* **Use**: [e.g., "Environment variables", "Secret management tools", "Encrypted config"]

---

## Monitoring and Observability

**[PROJECT-SPECIFIC]** Define monitoring setup:

### Monitoring Tools

* **Metrics**: [e.g., Prometheus, CloudWatch, Datadog, New Relic]
* **Logs**: [e.g., ELK Stack, CloudWatch Logs, Splunk, Loki]
* **Traces**: [e.g., Jaeger, Zipkin, X-Ray, Datadog APM]
* **Dashboards**: [e.g., Grafana, CloudWatch Dashboards, Datadog]

### Alerting

* **Alert manager**: [e.g., Alertmanager, PagerDuty, Opsgenie]
* **Alert channels**: [e.g., Slack, email, SMS, PagerDuty]
* **Alert severity**: [e.g., Critical, Warning, Info]

### Key Metrics

* **Infrastructure**: [e.g., CPU, memory, disk, network]
* **Application**: [e.g., Request rate, error rate, latency]
* **Business**: [e.g., Active users, transactions, revenue]

---

## Networking

**[PROJECT-SPECIFIC]** Define networking configuration:

### Network Architecture

* **VPC/Network**: [e.g., "One VPC per environment", "Shared VPC"]
* **Subnets**: [e.g., "Public and private subnets", "Multi-AZ"]
* **Security groups**: [e.g., "Least privilege", "Service-specific rules"]

### Load Balancing

* **Load balancer**: [e.g., ALB, NLB, Cloud Load Balancer, Ingress]
* **SSL/TLS**: [e.g., "Terminate at load balancer", "End-to-end encryption"]
* **Certificates**: [e.g., "ACM", "Let's Encrypt", "Manual"]

### DNS

* **DNS provider**: [e.g., Route 53, Cloud DNS, Cloudflare]
* **Domain structure**: [e.g., api.example.com, app.example.com]
* **TTL**: [e.g., "300s for production", "60s for testing"]

---

## Backup and Disaster Recovery

**[PROJECT-SPECIFIC]** Define backup strategy:

### Backup Policy

* **Backup frequency**: [e.g., "Daily", "Hourly", "Continuous"]
* **Retention**: [e.g., "30 days", "90 days", "1 year"]
* **Backup location**: [e.g., "S3", "GCS", "Azure Blob Storage"]

### Disaster Recovery

* **RPO**: [e.g., "1 hour", "24 hours"]
* **RTO**: [e.g., "4 hours", "1 hour"]
* **DR procedure**: [e.g., docs/disaster-recovery.md]
* **DR testing**: [e.g., "Quarterly", "Annually"]

---

## Security and Compliance

**[PROJECT-SPECIFIC]** Define security practices:

### Security Scanning

* **Container scanning**: [e.g., Trivy, Snyk, Clair]
* **IaC scanning**: [e.g., Checkov, tfsec, Terrascan]
* **Dependency scanning**: [e.g., Dependabot, Snyk, WhiteSource]

### Compliance

* **Standards**: [e.g., SOC 2, HIPAA, PCI-DSS, GDPR]
* **Audit logging**: [e.g., CloudTrail, Cloud Audit Logs]
* **Access control**: [e.g., IAM, RBAC, least privilege]

### Network Security

* **Firewalls**: [e.g., WAF, Network firewall, Security groups]
* **DDoS protection**: [e.g., CloudFlare, AWS Shield, Cloud Armor]
* **Intrusion detection**: [e.g., GuardDuty, Cloud IDS]

---

## Cost Management

**[PROJECT-SPECIFIC]** Define cost optimization:

### Cost Monitoring

* **Tool**: [e.g., AWS Cost Explorer, GCP Billing, Azure Cost Management]
* **Budget alerts**: [e.g., "Alert at 80% of budget", "Daily cost reports"]
* **Cost allocation**: [e.g., "Tag resources by team/project", "Use cost centers"]

### Cost Optimization

* **Right-sizing**: [e.g., "Review instance sizes monthly", "Use auto-scaling"]
* **Reserved capacity**: [e.g., "Use reserved instances for stable workloads"]
* **Spot instances**: [e.g., "Use for non-critical workloads", "Use for batch jobs"]

---

## CI/CD Pipeline

**[PROJECT-SPECIFIC]** Define CI/CD configuration:

### Pipeline Structure

* **Pipeline config**: [e.g., .github/workflows/, .gitlab-ci.yml, Jenkinsfile]
* **Stages**: [e.g., build, test, deploy]
* **Triggers**: [e.g., "On push to main", "On PR", "On tag"]

### Build Process

* **Build steps**: [e.g., "Install deps", "Run tests", "Build artifacts", "Build container"]
* **Artifact storage**: [e.g., S3, GCS, Artifactory]
* **Build caching**: [e.g., "Cache dependencies", "Use layer caching"]

### Deployment Process

* **Deploy steps**: [e.g., "Push image", "Update k8s", "Run migrations", "Smoke tests"]
* **Rollback**: [e.g., "Automatic on failure", "Manual trigger"]

---

## Infrastructure Testing

**[PROJECT-SPECIFIC]** Define infrastructure testing:

### IaC Testing

* **Validation**: [e.g., `terraform validate`, `pulumi preview`]
* **Linting**: [e.g., tflint, pylint for Pulumi]
* **Policy testing**: [e.g., OPA, Sentinel, Cloud Custodian]

### Integration Testing

* **Tool**: [e.g., Terratest, Kitchen-Terraform, Pulumi testing]
* **Test scope**: [e.g., "Test resource creation", "Test connectivity", "Test security rules"]

---

## Documentation

**[PROJECT-SPECIFIC]** Define infrastructure documentation:

### Required Documentation

* **Architecture diagrams**: [e.g., docs/architecture.md, draw.io files]
* **Runbooks**: [e.g., docs/runbooks/]
* **Incident response**: [e.g., docs/incident-response.md]
* **On-call guide**: [e.g., docs/on-call.md]

### Diagram Tools

* **Tool**: [e.g., draw.io, Lucidchart, Mermaid, PlantUML]
* **Diagram location**: [e.g., docs/diagrams/]

---

## Additional Infrastructure Resources

**[PROJECT-SPECIFIC]** Link to infrastructure-specific documentation:

* **Architecture decision records**: [e.g., docs/adr/]
* **Deployment guide**: [e.g., docs/deployment.md]
* **Troubleshooting guide**: [e.g., docs/troubleshooting.md]
* **Capacity planning**: [e.g., docs/capacity-planning.md]
