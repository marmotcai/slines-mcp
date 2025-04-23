from server import main
import asyncio
import sys
import click

@click.command()
@click.option(
    "--transport",
    type=click.Choice(["stdio", "sse"]),
    default="stdio",
    help="Transport type",
)
def run(transport: str) -> int:
    """Main entry point for the package."""
    if transport == "sse":
        print(f"Starting server with SSE transport")
        # Add logic to start the server with SSE transport
        asyncio.run(main(transport))
    elif transport == "stdio":
        print("Starting server with stdio transport")
        asyncio.run(main(transport))

if __name__ == "__main__":
    sys.exit(run())