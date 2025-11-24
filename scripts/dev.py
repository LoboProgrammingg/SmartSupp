#!/usr/bin/env python3
"""
Script para iniciar o servidor de desenvolvimento
"""
import subprocess
import sys
import os
from pathlib import Path


def main() -> None:
    """Inicia o servidor uvicorn"""
    # Criar diretório de logs se não existir
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    
    # Configurar variáveis de ambiente para logs
    os.environ["PYTHONUNBUFFERED"] = "1"
    
    cmd = [
        "uvicorn",
        "src.main:app",
        "--reload",
        "--host",
        "0.0.0.0",
        "--port",
        "8003",
        "--log-level",
        "info",
    ]
    
    # Se rodando em background (detectado por não ter TTY), redirecionar logs
    if not sys.stdout.isatty():
        log_file = log_dir / "api.log"
        with open(log_file, "a") as f:
            sys.exit(subprocess.run(cmd, stdout=f, stderr=f).returncode)
    else:
        # Foreground: logs vão para stdout
        sys.exit(subprocess.run(cmd).returncode)


if __name__ == "__main__":
    main()

