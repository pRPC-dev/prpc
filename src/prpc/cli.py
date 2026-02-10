import typer
from rich.console import Console
from rich.panel import Panel

app = typer.Typer(
    name="prpc",
    help="prpc CLI - A modern Python library project",
    add_completion=False,
)
console = Console()

@app.command()
def hello(name: str = "World"):
    """
    Say hello to someone.
    """
    console.print(
        Panel.fit(
            f"Hello [bold magenta]{name}[/bold magenta]! Welcome to [bold cyan]prpc[/bold cyan].",
            title="prpc CLI",
            border_style="green",
        )
    )

@app.command()
def codegen(
    module: str = typer.Option(..., "--module", "-m", help="Python module to introspect"),
    output: str = typer.Option("client.ts", "--output", "-o", help="Output TypeScript file path"),
):
    """
    Generate a TypeScript client from registered procedures.
    """
    import importlib
    import sys
    import os
    from . import default_registry, save_typescript_client

    console.print(f"Generating TypeScript client for module: [bold cyan]{module}[/bold cyan]")
    
    # Ensure current directory is in path
    sys.path.append(os.getcwd())
    
    try:
        importlib.import_module(module)
    except ImportError as e:
        console.print(f"[bold red]Error:[/bold red] Could not import module '{module}': {e}")
        raise typer.Exit(code=1)

    save_typescript_client(default_registry, output)
    console.print(f"Successfully generated [bold green]{output}[/bold green]")


@app.command()
def version():
    """
    Show the version of prpc.
    """
    from . import __version__
    console.print(f"prpc version: [bold cyan]{__version__}[/bold cyan]")

if __name__ == "__main__":
    app()
