from formula import *


def length(formula):

    if isinstance(formula, Atom):
        return 1

    elif isinstance(formula, Not):
        return length(formula.inner) + 1

    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        return length(formula.left) + length(formula.right) + 1


def subformulas(formula, vetor = []):
    
    vetorS = []

    if isinstance(formula, Atom):
        vetor.append(formula)
        return formula
    
    elif isinstance(formula, Not):
        vetor.append(formula)
        subformulas(formula.inner, vetor)
        
    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        vetor.append(formula)
        subformulas(formula.left, vetor)
        subformulas(formula.right, vetor)
        
    for elemento in vetor:
            vetorS.append(f'{elemento}')

    return list(dict.fromkeys(vetorS))


def atoms(formula, vetor = []):
    
    vetorS = []
    
    if isinstance(formula, Atom):
        return formula
    
    elif isinstance(formula, Not):
        vetor.append(atoms(formula.inner, vetor))

    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        vetor.append(atoms(formula.right, vetor))
        vetor.append(atoms(formula.left, vetor))

    for elemento in vetor:
        if isinstance(elemento, Atom):
            vetorS.append(f'{elemento}')

    return list(dict.fromkeys(vetorS))


def number_of_atoms(formula):
    
    contador = 0

    if isinstance(formula, Atom):
        contador += 1
        
    elif isinstance(formula, Not):
        contador += number_of_atoms(formula.inner)
        
    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        contador += number_of_atoms(formula.left) + number_of_atoms(formula.right)

    return contador


def number_of_connectives(formula):
    
    contador = 0
    
    if isinstance(formula, Atom):
        contador = contador
    
    elif isinstance(formula, Not):
        contador += 1
        contador += number_of_connectives(formula.inner)

    if isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        contador += 1
        contador += number_of_connectives(formula.left) + number_of_connectives(formula.right)

    return contador


def is_literal(formula):
    
    if isinstance(formula, Atom) or isinstance(formula, Not) and isinstance(formula.inner, Atom):
        return True
    
    return False


def substitution(formula, old_subformula, new_subformula):
    
    if isinstance(formula, Atom):
        if formula == old_subformula:
            formula = new_subformula
        
    elif isinstance(formula, Not):
        if formula == old_subformula:
            formula = new_subformula
        
        else: 
            substitution(formula.inner, old_subformula, new_subformula)
        
    elif isinstance(formula, Implies) or isinstance(formula, And) or isinstance(formula, Or):
        if formula == old_subformula:
            formula = new_subformula
        
        else:
            formula.left = substitution(formula.left, old_subformula, new_subformula)
            formula.right = substitution(formula.right, old_subformula, new_subformula)

    return formula


def is_clause(formula):
    
    if isinstance(formula, Atom):
        return True
    
    elif isinstance(formula, Not):
        if is_literal(formula.inner):
            return True
        
        else:
            return False
        
    elif isinstance(formula, Implies) or isinstance(formula, And):
        return False
    
    elif isinstance(formula, Or):
        if is_clause(formula.left) and is_clause(formula.right):
            return True
        
        else:
            return False
  
  
def is_negation_normal_form(formula):
    
    if isinstance(formula, Atom):
        return True
    
    elif isinstance(formula, Not):
        if isinstance(formula.inner, Atom):
            return True
        
        else:
            return False
        
    elif isinstance(formula, And) or isinstance(formula, Or):
        if is_negation_normal_form(formula.left) and is_negation_normal_form(formula.right):
            return True
        
        else:
            return False
        
    elif isinstance(formula, Implies):
        return False


def is_cnf(formula):
    
    if isinstance(formula, Atom):
        return True
    
    if isinstance(formula, Not):
        if is_literal(formula.inner):
            return True
        
        else:
            return False
        
    elif isinstance(formula, Or):
        if is_clause(formula.left) and is_clause(formula.right):
            return True
        
        else:
            return False
        
    elif isinstance(formula, And):
        if (is_clause(formula.left) or is_cnf(formula.left)) and (is_clause(formula.right) or is_cnf(formula.right)):
            return True
        
        else:
            return False
        
    elif isinstance(formula, Implies):
        return False


def is_term(formula):
    termo = True

    if isinstance(formula, And):

        if isinstance(formula.right and formula.left, Atom):
            termo = termo and is_literal(formula.right) and is_literal(formula.left)
            return termo

        if isinstance(formula.right or formula.left, Not):
            termo = termo and is_literal(formula.left)  and is_literal(formula.right)
            return termo

        if isinstance(formula.left and formula.right, And):
            is_term(formula.right)
            is_term(formula.left)
        
        elif isinstance(formula.left or formula.right, And):
            if isinstance(formula.left, And):
                is_term(formula.left)
                termo = termo and is_literal(formula.right)
            else:
                is_term(formula.right)
                termo = termo and is_literal(formula.left)

        return termo
        
    else:
        termo = False
        return termo


def is_dnf(formula):
    termo = True
    
    if isinstance(formula, Or):
        
        if isinstance(formula.right or formula.left, Not):
            termo = termo and is_term(formula.left)  and is_term(formula.right)
            return termo

        if isinstance(formula.left and formula.right, Or):
            is_dnf(formula.right)
            is_dnf(formula.left)

        elif isinstance(formula.left or formula.right, Or):
            if isinstance(formula.left, Or):
                is_dnf(formula.left)
                termo = termo and is_term(formula.right)
            else:
                is_dnf(formula.right)
                termo = termo and is_term(formula.left)
        else:
            termo = termo and is_term(formula.right) and is_term(formula.left)
            return termo

        return termo
    
    else:
        termo = False
        return termo


def is_decomposable_negation_normal_form(formula):

    pass