# Badger - Data Contract Validation & Observability

![Badger Logo](https://your-logo-url.com/logo.png)

## 🚀 Overview
Badger is an open-source **data contract validation and observability** tool for **data pipelines and AI workflows**. It ensures that data conforms to **predefined schemas, SLAs, and quality rules**, while also detecting **feature drift** for AI models.

## 🔥 Key Features
- ✅ **Schema Validation** - Ensures required fields and correct data types.
- ✅ **Data Quality Checks** - Enforces regex patterns and field constraints.
- ✅ **Feature Drift Detection** - Detects changes in AI model inputs.
- ✅ **SLA Monitoring** - Tracks freshness, schema drift, and validation success rates.
- ✅ **CLI & API Support** - Validate datasets programmatically.

## 📦 Installation
```bash
pip install badger-validator
```

## 🛠 Usage
### **1️⃣ Validating a Data Pipeline Contract**
```bash
badger validate --contract data_contract.yaml --data sample_data.csv
```

### **2️⃣ AI Data Validation with Feature Drift Detection**
```bash
badger validate --contract ai_data_contract.yaml --data new_data.csv --reference reference_data.csv
```

## 📖 Example Data Contract
```yaml
version: "1.0"
contract_name: "Contract-Finance-Data"
required_fields:
  - user_id
  - user_name
  - email
field_types:
  user_id: integer
  user_name: string
  email: string
data_quality_rules:
  - field: email
    rule: "must be a valid email"
    pattern: "^[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\\.[A-Za-z]{2,}$"
slas:
  - name: "Data Freshness"
    metric: "freshness"
    threshold: 15  # minutes
```

## 🤝 Contributing
We welcome contributions! Please read [`CONTRIBUTING.md`](CONTRIBUTING.md) before submitting PRs.

## 📜 License
Badger is licensed under the **Apache 2.0 License**.

