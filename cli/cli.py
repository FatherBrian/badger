import click
from core.contracts import load_contract
from core.validate import validate_data
from core.lineage import get_lineage
from core.observe import observe_results

@click.group(invoke_without_command=True)
@click.pass_context
def cli(ctx):
    """Badger: Data contract validation and observability."""
    if ctx.invoked_subcommand is None:
        click.echo(ctx.get_help())

@cli.command()
@click.option('--contract', required=True, help='Path to YAML contract')
@click.option('--data', required=True, help='Path to CSV data')
def validate(contract, data):
    """Validate a dataset against a contract."""
    contract_obj = load_contract(contract)
    results = validate_data(contract_obj, data)
    lineage = get_lineage(contract_obj)

    click.echo(f"Loaded contract for {contract_obj.dataset}")
    click.echo(f"Lineage: {lineage}")
    click.echo(click.style("Validation Results:", bold=True))

    # Schema
    schema = results["schema"]
    status_str = "[PASS]" if schema["status"] else "[FAIL]"
    color = "green" if schema["status"] else "red"
    click.echo(click.style(f"  Schema: {status_str} {schema['details']}", fg=color))

    # SLA
    sla = results["sla"]
    status_str = "[PASS]" if sla["status"] else "[FAIL]"
    color = "green" if sla["status"] else "red"
    click.echo(click.style(f"  SLA: {status_str} {sla['details']}", fg=color))

    # Rule
    rule = results["rule"]
    status_str = "[PASS]" if rule["status"] else "[FAIL]"
    color = "green" if rule["status"] else "red"
    click.echo(click.style(f"  Rule: {status_str} {rule['details']}", fg=color))

    # AI Checks
    click.echo("  AI Checks:")
    ai_checks = results["ai_checks"]
    for check, result in ai_checks.items():
        status_str = "[PASS]" if result["status"] else "[FAIL]"
        color = "green" if result["status"] else "red"
        click.echo(click.style(f"    {check.capitalize()}: {status_str} {result['details']}", fg=color))

    # JSON
    click.echo(click.style("\nJSON Output:", bold=True))
    click.echo(observe_results(results))

if __name__ == '__main__':
    cli()