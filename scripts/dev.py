#!/usr/bin/env python3
"""
Script para iniciar o servidor de desenvolvimento
"""
import subprocess
import sys


def main() -> None:
    """Inicia o servidor uvicorn"""
    cmd = [
        "uvicorn",
        "src.main:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8003",
    ]
    sys.exit(subprocess.run(cmd).returncode)


if __name__ == "__main__":
    main()

