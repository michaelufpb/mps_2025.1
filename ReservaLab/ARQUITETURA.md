# Arquitetura do Sistema ReservaLab

## Diagrama de Arquitetura

```
┌─────────────────────────────────────────────────────────────┐
│                        CLI Layer                            │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              ReservaLabCLI                             │ │
│  │  - Menu de Login                                       │ │
│  │  - Menu Admin                                          │ │
│  │  - Menu Usuário                                        │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                    Controller Layer                         │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              FacadeSingleton                           │ │
│  │  - Ponto único de acesso                               │ │
│  │  - Gerencia instâncias dos gerentes                    │ │
│  └─────────────────────────────────────────────────────────┘ │
│                                │                            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │GerenteLab   │ │GerenteUsuario│ │    GerenteReserva       │ │
│  │- Cadastrar  │ │- Cadastrar  │ │- Criar Reserva          │ │
│  │- Listar     │ │- Autenticar │ │- Cancelar Reserva        │ │
│  │- Atualizar  │ │- Listar     │ │- Consultar Disponib.    │ │
│  │- Remover    │ │             │ │- Verificar Conflitos     │ │
│  └─────────────┘ └─────────────┘ └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                     Entity Layer                            │
│  ┌─────────────┐ ┌─────────────┐ ┌─────────────────────────┐ │
│  │    Lab      │ │    User     │ │       Reserva           │ │
│  │- id         │ │- user_id    │ │- id                     │ │
│  │- nome       │ │- name       │ │- lab_id                 │ │
│  │- capacidade │ │- role       │ │- usuario_id             │ │
│  │- equipamentos│ │- password  │ │- data_inicio           │ │
│  └─────────────┘ └─────────────┘ │- data_fim               │ │
│                                  │- motivo                 │ │
│                                  │- status                 │ │
│                                  │- tem_conflito()         │ │
│                                  └─────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
                                │
                                ▼
┌─────────────────────────────────────────────────────────────┐
│                  Repository Layer                           │
│  ┌─────────────────────────────────────────────────────────┐ │
│  │              JSONRepository                            │ │
│  │  - Carrega dados do JSON                               │ │
│  │  - Salva dados no JSON                                 │ │
│  │  - Operações CRUD para todas as entidades              │ │
│  │  - Arquivo: reservalab_data.json                       │ │
│  └─────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────┘
```

## Fluxo de Dados

1. **CLI** recebe entrada do usuário
2. **FacadeSingleton** coordena operações
3. **Gerentes** aplicam regras de negócio
4. **Entidades** representam os dados
5. **Repository** persiste no arquivo JSON

## Padrões de Design Utilizados

- **Singleton**: FacadeSingleton garante uma única instância
- **Facade**: Interface simplificada para operações complexas
- **Repository**: Abstração da camada de persistência
- **MVC**: Separação clara entre Model, View e Controller

## Responsabilidades por Camada

### CLI Layer
- Interface com o usuário
- Validação de entrada
- Formatação de saída
- Navegação entre menus

### Controller Layer
- Regras de negócio
- Validações específicas
- Coordenação entre entidades
- Controle de fluxo

### Entity Layer
- Modelos de dados
- Validações básicas
- Métodos de negócio das entidades

### Repository Layer
- Persistência de dados
- Operações CRUD
- Serialização/Deserialização
- Gerenciamento de arquivos
