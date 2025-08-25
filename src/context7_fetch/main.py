import typer
from rich import box
from rich.console import Console
from rich.table import Table

from context7_fetch.context7.client import Client

app = typer.Typer(
    name="context7-fetch",
    help="Fetch docs from context7.com",
    add_completion=False,
    no_args_is_help=True,
)
console = Console()


@app.command("trending")
def trending():
    # TODO: fetch trending projects
    pass


@app.command("search")
def search(query: str = typer.Argument(..., help="The query to search for")):
    typer.secho(f"Searching for {query}", fg=typer.colors.CYAN)
    r = Client().search(query)
    typer.secho(f"Found {len(r.results)} results", fg=typer.colors.GREEN)
    results = r.results
    results.sort(key=lambda x: (x.settings.stars or -1), reverse=True)

    table = Table(
        title=f"Results for: {query} ({len(results)})",
        header_style="bold cyan",
        box=box.SIMPLE_HEAVY,
        show_lines=False,
    )
    table.add_column("#", style="bold green")
    table.add_column("Trust", justify="right")
    table.add_column("Title", justify="left")
    table.add_column("Type", justify="center")
    table.add_column("⭐", justify="center")
    table.add_column("Tokens", justify="right")
    table.add_column("Snippets", justify="right")
    table.add_column("Source", justify="center")
    table.add_column("txt url", justify="center")

    for i, result in enumerate(results):
        st = result.settings
        ver = result.version
        table.add_row(
            str(i),
            str(st.trust_score if st.trust_score is not None else ""),
            st.title or "",
            (st.source_type.value if st.source_type else ""),
            str(st.stars if st.stars is not None else ""),
            str(ver.total_tokens) if (ver and ver.total_tokens is not None) else "",
            str(ver.total_snippets) if (ver and ver.total_snippets is not None) else "",
            st.docs_site_url or st.docs_repo_url or "",
            ("https://context7.com" + st.project + "/llms.txt") if st.project else "",
        )

    console.print(table)

    # TODO: add batch downloads
    while True:
        prompt = typer.prompt("Do you want to download the docs? (number/exit)")
        match prompt:
            case "exit":
                return

            case prompt if prompt.isdigit():
                result = results[int(prompt)]
                project_page = "https://context7.com" + result.settings.project
                docs = Client().fetch_docs(project_page)
                with open(f"{result.settings.title}.txt", "w", encoding="utf-8") as f:
                    f.write(docs)
                typer.secho(
                    f"Docs fetched for {result.settings.title} | {project_page}",
                    fg=typer.colors.GREEN,
                )
                break
            case _:
                typer.secho("Invalid input", fg=typer.colors.RED)
