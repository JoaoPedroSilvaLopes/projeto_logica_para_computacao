"""The goal in this module is to define functions that take a formula as input and
do some computation on its syntactic structure. """


from formula import *

# MOSTRAR O TAMANHO DE UMA FÓRMULA
def length(formula):

    if isinstance(formula, Atom): # Se a formula for uma atômica
        return 1

    elif isinstance(formula, Not): # Se a formula for uma negação
        return length(formula.inner) + 1

    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or): # Se a formula possuir um conectivo binário
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
    
    if isinstance(formula, Atom): # Se a formula for uma atômica
        return formula # retornar a formula
    
    elif isinstance(formula, Not): # Se a formula for uma negação
        vetor.append(atoms(formula.inner, vetor)) # adicionar o resultado da chamada da função atoms no vetor

    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or): # Se a formula possuir um conectivo binário
        vetor.append(atoms(formula.right, vetor)) # adicionar o resultado da chamada da função atoms no vetor
        vetor.append(atoms(formula.left, vetor)) # adicionar o resultado da chamada da função atoms no vetor

    for elemento in vetor: # guardar as strings das subformulas no vetorF
        if isinstance(elemento, Atom): # pegar somente as formulas que sao atomicas
            vetorS.append(f'{elemento}')

    return list(dict.fromkeys(vetorS)) # retornar o vetorS sem repetições


# NÚMERO DE ATÔMICAS EM UMA FÓRMULA
def number_of_atoms(formula):
    
    contador = 0 # contador

    if isinstance(formula, Atom): # Se a formula for uma atômica
        contador += 1 # Adicionar +1 ao contador caso a formula recebida seja uma atomica
        
    elif isinstance(formula, Not): # Se a formula for uma negação
        contador += number_of_atoms(formula.inner) # Chamar a função number_of_atoms para a formula dentro da negação e somar ao contador
        
    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or): # Se a formula possuir um conectivo binário
        contador += number_of_atoms(formula.left) + number_of_atoms(formula.right) # Chamar a função number_of_atoms para as formulas do lado esquerdo e direito soma-las ao contador

    return contador # Retornar o contador


# CONTAR O NÚMERO DE CONECTIVOS DE UMA FÓRMULA
def number_of_connectives(formula):
    
    contador = 0 # Contador dos conectivos
    
    if isinstance(formula, Atom): # Se a formula for uma atômica
        contador = contador # Contador deve ser igual ao contador, pois uma atomica nao possui conectivo
    
    elif isinstance(formula, Not): # Se a formula for uma negação
        contador += 1 # Somar 1 ao contador devido ao conectivo de negação
        contador += number_of_connectives(formula.inner) # chamar a função number_of_connectives da formula dentro da negação e atribuir ao contador

    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or): # Se a formula possuir um conectivo binário
        contador += 1 # Somar 1 ao contador devido ao conectivo binário
        contador += number_of_connectives(formula.left) + number_of_connectives(formula.right) # somar as chamadas da função number_of_connectives da direita e esquerda e atribuir ao contador

    return contador # Retornar o valor final do contador


# VERIFICAR SE A FORMULA É UM LITERAL
def is_literal(formula):
    
    if isinstance(formula, Atom) or (isinstance(formula, Not) and isinstance(formula.inner, Atom)): # Se a formula for uma atomica ou se a formula for uma negação de uma atomica
        return True
    
    else: # Se não for nenhuma das condições acima
        return False


# REALIZAR UMA SUBSTITUIÇÃO NA FORMULA
def substitution(formula, old_subformula, new_subformula):
    
    if isinstance(formula, Atom): # Se a formula for uma atômica
        if formula == old_subformula: # Se a formula for a propria old_formula
            formula = new_subformula # Então a formula sera simplesmente a new_formula
        
    elif isinstance(formula, Not): # Se a formula for uma negação
        if formula == old_subformula: # Se a formula for a propria old_formula
            formula = new_subformula # Então a formula sera simplesmente a new_formula
        
        else: # Se não 
            substitution(formula.inner, old_subformula, new_subformula) # Chamar a função substitution
        
    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or): # Se a formula possuir um conectivo binário
        if formula == old_subformula: # Se a formula for a propria old_formula
            formula = new_subformula # Então a formula sera simplesmente a new_formula
        
        else: # Se não
            formula.left = substitution(formula.left, old_subformula, new_subformula) # Chamar a função substitution da formula do lado esquerdo
            formula.right = substitution(formula.right, old_subformula, new_subformula) # Chamar a função substitution da formula do lado direito

    return formula # retornar a formula


# VERIFICAR SE A FORMULA É UMA CLÁUSULA
def is_clause(formula):
    
    if isinstance(formula, Atom): # Se a formula for uma atômica que é automicaticamente uma cláusula, pois A = A V A
        return True # Retornar True
    
    elif isinstance(formula, Not): # Se a formula for uma negação
        if is_literal(formula.inner): # Se a formula dentro da negação for um literal
            return True # Retornar True
        
        else: # Se não
            return False # Retornar False
        
    elif isinstance(formula, Implies) or isinstance(formula, And): # Se a formula possuir um conectivo binário IMPLIES ou AND
        return False # Retornar falso, pois não é uma disjunção
    
    elif isinstance(formula, Or): # Se a formula possuir um conectivo binário OR
        if is_clause(formula.left) and is_clause(formula.right): # Chamar a função is_clause para as formulas da esquerda e direita para verificar se sao clausulas
            return True # Retornar True
        
        else: # Se não
            return False # Retornar False
  
  
