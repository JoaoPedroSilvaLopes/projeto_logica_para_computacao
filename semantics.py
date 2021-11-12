"""The goal in this module is to define functions associated with the semantics of formulas in propositional logic. """


from formula import *
from functions import atoms


def truth_value(formula, interpretation):
    """Determines the truth value of a formula in an interpretation (valuation).
    An interpretation may be defined as dictionary. For example, {'p': True, 'q': False}.
    """
    pass
    # ======== YOUR CODE HERE ========


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
    """Checks whether formula is satisfiable.
    In other words, if the input formula is satisfiable, it returns an interpretation that assigns true to the formula.
    Otherwise, it returns False."""
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
    
    # Se a fórmula não for safisfatível, logo a fórmula é válida
    if satisfiability_checking(Not(formula)) == False:
        # A fórmula é válida
        return True
    
    # Caso seja True
    else:
        # A fórmula não é válida
        return False


#---------------------------------------------------------------

# Função para converter todas os operadores das formulas em And utilizando os conceitos da equivalencia lógica

def converterOu(formula):  
    formula = Not(And(Not(formula.left), Not(formula.right)))
    formulaNegada = formula.inner   
    
    if isinstance(formulaNegada.left.inner, Not) and isinstance(formulaNegada.right.inner, Not):
        formula = Not(And(formulaNegada.left.inner.inner, formulaNegada.right.inner.inner))
        return formula
        
    elif isinstance(formulaNegada.left.inner, Not):
        formula = Not(And(formulaNegada.left.inner.inner, Not(formulaNegada.right.inner)))
        return formula
    
    elif isinstance(formulaNegada.right.inner, Not):
        formula = Not(And(Not(formulaNegada.left.inner), formulaNegada.right.inner.inner))
        return formula
    
    else:
        return formula
 
       
def converterImplica(formula):
    formula = Or(Not(formula.left), formula.right)
    return converterOu(formula)

"""def converterNot(formula: Not):
    if isinstance(formula.inner, Not):
        formulaNegada = formula.inner
        formula = formulaNegada.inner
        #print(formula)
    
        if isinstance(formula, And):
            print(formula.left)
            
        formulaNegada = formula.inner
        formula = formulaNegada.inner
            
        if isinstance(formula, Atom):
            return formula
            
        if isinstance(formula, And):
            print(formula)
            return formula
            
        elif isinstance(formula, And):
            converterFormula(formula.left)
            converterFormula(formula.right)
                
        elif isinstance(formula, Or):
            converterOu(formula)
                
        elif isinstance(formula, Implies):
            converterImplica(formula)
                
        else:
            if isinstance(formula.inner, And):
                converterFormula(formula.inner.left)
                converterFormula(formula.inner.right)
                
            elif isinstance(formula.inner, Or):
                converterOu(formula.inner)
                
            elif isinstance(formula.inner, Implies):
                converterImplica(formula.inner)"""

def converterFormula(formula):
    
    if isinstance(formula, Atom):
        return formula
    
    elif isinstance(formula, Not):
        print(formula)
        
        if isinstance(formula.inner, And):
            
            converterFormula(formula)
            print(Not(converterFormula(formula)))
            
        elif isinstance(formula.inner, Implies):
            print(formula.inner)
        
    # E       
    elif isinstance(formula, And):
        f1 = converterFormula(formula.left)
        f2 = converterFormula(formula.right)
        formulaE = And(f1, f2)
        print(formulaE)
        
        #return formulaE
            
    # OU       
    elif isinstance(formula, Or):
        print(formula)
        formulaO = converterOu(formula)
        return formulaO
            
    # IMPLICA        
    elif isinstance(formula, Implies):
        print(formula)
        formulaI = converterImplica(formula)
        print(formulaI)
        return formulaI
                


             
"""formula1 = Or(Atom('p'), Implies(Atom('q'), Atom('r')))  
formula2 = Or(Not(Atom('p')), Implies(Atom('q'), Atom('r')))  
formula3 = Or(Atom('p'), Not(Implies(Atom('q'), Atom('r'))))
formula4 = Or(Not(Atom('p')), Not(Implies(Atom('q'), Atom('r'))))

formula5 = And(Atom('p'), Implies(Atom('q'), Atom('r')))""" 

formula1 = Implies(Atom('q'), Atom('r'))
formula2 = Implies(Not(Atom('q')), Atom('r'))
formula3 = Implies(Atom('q'), Not(Atom('r')))
formula4 = Implies(Not(Atom('q')), Not(Atom('r')))

converterFormula(formula1)
    
    