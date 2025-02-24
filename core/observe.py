import json

def observe_results(results: dict) -> str:
    return json.dumps(results, indent=2)