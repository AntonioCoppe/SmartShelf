# SmartShelf

**Real-Time Retail Shelf Monitoring & Demand Forecasting**

---

## Table of Contents

1. [Project Overview](#project-overview)
2. [Features](#features)
3. [Architecture & Design](#architecture--design)
4. [Getting Started](#getting-started)

   * [Prerequisites](#prerequisites)
   * [Installation](#installation)
   * [Configuration](#configuration)
5. [Usage](#usage)
6. [Modeling Details](#modeling-details)
7. [Tech Stack](#tech-stack)
8. [Contributing](#contributing)
9. [License](#license)
10. [Contact](#contact)

---

## Project Overview

SmartShelf is a microservices-based platform that uses state‑of‑the‑art AI to:

* **Detect & Segment** products on retail shelves in real time via computer vision.
* **Forecast** SKU depletion using time‑series models combined with historical POS data.
* **Alert** stakeholders with automated restock notifications and daily “Shelf Health” reports.

Out‑of‑stock events cost retailers billions annually. SmartShelf minimizes lost sales, improves customer satisfaction, and slashes emergency reorder fees.

## Features

* **Zero‑Shot Object Detection**: Identify new SKUs without retraining.
* **Image Segmentation**: Accurately separate products from shelf backgrounds.
* **Demand Forecasting**: Temporal Fusion Transformer for 7‑day run‑out predictions.
* **Automated Alerts**: Slack, email, SMS, or in‑app notifications.
* **Dashboard**: React + D3.js UI with live heatmaps and predictive charts.
* **Scalable**: Dockerized services in Kubernetes/ECS, plug‑in model architecture.

## Architecture & Design

```text
Video/Image Feed → Edge Agent → Storage       POS & Inventory API → Data Store
        │                    │                         │
        └──> CV Service (FastAPI + DETR) ───> JSON Events ─┐
                                                           └> Forecast Service (FastAPI + TFX)
                                                                        ↓
                                                         Alerting & Reporting ↔ Frontend Dashboard
                                                                       
```

* **Edge Agent** (Raspberry Pi / Mobile App) streams images to cloud storage.
* **CV Service**: PyTorch + Hugging Face DETR for detection & segmentation.
* **Forecasting Service**: Temporal Fusion Transformer via `pytorch-forecasting`.
* **Alerting**: Aggregates events, sends notifications, and produces summaries.
* **Dashboard**: Interactive React/TypeScript + D3.js for visualization.
* **CI/CD**: GitHub Actions → AWS ECR/EKS (or Terraform + Kubernetes).

## Getting Started

### Prerequisites

* **Python 3.9+**
* **Node.js 16+ & npm/yarn**
* **Docker & Kubernetes** (or AWS ECS)
* **AWS Account** (S3, EKS, IAM) or **GCP** (Storage, GKE)
* **PostgreSQL** & **Redis** instances

### Installation

1. **Clone the repo**

   ```bash
   git clone https://github.com/<your-org>/smartshelf.git
   cd smartshelf
   ```
2. **Backend**

   ```bash
   cd backend
   pip install -r requirements.txt
   ```
3. **Frontend**

   ```bash
   cd ../frontend
   npm install
   ```
4. **Infrastructure**

   * Use Terraform scripts under `infra/` to provision cloud resources.

### Configuration

1. Copy `.env.example` to `.env` in each service folder.
2. Update credentials (AWS/GCP keys, DB URLs, API tokens).
3. (Optional) Fine‑tune Hugging Face models and update model endpoints.

## Usage

### Local Development

1. **Launch services**

   ```bash
   docker-compose up --build
   ```
2. **Access dashboard** at `http://localhost:3000`
3. **Stream test images** via the edge-simulator script:

   ```bash
   python edge_agent/simulate_stream.py --dir ./test_images
   ```

### Deployment

1. **Build & push** Docker images:

   ```bash
   bash scripts/build_and_push.sh
   ```
2. **Deploy** with Helm/Terraform:

   ```bash
   terraform apply -var-file=prod.tfvars
   ```

## Modeling Details

* **Object Detection**: `facebook/detr-resnet-50` fine‑tuned on custom grocery dataset.
* **Segmentation**: `nvidia/segformer-b0` for precise masking.
* **Forecasting**: Hugging Face’s `temporal-fusion-transformer` with historical sales + restock events.

## Tech Stack

* **Backend**: Python, FastAPI, PyTorch, Hugging Face Transformers
* **Frontend**: React, TypeScript, D3.js
* **Data**: PostgreSQL, Redis, AWS S3/GCS
* **Infrastructure**: Docker, Kubernetes/ECS, Terraform, GitHub Actions
* **Monitoring**: Prometheus, Grafana, Sentry

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/YourFeature`)
3. Commit your changes (`git commit -m 'Add YourFeature'`)
4. Push to branch (`git push origin feature/YourFeature`)
5. Open a Pull Request

Please follow the [Code of Conduct](CODE_OF_CONDUCT.md) and [Contributor Guidelines](CONTRIBUTING.md).

## License

This project is licensed under the [MIT License](LICENSE).

## Contact

Antonio Coppe – [antonio.coppe@gmail.com](mailto:antonio.coppe@gmail.com)

Project Link: [github.com/AntonioCoppe/smartshelf](https://github.com/AntonioCoppe/smartshelf)
