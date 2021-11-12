"""The goal in this module is to define functions that take a formula as input and
do some computation on its syntactic structure. """


from formula import *

# MOSTRAR O TAMANHO DE UMA FÓRMULA
def length(formula):

    if isinstance(formula, Atom): # Se a formula for uma atômica
        return 1

    if isinstance(formula, Not): # Se a formula for uma negação
        return length(formula.inner) + 1

    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or): # Se a formula possuir um conectivo binário
        return length(formula.left) + length(formula.right) + 1


# MOSTRAR AS SUBFÓRMULAS DE UMA FÓRMULA
def subformulas(formula, vetor = []):

    vetorS = [] # vetor para guardar as strings das subsformulas

    if isinstance(formula, Atom): # Se a formula for uma atômica
        vetor.append(formula) # Guardar a formula atomica no vetor
        return formula # retornar a formula
    
    elif isinstance(formula, Not): # Se a formula for uma negação
        vetor.append(formula) # guardar a formula negada no vetor
        subformulas(formula.inner, vetor) # Chamar novamente a função subformulas dessa vez com a formula dentro da negação
        
    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or): # Se a formula possuir um conectivo binário
        vetor.append(formula) # guardar a formula com conectivo no vetor
        subformulas(formula.left, vetor) # Chamar novamente a função subformulas dessa vez com a formula esquerda da formula com conectivo
        subformulas(formula.right, vetor) # Chamar novamente a função subformulas dessa vez com a formula direita da formula com conectivo
        
    for elemento in vetor: # guardar as strings das subformulas no vetorS
            vetorS.append(f'{elemento}')

    return list(dict.fromkeys(vetorS)) # retornar o vetorS sem repetições


# MOSTRAR TODAS AS ATÔMICAS DE UMA FÓRMULA
def atoms(formula, vetor = []):

    vetorS = [] # vetor para armazenar as string das atomicas

    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        vetor.append(atoms(formula.right, vetor)) # adicionar o resultado da chamada da função atoms no vetor
        vetor.append(atoms(formula.left, vetor)) # adicionar o resultado da chamada da função atoms no vetor

    elif isinstance(formula, Not):
        vetor.append(atoms(formula.inner, vetor)) # adicionar o resultado da chamada da função atoms no vetor

    elif isinstance(formula, Atom):
        return formula # retornar a formula

    for elemento in vetor: # guardar as strings das subformulas no vetorF
        if isinstance(elemento, Atom): # pegar somente as formulas que sao atomicas
            vetorS.append(f'{elemento}')

    return list(dict.fromkeys(vetorS)) # retornar o vetorS sem repetições

# NÚMERO DE ATÔMICAS EM UMA FÓRMULA
def number_of_atoms(formula):

    for index, formula in enumerate(atoms(formula, vetor = [])): # Percorrer o vetor da função atoms
        contador = index + 1 # Contador para contar o número de atomicas

    return contador # Retornar o contador

# CONTAR O NÚMERO DE CONECTIVOS DE UMA FÓRMULA
def number_of_connectives(formula):
    contador = 0 # Contador dos conectivos

    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or): # Se a formula possuir um conectivo binário
        contador += 1 # Somar 1 ao contador devido ao conectivo binário
        contador += number_of_connectives(formula.left) + number_of_connectives(formula.right) # somar as chamadas da função number_of_connectives da direita e esquerda e atribuir ao contador

    elif isinstance(formula, Not): # Se a formula for uma negação
        contador += 1 # Somar 1 ao contador devido ao conectivo de negação
        contador += number_of_connectives(formula.inner) # chamar a função number_of_connectives da formula dentro da negação e atribuir ao contador

    elif isinstance(formula, Atom): # Se a formula for uma atômica
        contador = contador # Contador deve ser igual ao contador, pois uma atomica nao possui conectivo

    return contador # Retornar o valor final do contador

# VERIFICAR SE A FORMULA É UM LITERAL
def is_literal(formula):
    
    if isinstance(formula, Atom) or (isinstance(formula, Not) and isinstance(formula.inner, Atom)): # Se a formula for uma atomica ou se a formula for uma negação de uma atomica
        return True
    
    else: # Se não for nenhuma das condições acima
        return False

def substitution(formula, old_subformula, new_subformula):
    """Returns a new formula obtained by replacing all occurrences
    of old_subformula in the input formula by new_subformula."""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========

# VERIFICAR SE A FORMULA É UMA CLÁUSULA
def is_clause(formula):
    
    if isinstance(formula, Or) and (is_literal(formula.left) and is_literal(formula.right)): # Se existir uma disjunção entre literais
        return True
        
    else: # Se não satisfazer a exigencia acima
        return False

# VERIFICAR SE A FORMULA ESTA NA NNF
def is_negation_normal_form(formula):
    
    if isinstance(formula, And) or isinstance(formula, Or):
        if is_negation_normal_form(formula.left) and is_negation_normal_form(formula.right):
            return True
        
    elif isinstance(formula, Not):
        if isinstance(formula.inner, Atom):
            return True
        
        else:
            return False
        
    elif isinstance(formula, Implies):
        return False
    
    else:
        return True
    

# VERIFICAR SE A FORMULA ESTA EM CNF
def is_cnf(formula):
    
    if isinstance(formula, And) and (is_clause(formula.left) and is_clause(formula.right)): # Se existir uma conjunção entre cláusulas
        return True
    
    else: # Se não satisfazer a exigencia acima
        return False

# VERIFICAR SE A FORMULA É UM TERMO
def is_term(formula):
    
    if isinstance(formula, And) and (is_literal(formula.left) and is_literal(formula.right)): # Se existir uma conjunção entre literais
        return True
        
    else: # Se não satisfazer a exigencia acima
        return False


def is_dnf(formula):
    """Returns True if formula is in disjunctive normal form.
    Returns False, otherwise."""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========


def is_decomposable_negation_normal_form(formula):
    """Returns True if formula is in decomposable negation normal form.
    Returns False, otherwise."""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========