#!/usr/bin/env python3

import os

import uvicorn


def main() -> None:
    """
    Entrypoint for development: run the application in uvicorn (with automatic code reload).
    """
    port = int(os.environ.get("PORT", "5000"))
    uvicorn.run(
        "app.core.app:create_app",
        factory=True,
        host="0.0.0.0",
        port=port,
        reload=True,
    )


if __name__ == "__main__":
    main()
