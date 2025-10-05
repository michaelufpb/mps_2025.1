from typing import List
from entity.lab import Lab
from repository.json_repository import JSONRepository
from entity.memento import LabOriginator, Memento

class GerenteLab:
    def __init__(self, repository: JSONRepository):
        self.dao = repository.lab_dao
        self.repository = repository  # Manter para acesso a _save_data
        self.mementos = {}  # lab_id: Memento
    
    def cadastrar_lab(self, lab_id: str, nome: str, capacidade: int, equipamentos: List[str] = None) -> bool:
        """Cadastra um novo laboratório"""
        try:
            # Verifica se já existe um lab com esse ID
            if self.dao.get_lab_by_id(lab_id):
                print(f"Erro: Laboratório com ID '{lab_id}' já existe.")
                return False
            
            # Validações básicas
            if not lab_id or not nome:
                print("Erro: ID e nome do laboratório são obrigatórios.")
                return False
            
            if capacidade <= 0:
                print("Erro: Capacidade deve ser maior que zero.")
                return False
            
            lab = Lab(lab_id, nome, capacidade, equipamentos)
            self.dao.add_lab(lab)  # Usar DAO para adicionar
            self.repository._save_data()  # Salvar alterações no JSON
            print(f"Laboratório '{nome}' cadastrado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao cadastrar laboratório: {e}")
            return False
    
    def listar_labs(self) -> List[Lab]:
        """Lista todos os laboratórios"""
        return self.dao.get_all_labs()
    
    def buscar_lab(self, lab_id: str) -> Lab:
        """Busca um laboratório por ID"""
        return self.dao.get_lab_by_id(lab_id)
    
    def atualizar_lab(self, lab_id: str, nome: str = None, capacidade: int = None, 
                     equipamentos: List[str] = None) -> bool:
        """Atualiza um laboratório existente"""
        try:
            lab = self.dao.get_lab_by_id(lab_id)
            if not lab:
                print(f"Erro: Laboratório com ID '{lab_id}' não encontrado.")
                return False
            
            # Salvar memento antes da atualização
            originator = LabOriginator(lab)
            self.mementos[lab_id] = originator.save()
            
            # Atualiza apenas os campos fornecidos
            if nome is not None:
                lab.nome = nome
            if capacidade is not None:
                if capacidade <= 0:
                    print("Erro: Capacidade deve ser maior que zero.")
                    return False
                lab.capacidade = capacidade
            if equipamentos is not None:
                lab.equipamentos = equipamentos
            
            self.dao.update_lab(lab)
            self.repository._save_data()  # Salvar alterações
            print(f"Laboratório '{lab_id}' atualizado com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao atualizar laboratório: {e}")
            return False
    
    def remover_lab(self, lab_id: str) -> bool:
        """Remove um laboratório"""
        try:
            lab = self.dao.get_lab_by_id(lab_id)
            if not lab:
                print(f"Erro: Laboratório com ID '{lab_id}' não encontrado.")
                return False
            
            # Verifica se há reservas ativas para este lab
            reservas = self.repository.reserva_dao.get_reservas_by_lab(lab_id)
            reservas_ativas = [r for r in reservas if r.status == "ativa"]
            
            if reservas_ativas:
                print(f"Erro: Não é possível remover o laboratório '{lab_id}' pois há {len(reservas_ativas)} reserva(s) ativa(s).")
                return False
            
            self.dao.delete_lab(lab_id)
            self.repository._save_data()  # Salvar alterações
            print(f"Laboratório '{lab_id}' removido com sucesso!")
            return True
            
        except Exception as e:
            print(f"Erro ao remover laboratório: {e}")
            return False
    
    def undo_update_lab(self, lab_id: str) -> bool:
        if lab_id in self.mementos:
            lab = self.dao.get_lab_by_id(lab_id)
            if lab:
                originator = LabOriginator(lab)
                originator.restore(self.mementos[lab_id])
                self.dao.update_lab(lab)
                self.repository._save_data()  # Salvar alterações
                del self.mementos[lab_id]
                print(f"Última atualização desfeita para o laboratório '{lab_id}'.")
                return True
            else:
                print(f"Erro: Laboratório '{lab_id}' não encontrado.")
                return False
        else:
            print(f"Erro: Não há atualização recente para desfazer no laboratório '{lab_id}'.")
            return False