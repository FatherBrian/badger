import pandas as pd
from core.contracts import Contract

def validate_schema(df: pd.DataFrame, contract: Contract) -> dict:
    expected_types = {'int': 'int64', 'float': 'float64', 'str': 'object'}
    schema_results = {}
    details = []
    for field, type_ in contract.data_schema.items():
        if field not in df.columns:
            schema_results[field] = False
            details.append(f"Missing column: {field}")
        else:
            matches = df[field].dtype == expected_types[type_]
            schema_results[field] = matches
            if not matches:
                details.append(f"Type mismatch for {field}: expected {type_}, got {df[field].dtype}")
    status = all(schema_results.values())
    return {"schema": {"status": bool(status), "details": "All columns match expected types" if status else "; ".join(details)}}

def validate_sla(df: pd.DataFrame, contract: Contract) -> dict:
    completeness = 1 - df.isnull().any(axis=1).mean()
    status = completeness >= contract.sla.completeness
    details = f"Completeness {completeness:.2f} >= {contract.sla.completeness}" if status else f"Completeness {completeness:.2f} < {contract.sla.completeness}"
    return {"sla": {"status": bool(status), "details": details}}

def validate_rule(df: pd.DataFrame, rule: str) -> dict:
    field, op, val = rule.split()
    if op == '>':
        valid = df[field] > float(val)
        status = valid.all()
        details = f"'{rule}' passed" if status else f"'{rule}' failed - {len(df[~valid])} rows have {field} <= {val}"
        return {"rule": {"status": bool(status), "details": details}}
    return {"rule": {"status": False, "details": "Unsupported operator"}}

def validate_ai_checks(df: pd.DataFrame, contract: Contract) -> dict:
    results = {}
    # Drift
    for field_stat, baseline in contract.ai_checks.field_baselines.items():
        field = field_stat.replace('_mean', '').replace('_variance', '')
        if 'mean' in field_stat:
            mean = df[field].mean()
            drift_ok = abs(mean - baseline) / baseline <= 0.1
            details = f"Mean {mean:.1f} within 10% of {baseline}" if drift_ok else f"Mean {mean:.1f} drifted >10% from {baseline}"
            results[f'{field}_drift'] = {"status": bool(drift_ok), "details": details}
    # Labels
    if contract.ai_checks.labels == 'consistent':
        label_field = next((f for f in df.columns if f in ['churn', 'label', 'status']), None)
        if label_field:
            dups = df.duplicated('id', keep=False)
            if dups.any():
                inconsistent = df[dups].groupby('id')[label_field].nunique() > 1
                status = not inconsistent.any()
                details = "No inconsistent labels for duplicate IDs" if status else f"Inconsistent labels for {inconsistent.sum()} IDs"
                results['labels'] = {"status": bool(status), "details": details}
            else:
                results['labels'] = {"status": True, "details": "No duplicate IDs found"}
        else:
            results['labels'] = {"status": True, "details": "No label field identified"}
    return {"ai_checks": results}

def validate_data(contract: Contract, data_path: str) -> dict:
    df = pd.read_csv(data_path)
    results = {}
    results.update(validate_schema(df, contract))
    results.update(validate_sla(df, contract))
    results.update(validate_rule(df, contract.rules[0]))  # First rule only
    results.update(validate_ai_checks(df, contract))
    return results