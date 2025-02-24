from src.contract import load_contract

def test_load_contract():
    contract = load_contract("examples/user_events.yaml")
    assert contract.name == "user_events"
    assert len(contract.schema) == 2