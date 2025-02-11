import yaml
import pandas as pd
import re
from scipy.stats import ks_2samp
import numpy as np

class BadgerValidator:
    def __init__(self, contract_path):
        with open(contract_path, 'r') as file:
            self.contract = yaml.safe_load(file)
        self.errors = []

    def validate_schema(self, df):
        """Validate schema against the contract."""
        required_fields = self.contract.get('required_fields', [])
        field_types = self.contract.get('field_types', {})
        
        for field in required_fields:
            if field not in df.columns:
                self.errors.append(f"Missing required field: {field}")

        for field, expected_type in field_types.items():
            if field in df.columns:
                actual_type = df[field].dtype
                if not self._validate_dtype(actual_type, expected_type):
                    self.errors.append(f"Field {field} has incorrect type: expected {expected_type}, found {actual_type}")
    
    def _validate_dtype(self, actual_type, expected_type):
        """Maps Pandas dtypes to expected contract types."""
        type_mapping = {
            'integer': 'int',
            'float': 'float',
            'string': 'object',
            'boolean': 'bool'
        }
        return type_mapping.get(expected_type) in str(actual_type)
    
    def validate_data_quality(self, df):
        """Validate data quality rules from the contract."""
        rules = self.contract.get('data_quality_rules', [])
        for rule in rules:
            field = rule['field']
            if field in df.columns:
                if 'pattern' in rule:
                    pattern = re.compile(rule['pattern'])
                    invalid_values = df[~df[field].astype(str).str.match(pattern)]
                    if not invalid_values.empty:
                        self.errors.append(f"Field {field} has invalid values that do not match pattern {rule['pattern']}")
                if 'condition' in rule:
                    condition = rule['condition']
                    if not df.eval(f"{field} {condition}").all():
                        self.errors.append(f"Field {field} failed condition: {condition}")
    
    def validate_feature_drift(self, df, reference_df):
        """Detects feature drift using Kolmogorov-Smirnov test."""
        drift_rules = self.contract.get('ai_specific_validations', [])
        for rule in drift_rules:
            if rule['name'] == 'Feature Drift':
                threshold = rule['threshold']
                for feature in df.columns:
                    if feature in reference_df.columns and df[feature].dtype in [np.float64, np.int64]:
                        ks_stat, p_value = ks_2samp(df[feature].dropna(), reference_df[feature].dropna())
                        if p_value < threshold:
                            self.errors.append(f"Feature drift detected in {feature} (p-value={p_value:.4f})")
    
    def run_validations(self, df, reference_df=None):
        """Run all validations and return errors."""
        self.errors = []
        self.validate_schema(df)
        self.validate_data_quality(df)
        if reference_df is not None:
            self.validate_feature_drift(df, reference_df)
        return self.errors
