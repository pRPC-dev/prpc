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
def version():
    """
    Show the version of prpc.
    """
    from . import __version__
    console.print(f"prpc version: [bold cyan]{__version__}[/bold cyan]")

if __name__ == "__main__":
    app()
