from cli.base_cli import BaseCLI
from entity.user import User

class LoginCLI(BaseCLI):
    """CLI para login e cadastro de usuários"""
    
    def exibir_menu_login(self) -> str:
        """Exibe menu de login e retorna opção escolhida"""
        self.exibir_cabecalho("MENU DE LOGIN")
        print("1. Fazer login")
        print("2. Cadastrar novo usuário")
        print("3. Sair")
        
        return self.ler_opcao()
    
    def fazer_login(self) -> User:
        """Realiza login do usuário"""
        user_id = self.ler_texto("Login")
        password = self.ler_texto("Senha")
        
        usuario = self.facade.autenticar_usuario(user_id, password)
        if usuario:
            self.exibir_sucesso(f"Bem-vindo, {usuario.name}!")
            return usuario
        else:
            self.exibir_erro("Login ou senha inválidos!")
            return None
    
    def cadastrar_usuario(self) -> bool:
        """Cadastra novo usuário"""
        self.exibir_secao("CADASTRO DE USUÁRIO")
        
        user_id = self.ler_texto("Login (máx 12 caracteres, sem números)")
        name = self.ler_texto("Nome completo")
        password = self.ler_texto("Senha (min 8 caracteres, com maiúscula, minúscula, número e símbolo)")
        
        sucesso = self.facade.get_gerente_usuario().cadastrar_usuario(user_id, name, "usuario", password)
        if sucesso:
            self.exibir_sucesso("Usuário cadastrado com sucesso! Faça login para continuar.")
            return True
        return False
    
    def processar_menu_login(self) -> tuple[User, bool]:
        """
        Processa menu de login
        Retorna: (usuario_logado, deve_continuar)
        """
        opcao = self.exibir_menu_login()
        
        if opcao == "1":
            usuario = self.fazer_login()
            return usuario, True
        elif opcao == "2":
            self.cadastrar_usuario()
            return None, True
        elif opcao == "3":
            print("Obrigado por usar o ReservaLab!")
            return None, False
        else:
            self.exibir_erro("Opção inválida!")
            return None, True
