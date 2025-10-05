from abc import ABC, abstractmethod
from repository.json_repository import JSONRepository
from entity.reserva import Reserva
from typing import Dict

class ReportGenerator(ABC):
    def __init__(self, repository: JSONRepository):
        self.repository = repository

    def generate_report(self):
        data = self.collect_data()
        content = self.format_content(data)
        self.save_report(content)

    def collect_data(self) -> Dict[str, int]:
        # Coletar estatísticas de reservas ativas por usuário (como proxy para "acesso")
        reservas = self.repository.get_all_reservas()
        stats: Dict[str, int] = {}
        for r in reservas:
            if r.status == "ativa":
                stats[r.usuario_id] = stats.get(r.usuario_id, 0) + 1
        return stats

    @abstractmethod
    def format_content(self, data: Dict[str, int]) -> str:
        pass

    @abstractmethod
    def save_report(self, content: str):
        pass

class HTMLReportGenerator(ReportGenerator):
    def format_content(self, data: Dict[str, int]) -> str:
        html = "<html><body><h1>Estatísticas de Acesso (Reservas Ativas por Usuário)</h1><ul>"
        for user, count in data.items():
            html += f"<li>Usuário {user}: {count} reservas</li>"
        html += "</ul></body></html>"
        return html

    def save_report(self, content: str):
        with open("relatorio_acesso.html", "w", encoding="utf-8") as f:
            f.write(content)
        print("Relatório HTML gerado em 'relatorio_acesso.html'!")

class PDFReportGenerator(ReportGenerator):
    def format_content(self, data: Dict[str, int]) -> str:
        # Simulação simples de PDF (poderia usar uma lib como reportlab, mas para exemplo, texto plano)
        pdf_text = "Estatísticas de Acesso (Reservas Ativas por Usuário)\n\n"
        for user, count in data.items():
            pdf_text += f"Usuário {user}: {count} reservas\n"
        return pdf_text

    def save_report(self, content: str):
        with open("relatorio_acesso.pdf.txt", "w", encoding="utf-8") as f:  # Extensão .txt para simulação
            f.write(content)
        print("Relatório PDF simulado gerado em 'relatorio_acesso.pdf.txt'!")