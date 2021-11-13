# MAIN PARA TESTE DE FUNÇÕES

from formula import *
from functions import *

# FORMULAS DE TESTES

formula1 = Atom('p') # p
formula2 = Atom('q') # q
formula3 = And(formula1, formula2) # (p /\ q)
formula4 = And(formula1, Atom('s')) # (p /\ s)
formula5 = Not(formula4) # (¬(p /\ s))
formula6 = Or(formula5, formula2) # ((¬(p /\ s)) v q)
formula7 = Implies(formula5, And(formula2, Atom('r'))) # ((¬(p /\ s)) -> (q /\ r))
formula8 = Implies(formula5, And(formula2, formula5)) # ((¬(p /\ s)) -> (q /\ (¬(p /\ s))))
formula9 = Or(And(And(Atom('P'), Not(Atom('R'))), And(Not(Atom('Q')), Atom('R'))), Atom('S')) # (p ∧ (¬q ∧ r) ∧ ¬r) ∨ s
formula10 = Or(And(And(Atom('P'), Not(Atom('R'))), Not(And(Atom('Q'), Atom('R')))), Atom('S')) # (p ∧ ¬(q ∧ r) ∧ ¬r) ∨ s

# TESTES DE FUNÇÕES

"""formula11 = Or(formula1, Or(Not(formula2), Atom('r')))            # (p ∨ ¬q ∨ r)
formula12 = Not(formula11) # ¬(p ∨ ¬q ∨ r)
formula13 = Or(Not(Or(formula1, Not(formula2))), Atom('r')) # (¬(p ∨ ¬q) ∨ r)
formula14 = Or(formula1, formula2)
formula15 = Or(formula11, formula14)"""

'''formula11 = Or(Atom('r'), Atom('s')) # (r ∨ s)
formula12 = Or(Not(Atom('S')), formula1) # (¬s ∨ p)
formula13 = Or(Not(formula2), formula11) # (¬q ∨ r ∨ s)
formula14 = Or(Not(formula1), formula12) # (¬p ∨ ¬s ∨ p)
formula15 = And(formula13, formula14) # ((¬q ∨ r ∨ s) ∧ (¬p ∨ ¬s ∨ p))
formula16 = And(formula1, formula15)  # p ∧ (¬q ∨ r ∨ s) ∧ (¬p ∨ ¬s ∨ p)

formula17 = And(Not(formula1), Atom('r')) # (¬p ∧ r)
formula18 = Or(Not(formula2), formula17) # (¬q ∨ (¬p ∧ r))
formula19 = And(formula1, formula18) # p ∧ (¬q ∨ (¬p ∧ r))
'''

formula20 = Not(And(formula2, Atom('r')))
formula21 = And(formula20, Not(Atom('r')))
formula22 = And(formula1, formula21)
formula23 = Or(formula22, Atom('s'))

print(formula23)
print(f'teste: {is_negation_normal_form(formula23)}')

"""print(atoms(formula8))
print(number_of_atoms(formula8))
print(f'Numero de conectivos {formula8}: {number_of_connectives(formula8)}')
#print(f'Número de atomicas da formula {formula8}: {number_of_atoms(formula8)}')"""

"""# TESTE SUSBSTITUIÇÃO
formula11 = Implies(And(Atom('p'),Not(Atom('q'))), Atom('r'))
formula12 = Not(formula2)
formula13 = Or(Atom('r'), Atom('t'))

print(f'formula {formula1} foi substituida para: {substitution(formula1, formula1, formula2)}')"""