# VERIFICAR SE A FORMULA ESTA NA NNF
def is_negation_normal_form(formula):
    
    if isinstance(formula, Atom): # # Se a formula for uma atomica
        return True # Retornar True
    
    elif isinstance(formula, Not): # Se a formula for uma negação
        if isinstance(formula.inner, Atom): # Se a formula dentro da negação é uma atomica
            return True # Retornar True
        
        else: # Se não
            return False # Retornar False
        
    elif isinstance(formula, And) or isinstance(formula, Or): # Se a formula possuir um conectivo binário AND ou OR
        if is_negation_normal_form(formula.left) and is_negation_normal_form(formula.right): # Se as formulas da esquerda e direita estão na NNF
            return True # Retornar True
        
        else: # Se não
            return False # Retornar False
        
    elif isinstance(formula, Implies): # Se a formula possuir um conectivo binário IMPLIES
        return False # Retornar False


# VERIFICAR SE A FORMULA ESTA EM CNF
def is_cnf(formula):
    
    if isinstance(formula, Atom): # Se a formula for uma atomica que por tabela é uma cláusula entao esta em CNF, pois A = A /\ A = (A V A) /\ (A V A)
        print('é cnf')
        return True # Retornar True
    
    if isinstance(formula, Not): # Se a formula for uma negação
        if is_literal(formula.inner): # Se a formula dentro da negação for um literal
            return True # Retornar True
        
        else: # Se não
            return False # Retornar False
        
    elif isinstance(formula, Or): # Se a formula possuir um conectivo binário OR
        if is_clause(formula.left) and is_clause(formula.right): # Chamar a função is_clause para as formulas da esquerda e direita para verificar se sao clausulas
            return True # Retornar True
        
        else: # Se não
            return False # Retornar False
        
    elif isinstance(formula, And): # Se a formula possuir um conectivo binário AND
        if (is_clause(formula.left) or is_cnf(formula.left)) and (is_clause(formula.right) or is_cnf(formula.right)): # or (is_clause(formula.left) and is_cnf(formula.right)) or (is_cnf(formula.left) and is_clause(formula.right)): # Verificar se as formulas do lado esquerdo são cláusulas ou cnf
            return True # Retornar True
        
        else: # Se não
            return False # Retornar False
        
    elif isinstance(formula, Implies): # Se a formula possuir um conectivo binário IMPLIES
        return False # Retornar False


# VERIFICAR SE A FORMULA É UM TERMO
def is_term(formula):
    termo = True

    if isinstance(formula, And): # verifica se é uma conjunção de literais

        if isinstance(formula.right and formula.left, Atom):# caso sejam atômicas
            termo = termo and is_literal(formula.right) and is_literal(formula.left)# guarda o valor true ou false na variavel termo, só será termo se as duas forem
            return termo# retorna o termo

        if isinstance(formula.right or formula.left, Not):# caso exista uma NOT, já chama a função is_literal
            termo = termo and is_literal(formula.left)  and is_literal(formula.right)# guarda o valor true ou false na variavel termo, só será termo se as duas forem
            return termo# retorna o termo

        if isinstance(formula.left and formula.right, And):# caso exista uma encadeado de AND, nos dois lados da formula
            is_term(formula.right)# chama a função recursivamente
            is_term(formula.left)# chama a função recursivamente
        
        elif isinstance(formula.left or formula.right, And):# caso exista uma encadeado de AND, em um dos lados da formula
            if isinstance(formula.left, And):
                is_term(formula.left)# chama a função recursivamente
                termo = termo and is_literal(formula.right)# guarda o valor de um dos lados em termo
            else:
                is_term(formula.right)# chama a função recursivamente
                termo = termo and is_literal(formula.left)# guarda o valor de um dos lados em termo

        return termo# retorna o termo
        
    else: # Se não satisfazer a exigencia acima
        termo = False# termo recebe o valor false
        return termo# retorna o termo


# VERIFICAR SE A FORMULA ESTÁ NA FORMA NORMAL DISJUNTIVA
def is_dnf(formula):
    termo = True
    
    if isinstance(formula, Or):# verifica se a formula é uma disjunção 
        
        if isinstance(formula.right or formula.left, Not):# caso exista um NOT, chama a função is_termo para verificação
            termo = termo and is_term(formula.left)  and is_term(formula.right)# guarda o valor em termo
            return termo# retorna termo

        if isinstance(formula.left and formula.right, Or):# caso exista um encadeado de OR, nos dois lados
            is_dnf(formula.right)# chama a função recursivamente
            is_dnf(formula.left)# chama a função recursivamente

        elif isinstance(formula.left or formula.right, Or):# caso exista um encadeado de OR, em um dos lados
            if isinstance(formula.left, Or):
                is_dnf(formula.left)# chama a função recursivamente
                termo = termo and is_term(formula.right)# guarda o valor em termo
            else:
                is_dnf(formula.right)# chama a função recursivamente
                termo = termo and is_term(formula.left)# guarda o valor em termo
        else:
            termo = termo and is_term(formula.right) and is_term(formula.left)# se não se encaixar em nenhuma das situações anteriores, a função is_term é chamada
            return termo# retorna termo

        return termo# retorna termo
        
    else: # Se não satisfazer a exigencia acima
        termo = False# termo recebe false
        return termo# retorna termo


def is_decomposable_negation_normal_form(formula):
    """Returns True if formula is in decomposable negation normal form.
    Returns False, otherwise."""
    pass  # ======== REMOVE THIS LINE AND INSERT YOUR CODE HERE ========