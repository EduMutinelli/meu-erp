

def get_user_permissions(cargo):
    """
    Retorna as permissões baseadas no cargo do usuário
    """
    permissoes = {
        'ADM': {
            'acesso': ['dashboard', 'clientes', 'produtos', 'vendas', 'fiscal', 'financeiro', 'configuracoes'],
            'editar': ['clientes', 'produtos', 'vendas', 'fiscal', 'financeiro'],
            'deletar': ['clientes', 'produtos', 'vendas', 'fiscal', 'financeiro'],
            'criar': ['clientes', 'produtos', 'vendas', 'fiscal', 'financeiro']
        },
        'financeiro': {
            'acesso': ['dashboard', 'clientes', 'produtos', 'vendas', 'financeiro'],
            'editar': ['clientes', 'produtos', 'vendas', 'financeiro'],
            'deletar': ['financeiro'],
            'criar': ['clientes', 'produtos', 'vendas', 'financeiro']
        },
        'usuario': {
            'acesso': ['dashboard', 'produtos'],
            'editar': ['produtos'],
            'deletar': [],
            'criar': ['produtos']
        }
    }
    
    return permissoes.get(cargo, permissoes['usuario'])

def can_access(cargo, modulo):
    """Verifica se usuário pode acessar um módulo"""
    permissoes = get_user_permissions(cargo)
    return modulo in permissoes['acesso']

def can_edit(cargo, modulo):
    """Verifica se usuário pode editar em um módulo"""
    permissoes = get_user_permissions(cargo)
    return modulo in permissoes['editar']

def can_delete(cargo, modulo):
    """Verifica se usuário pode deletar em um módulo"""
    permissoes = get_user_permissions(cargo)
    return modulo in permissoes['deletar']

def can_create(cargo, modulo):
    """Verifica se usuário pode criar em um módulo"""
    permissoes = get_user_permissions(cargo)
    return modulo in permissoes['criar']