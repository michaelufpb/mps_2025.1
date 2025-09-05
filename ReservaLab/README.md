# ReservaLab - Sistema de Gerenciamento de Reservas de Laboratórios

## Descrição

O ReservaLab é um sistema simples em linha de comando (CLI) para gerenciar reservas de laboratórios e salas. O objetivo é centralizar e organizar o processo de agendamento, permitindo cadastrar salas, registrar reservas, cancelar e consultar disponibilidade.

## Características

- **Interface CLI**: Interação via terminal com menus intuitivos
- **Persistência JSON**: Dados armazenados em arquivo JSON local
- **Controle de Conflitos**: Verificação automática de conflitos de horário
- **Sistema de Usuários**: Login com diferentes níveis de acesso (admin/usuário)
- **Validações**: Validação de dados de entrada e regras de negócio

## Estrutura do Projeto

```
ReservaLab/
├── app/
│   ├── __init__.py
│   └── main.py                 # Ponto de entrada do sistema
├── cli/
│   ├── __init__.py
│   └── reservalab_cli.py      # Interface de linha de comando
├── controller/
│   ├── __init__.py
│   ├── facade_singleton.py    # Ponto único de acesso
│   ├── gerente_lab.py         # Gerenciamento de laboratórios
│   ├── gerente_usuario.py     # Gerenciamento de usuários
│   └── gerente_reserva.py     # Gerenciamento de reservas
├── entity/
│   ├── __init__.py
│   ├── lab.py                 # Entidade Laboratório
│   ├── reserva.py             # Entidade Reserva
│   └── user.py                # Entidade Usuário
├── repository/
│   ├── __init__.py
│   └── json_repository.py     # Persistência em JSON
└── requirements.txt           # Dependências do projeto
```

## Como Executar

1. **Instalar dependências** (opcional, pois usa apenas bibliotecas padrão):
   ```bash
   pip install -r requirements.txt
   ```

2. **Executar o sistema**:
   ```bash
   python app/main.py
   ```

## Funcionalidades

### Para Usuários Comuns

- **Login/Cadastro**: Sistema de autenticação
- **Consultar Laboratórios**: Lista todos os laboratórios disponíveis
- **Consultar Disponibilidade**: Verifica disponibilidade em período específico
- **Fazer Reserva**: Cria nova reserva com validação de conflitos
- **Minhas Reservas**: Lista reservas do usuário
- **Cancelar Reserva**: Cancela reservas próprias

### Para Administradores

- **Gerenciar Laboratórios**: Cadastrar, listar, atualizar e remover laboratórios
- **Gerenciar Usuários**: Listar usuários cadastrados
- **Gerenciar Reservas**: Visualizar todas as reservas do sistema

## Usuário Padrão

O sistema cria automaticamente um usuário administrador padrão:
- **Login**: `admin`
- **Senha**: `Admin123!`

## Validações Implementadas

### Usuários
- Login: máximo 12 caracteres, sem números
- Senha: 8-128 caracteres, com maiúscula, minúscula, número e símbolo especial

### Laboratórios
- ID único obrigatório
- Nome obrigatório
- Capacidade maior que zero

### Reservas
- Data de início não pode ser no passado
- Data de fim deve ser posterior à data de início
- Duração máxima de 4 horas
- Verificação de conflitos com outras reservas ativas

## Persistência de Dados

Os dados são armazenados no arquivo `reservalab_data.json` na raiz do projeto, contendo:
- Lista de usuários
- Lista de laboratórios
- Lista de reservas

O arquivo é criado automaticamente na primeira execução e atualizado a cada operação.

## Padrões de Design Utilizados

- **Singleton**: FacadeSingleton para acesso único aos gerentes
- **Repository**: Padrão para abstração da persistência
- **Facade**: Interface simplificada para operações complexas
- **MVC**: Separação entre entidades, controllers e interface

## Exemplo de Uso

1. Execute o sistema: `python app/main.py`
2. Faça login com o usuário admin padrão
3. Cadastre alguns laboratórios
4. Crie um usuário comum
5. Faça logout e login como usuário comum
6. Consulte disponibilidade e faça reservas
