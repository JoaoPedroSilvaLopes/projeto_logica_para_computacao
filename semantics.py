"""The goal in this module is to define functions associated with the semantics of formulas in propositional logic. """


from formula import *
from functions import atoms

   
def truth_value(formula, interpretation):
    
    if isinstance(formula, Atom): # Verificar se a fórmula é uma atomica
        for formulaArray in interpretation: # Percorrer o array de interpretações parciais
            if f'{formula}' == f'{formulaArray[0]}': # Se tal atomica estiver na interpretação
                return formulaArray[1] # Retornar a sua interpretação parcial

    elif isinstance(formula, Not):
        if truth_value(formula.inner, interpretation) == True or truth_value(formula.inner, interpretation) == False:
            return not truth_value(formula.inner, interpretation)
        
    elif isinstance(formula, And):
        if truth_value(formula.left, interpretation) == False or truth_value(formula.right, interpretation) == False:
            return False
        
        else:
            return True
  
    elif isinstance(formula, Or):
        if truth_value(formula.left, interpretation) == True or truth_value(formula.right, interpretation) == True:
            return True
        
        else:
            return False
 
    elif isinstance(formula, Implies): # Verificar se a fórmula possui o operador binário Implies
        if truth_value(formula.left, interpretation) == False or truth_value(formula.right, interpretation) == True:
            return True
        
        else:
            return False


def is_logical_consequence(premises, conclusion):  # function TT-Entails? in the book AIMA.
    """Returns True if the conclusion is a logical consequence of the set of premises. Otherwise, it returns False."""
    pass
    # ======== YOUR CODE HERE ========


def is_logical_equivalence(formula1, formula2):
    """Checks whether formula1 and formula2 are logically equivalent."""
    pass
    # ======== YOUR CODE HERE ========


def is_valid(formula):
    """Returns True if formula is a logically valid (tautology). Otherwise, it returns False"""
    pass
    # ======== YOUR CODE HERE ========


def satisfiability_brute_force(formula):
    """Verifica se a fórmula é satisfatória.
    Em outras palavras, se a fórmula de entrada for satisfatória, ela retornará uma interpretação que atribui verdadeiro à fórmula.
    Caso contrário, retorna False. """
    pass
    # ======== YOUR CODE HERE ========


# VERIFICAR A SATISFABILIDADE
def satisfiability_checking(formula):
    # Lista das atomicas da formula
    list_atoms = atoms(formula)
    
    # Interpretação
    # DICA DE MELHORIA, QUEBRAR AS FORMULA E TENTAR DEDUZIR AS INTERPRETAÇÕES
    interpretation = {}
    
    # Retorno da função
    # REMOVER AS ATOMICAS QUE JA RECEBERAM UMA INTERPRETAÇÃO PARCIAL DA LIST_ATOMS
    return sat(formula, list_atoms, interpretation)

# VERIFICAR AS POSSIBILIDADES DE SATISFABILIDADE 
def sat(formula, list_atoms, interpretation):
    # Verificar se list_atoms é um conjunto vazio
    if list_atoms == {}:
        # Caso o valor da formula seja verdadeiro
        if truth_value(formula, interpretation):       
            # Retornar a interpretação
            return interpretation
        
        # Caso o valor seja falso
        else:
            # Retornar False
            return False
    
    # Remover elemento do conjunto e atribui-lo a variavel atom
    atom = list_atoms.pop()
    
    # Cópia de atom
    atom2 = atom
    
    # Adicionar as duas possíveis interpretações: True ou False
    interpretation1 = {interpretation}.union(atom, True)
    interpretation2 = {interpretation}.union(atom, False)
    
    # Resultado da interpretação
    result = sat(formula, atom, interpretation1)
    
    # Se o resultado for True
    if result != False:
        # Retornar o resultado
        return result
    
    # Chamada recursiva da função sat interpretação 2 caso a interpretação 1 seja falsa
    return sat(formula, atom2, interpretation2)
    
# VERIFICAR A VALIDADE
def validity_checking(formula):
    
    if satisfiability_checking(Not(formula)) == False: # Se a fórmula não for safisfatível, logo a fórmula é válida
        return True # A fórmula é válida
    
    else: # Caso seja True
        return False # A fórmula não é válida

#---------------------------------------------------------------
# TESTES
# Função para converter todas os operadores das forulas em And utilizando os conceitos da equivalencia lógica

def conversor(formula):
    
    if isinstance(formula, Atom):
        return formula
    
    elif isinstance(formula, Not):
        if isinstance(formula.inner, Atom):
            return formula
        
        else:
            formula = conversor(formula.inner)
            return formula
    
    elif isinstance(formula, And):
        formula = And(conversor(formula.left), conversor(formula.right))
    
    elif isinstance(formula, Or):
        formula = Not(And(Not(conversor(formula.left)), Not(conversor(formula.right))))

    elif isinstance(formula, Implies):
        formulaParcial = Or(Not(conversor(formula.left)), conversor(formula.right))
        formula = conversor(formulaParcial)
    
    return formula

def simplificador_de_not(formula):
    
    if isinstance(formula, Atom):
        return formula
    
    elif isinstance(formula, Not):
        if isinstance(formula.inner, Not):
            formula = simplificador_de_not(formula.inner.inner)
            return formula
        
        else:
            formula = Not(simplificador_de_not(formula.inner))
            return formula
    
    elif isinstance(formula, And) or isinstance(formula, Or) or isinstance(formula, Implies):
        formula.left = simplificador_de_not(formula.left)
        formula.right = simplificador_de_not(formula.right)
        
    return formula

"""formula1 = Implies(Atom('q'), Atom('r'))
formula2 = Implies(Not(Atom('q')), Atom('r'))
formula3 = Implies(Atom('q'), Not(Atom('r')))
formula4 = Implies(Not(Atom('q')), Not(Atom('r')))

formula5 = Or(Atom('p'), Implies(Atom('q'), Atom('r')))

print(f'A fórmula {formula5} converteu para: {conversor(formula5)}')
formula6 = conversor(formula5)
print(f'A fórmula {formula6} foi simplificada para: {simplificador_de_not(formula6)}')"""
    
    