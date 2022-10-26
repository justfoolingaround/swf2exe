import io
import pathlib

import click
import httpx
from rich.console import Console
from rich.progress import Progress

from swf2exe import combine_player_and_swf, is_projector_valid, is_swf_valid

PROJECTOR_NAME = "flashplayer_32_sa.exe"
PROJECTOR_URL = (
    f"https://archive.org/download/adobe-flash-player-projector/{PROJECTOR_NAME}"
)


@click.command()
@click.argument("swf_file", type=click.Path(exists=True))
@click.option("-o", "--output", type=click.Path(), help="User specified output file")
@click.option(
    "-p", "--projector", type=click.Path(), help="User specified projector file"
)
@click.option(
    "--clean", is_flag=True, help="Supress all file IO except for the output file"
)
def swf2exe__main__(swf_file, output, projector, clean):

    console = Console(stderr=True)
    session = httpx.Client()

    projector = pathlib.Path(projector or PROJECTOR_NAME)

    if projector.exists():
        projector_io = projector.open("rb")
    else:
        console.print("[red]Could not find the projector file.[/]")
        projector_io = io.BytesIO()

        with session.stream("GET", PROJECTOR_URL, follow_redirects=True) as response:

            with Progress() as progress:
                task = progress.add_task(
                    "Downloading projector",
                    total=int(response.headers["content-length"]),
                )
                for chunk in response.iter_bytes():
                    projector_io.write(chunk)
                    progress.update(task, advance=len(chunk))

        projector_io.seek(0)
        projector_name = PROJECTOR_NAME

        if not clean:
            projector.write_bytes(projector_io.read())
        else:
            projector_name = "memory"

        console.print(
            "[green]Downloaded the projector file to [bold]%s[/].[/]" % projector_name
        )

    if not is_projector_valid(projector_io):
        console.print("[yellow]The projector file obtained may be corrupted.[/]")

    swf_file = pathlib.Path(swf_file)
    swf_file_io = swf_file.open("rb")

    if not is_swf_valid(swf_file_io):
        console.print("[red]The swf file does not have a valid signature.[/]")

    with open(outpath := (output or swf_file.with_suffix(".exe")), "wb") as output_file:
        output_file.write(combine_player_and_swf(projector_io, swf_file_io).read())

    console.print("[green]Compiled the SWF file to [bold]%s[/].[/]" % outpath.name)


if __name__ == "__main__":
    swf2exe__main__()
