# Badger

**Badger** is an open-source tool that empowers data teams to define, validate, and observe data pipelines through declarative data contracts. With a unique focus on schema rules, SLAs, dependencies, and AI-specific validation (like schema drift), Badger bridges the gap between data quality, observability, and AI readiness—all in a lightweight, extensible package.

**Version**: 0.1.0  
**Status**: MVP (Pre-Release)  
**License**: MIT  
**Repository**: [github.com/fatherbrian/badger](#) *(Update with your actual repo URL)*

---

## Why Badger?

Data pipelines are growing more complex, and AI workflows demand stricter quality controls. Existing tools focus on either validation (e.g., Great Expectations) or observability (e.g., Monte Carlo), but few combine enforceable contracts with AI-ready features. Badger Core offers:

- **Contracts First**: Define explicit expectations for schema, SLAs, rules, and dependencies.
- **Observability Built-In**: Track pipeline health with minimal setup.
- **AI Focus**: Validate datasets and detect drift for ML workloads.
- **Simple & Open**: No SaaS lock-in—just a Python tool you can run anywhere.

---

## Core Features

### 1. Creating and Managing Contracts
Define data contracts in YAML with schema rules, SLAs, basic rules, and dependencies.

- **Capabilities**:
  - Schema: Field types, nullability constraints.
  - SLAs: Latency, freshness requirements.
  - Rules: Uniqueness, range checks, etc.
  - Dependencies: Link to upstream data objects.
- **Example**:
  ```yaml
  contract:
    name: user_events
    owner: data_team@example.com
    dependencies:
      - table: raw_events
    schema:
      - field: user_id, type: string, nullable: false
      - field: event_time, type: datetime
    sla:
      latency: 10s
      freshness: 24h
    rules:
      - no_duplicates: user_id
      - range: event_time, min: "2023-01-01"
  
### 2. Validation Engine
A lightweight Python engine to compare data against defined contracts.

- **Capabilities**:
  - Validates schema, rules, and SLAs.
  - Supports CSV files or in-memory Pandas DataFrames.
  - Returns pass/fail status with detailed error messages.
- **Tech**: Pydantic for schema validation, custom logic for rules and SLAs.

### 3. Basic Observability for Contracts
Monitor contract adherence with simple, built-in metrics.

- **Capabilities**:
  - Tracks validation latency and error rates.
  - Outputs results to the terminal and JSON logs.
- **Example Output**:
``` 
Validation: PASSED
Latency: 2.3s
Error Rate: 0%
```

### 4. AI Contracts
Specialized rules for AI pipelines, including schema drift detection.

- **Capabilities**:
- Detects schema drift against a baseline dataset.
- Validates ranges and null values for machine learning features.
- **Example Contract**:
```yaml
contract:
  name: training_data
  owner: ml_team@example.com
  schema:
    - field: feature_x, type: float, nullable: false
  ai_rules:
    - drift: feature_x, baseline: baseline.csv
    - range: feature_x, min: 0, max: 1
```

### 5. CLI 
A developer-friendly command-line interface for easy interaction.

- **Commands**
- badger check <contract> <data>: Validate data against a contract.
- badger observe <contract>: Display observability metrics.
- badger --version: Show the current version.

### 6. Python SDK
Programmatically integrate Badger into your data pipelines.

- **API**
- badger.validate(data, contract_path): Validate data against a contract.
- badger.get_metrics(contract_path): Retrieve observability metrics.
- **Example Usage**
```
import badger
result = badger.validate("data.csv", "contract.yaml")
print(f"Passed: {result.passed}, Errors: {result.errors}")
```
---
## Architecture
- Language: Python 3.9+
- Dependencies:
  - pydantic: For schema validation
  - pyyaml: For parsing YAML contracts
  - pandas: For data processing
  - typer: For the CLI framework

- Storage: SQLite (local storage for metrics)
- Execution: Single-node, no external services required
- **Workflow**
  - Define a contract in YAML.
  - Use the CLI (badger check) or SDK (badger.validate()) to validate data.
  - The validation engine checks the data against schema, rules, SLAs, and AI-specific constraints.
  - Results and metrics are displayed or logged for observability.

---
## Installation
1. Clone the repo
```
git clone https://github.com/fatherbrian/badger.git
cd badger
```
2. Install the package
```
pip install .
```
3. Verify installation
```
badger --version
```
*Note*: Requires Python 3.9+. It is recommended to use a virtual environment (venv).

---
## Contributing
Badger Core is a community-driven project, and your contributions are welcome! Here’s how you can get involved:
- Report Bugs: Open an issue on GitHub.
- Add Features: Submit a pull request (e.g., for new validation rules or integrations).
- Improve Documentation: Fix typos or add new examples.
For more details, see CONTRIBUTING.md.

---
## Roadmap
v0.2: Integrate with major data tools (Kafka, Airflow, dbt).
v0.3: Add support for distributed validation (e.g., internal Kafka queue, clusters).
v1.0: Introduce a web UI and advanced AI features.

---
## License
Badger Core is licensed under the MIT License. See LICENSE (#) for details.

