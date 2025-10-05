import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cli.reservalab_cli import ReservaLabCLI

def main():
    """Função principal que inicia o sistema ReservaLab"""
    cli = ReservaLabCLI()
    cli.iniciar()

if __name__ == "__main__":
    main()