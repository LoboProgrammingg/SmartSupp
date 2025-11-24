#!/usr/bin/env python3
"""
Script para iniciar o servidor de desenvolvimento em background
com logs redirecionados para arquivo
"""
import subprocess
import sys
from pathlib import Path


def main() -> None:
    """Inicia o servidor uvicorn em background"""
    log_dir = Path(__file__).parent.parent / "logs"
    log_dir.mkdir(exist_ok=True)
    log_file = log_dir / "api.log"
    
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
    
    print(f"🚀 Iniciando API em background...")
    print(f"📝 Logs serão salvos em: {log_file}")
    print(f"👀 Para acompanhar: tail -f {log_file}")
    print(f"🛑 Para parar: pkill -f 'uvicorn.*8003'")
    print()
    
    with open(log_file, "a") as f:
        process = subprocess.Popen(
            cmd,
            stdout=f,
            stderr=subprocess.STDOUT,
            bufsize=1,
            universal_newlines=True,
        )
    
    print(f"✅ API iniciada (PID: {process.pid})")
    print(f"🌐 Acesse: http://localhost:8003/docs")
    print()
    print(f"Para ver logs em tempo real, execute:")
    print(f"  tail -f {log_file}")


if __name__ == "__main__":
    main()

