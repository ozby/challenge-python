"""Main entry point for the echo server."""

import asyncio

from server.server import logger, run_server

if __name__ == "__main__":
    try:
        asyncio.run(run_server())
    except KeyboardInterrupt:
        logger.warning("Server stopped by user")
