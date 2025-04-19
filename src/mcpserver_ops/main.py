from server import main
import asyncio
import sys

def run():
    """Main entry point for the package."""
    asyncio.run(main("sse"))

if __name__ == "__main__":
    sys.exit(run())