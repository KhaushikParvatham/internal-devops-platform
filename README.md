# Internal DevOps Platform

An internal DevOps and platform engineering project that demonstrates how applications are deployed, managed, and observed inside a Kubernetes cluster using GitOps, Helm, and open-source observability tooling.

This project focuses on **Kubernetes operations and platform workflows**, not cloud infrastructure provisioning. It simulates how DevOps and platform teams operate services once a Kubernetes cluster already exists.

---

## Project Purpose

The purpose of this project is to demonstrate:

• Kubernetes-native application deployment  
• GitOps-based continuous delivery using Argo CD  
• Helm-based application packaging  
• Service-to-service communication inside Kubernetes  
• Application observability using Prometheus and Grafana  
• Operational troubleshooting and monitoring workflows  

This project complements a cloud-focused DevOps project by emphasizing **runtime operations, reliability, and visibility inside Kubernetes**.

---

## Scope and Constraints

• Kubernetes cluster runs locally using Kind  
• No cloud provider is used  
• No infrastructure provisioning (Terraform, EKS, EC2)  
• Focus is on platform behavior, not infrastructure creation  

All design choices reflect this scope intentionally.

---

## High-Level Architecture

• Local multi-node Kubernetes cluster (Kind)  
• Argo CD for GitOps-based application delivery  
• Helm charts for application packaging  
• Internal API service (FastAPI)  
• PostgreSQL for relational storage  
• Redis for caching  
• Prometheus for metrics collection  
• Grafana for visualization  

All components are deployed and managed declaratively through Git.

---

## Technology Stack

**Containers & Orchestration**
• Docker  
• Kubernetes (Kind)  

**GitOps & Packaging**
• Argo CD  
• Helm  

**Backend Services**
• FastAPI (Python)  
• PostgreSQL  
• Redis  

**Observability**
• Prometheus  
• Grafana  
• kube-prometheus-stack  

**Tooling**
• Git  
• GitHub  
• kubectl  

---

## Application Components

### API Service

A FastAPI-based internal service that:

• Exposes REST endpoints  
• Connects to PostgreSQL and Redis using Kubernetes service discovery  
• Provides a health endpoint validating backend connectivity  
• Exposes Prometheus-compatible metrics via `/metrics`  
• Simulates latency using a controlled slow endpoint  

The service is deployed using a Kubernetes Deployment.

---

### PostgreSQL

• Deployed as a Kubernetes Deployment  
• Credentials stored in Kubernetes Secrets  
• Used to validate backend connectivity and health checks  

---

### Redis

• Deployed as a Kubernetes Deployment  
• Used as a cache layer  
• Validated through health checks and runtime connectivity  

---

## GitOps Workflow (Argo CD)

• All Kubernetes manifests and Helm charts are stored in Git  
• Argo CD continuously watches the repository  
• Any Git commit triggers reconciliation  
• Cluster state is automatically aligned with Git  

Manual changes inside the cluster are reverted, ensuring:

• No configuration drift  
• Fully auditable changes  
• Consistent environments  

---

## Helm-Based Deployments

Each application is packaged as a Helm chart:

• Parameterized configuration via `values.yaml`  
• Reusable templates for deployments and services  
• Clear separation of application logic and configuration  

Helm charts are consumed directly by Argo CD as part of the GitOps workflow.

---

## Networking and Service Discovery

• All services use Kubernetes ClusterIP services  
• Applications communicate using Kubernetes DNS  
• No hardcoded IP addresses  
• Services remain reachable during pod restarts  

---

## Deployment Strategy

• Applications are deployed using Kubernetes Deployments  
• Default rolling update behavior is used  
• Pods are replaced safely during updates  
• Service availability is maintained during restarts  

No custom strategy tuning was applied, reflecting real-world defaults.

---

## Observability

### Prometheus

• Scrapes metrics from the API `/metrics` endpoint  
• Uses ServiceMonitor for automatic discovery  
• Collects:
  - Request counts
  - Request latency histograms
  - Process-level metrics  

---

### Grafana

• Dashboards visualize:
  - API request rate
  - Latency trends
  - Slow endpoint behavior
  - Service health  

Metrics are validated by generating traffic and observing real-time changes.

---

## Operational Learnings

This project demonstrates how DevOps and platform engineers:

• Operate Kubernetes workloads reliably  
• Use Git as the single source of truth  
• Deploy changes safely using GitOps  
• Debug issues using metrics and dashboards  
• Build platform workflows without cloud dependencies