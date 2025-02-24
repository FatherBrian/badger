from core.contracts import Contract

def get_lineage(contract: Contract) -> str:
    return f"{contract.lineage.source} -> {contract.lineage.version}"