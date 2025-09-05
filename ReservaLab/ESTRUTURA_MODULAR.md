# Estrutura Modular do CLI ReservaLab

## Organização dos Módulos CLI

A interface CLI foi separada em módulos especializados, cada um responsável por uma "tela" específica:

```
cli/
├── __init__.py
├── reservalab_cli.py      # CLI principal - orquestra todos os módulos
├── base_cli.py           # Funcionalidades comuns para todas as telas
├── login_cli.py          # Tela de login e cadastro
├── admin_cli.py          # Menu administrativo
├── usuario_menu_cli.py   # Menu do usuário comum
├── lab_cli.py           # Gerenciamento de laboratórios
├── usuario_cli.py       # Gerenciamento de usuários
└── reserva_cli.py       # Gerenciamento de reservas
```

## Responsabilidades por Módulo

### `base_cli.py` - Funcionalidades Comuns
- **Propósito**: Classe base com métodos utilitários compartilhados
- **Responsabilidades**:
  - Formatação de cabeçalhos e seções
  - Leitura de entrada do usuário (texto, números, datas)
  - Exibição de listas e mensagens
  - Confirmações e validações básicas

### `login_cli.py` - Tela de Login
- **Propósito**: Gerencia autenticação e cadastro de usuários
- **Responsabilidades**:
  - Menu de login
  - Processamento de login
  - Cadastro de novos usuários
  - Retorno de usuário autenticado

### `admin_cli.py` - Menu Administrativo
- **Propósito**: Coordena funcionalidades administrativas
- **Responsabilidades**:
  - Menu principal do admin
  - Delegação para módulos específicos (labs, usuários, reservas)
  - Controle de fluxo administrativo

### `usuario_menu_cli.py` - Menu do Usuário
- **Propósito**: Funcionalidades para usuários comuns
- **Responsabilidades**:
  - Consulta de laboratórios
  - Consulta de disponibilidade
  - Criação de reservas
  - Visualização de reservas próprias
  - Cancelamento de reservas

### `lab_cli.py` - Gerenciamento de Laboratórios
- **Propósito**: Operações CRUD de laboratórios
- **Responsabilidades**:
  - Cadastro de laboratórios
  - Listagem de laboratórios
  - Atualização de laboratórios
  - Remoção de laboratórios
  - Menu específico de labs

### `usuario_cli.py` - Gerenciamento de Usuários
- **Propósito**: Operações de usuários (admin)
- **Responsabilidades**:
  - Listagem de usuários
  - Menu específico de usuários

### `reserva_cli.py` - Gerenciamento de Reservas
- **Propósito**: Operações de reservas (admin)
- **Responsabilidades**:
  - Listagem de todas as reservas
  - Menu específico de reservas

### `reservalab_cli.py` - CLI Principal
- **Propósito**: Orquestra todos os módulos CLI
- **Responsabilidades**:
  - Inicialização do sistema
  - Controle de fluxo principal
  - Gerenciamento de estado do usuário logado
  - Delegação para módulos apropriados

## Fluxo de Execução

```
ReservaLabCLI.iniciar()
    ↓
ReservaLabCLI.processar_login()
    ↓
LoginCLI.processar_menu_login()
    ↓ (se login bem-sucedido)
ReservaLabCLI.processar_menu_logado()
    ↓
AdminCLI.processar_menu_admin() OU UsuarioMenuCLI.processar_menu_usuario()
    ↓
Módulos específicos (LabCLI, UsuarioCLI, ReservaCLI)
```

## Vantagens da Estrutura Modular

1. **Separação de Responsabilidades**: Cada módulo tem uma responsabilidade específica
2. **Manutenibilidade**: Mudanças em uma tela não afetam outras
3. **Reutilização**: BaseCLI fornece funcionalidades comuns
4. **Testabilidade**: Cada módulo pode ser testado independentemente
5. **Escalabilidade**: Fácil adicionar novas telas ou funcionalidades
6. **Legibilidade**: Código mais organizado e fácil de entender

## Padrões Utilizados

- **Template Method**: BaseCLI define estrutura comum
- **Strategy**: Diferentes CLIs para diferentes tipos de usuário
- **Facade**: ReservaLabCLI simplifica acesso aos módulos
- **Composition**: Módulos são compostos conforme necessário
