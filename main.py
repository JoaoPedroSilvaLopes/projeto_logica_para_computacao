# MAIN PARA TESTE DE FUNÇÕES

from formula import *
from functions import *

formula1 = Atom('p')  # p
formula2 = Atom('q')  # q
formula3 = And(formula1, formula2)  # (p /\ q)
formula4 = And(Atom('p'), Atom('s'))  # (p /\ s)
formula5 = Not(And(Atom('p'), Atom('s')))  # (¬(p /\ s))
formula6 = Or(Not(And(Atom('p'), Atom('s'))), Atom('q'))  # ((¬(p /\ s)) v q)
formula7 = Implies(Not(And(Atom('p'), Atom('s'))), And(Atom('q'), Atom('r')))  # ((¬(p /\ s)) -> (q /\ r))
formula8 = Implies(Not(And(Atom('p'), Atom('s'))), And(Atom('q'), Not(And(Atom('p'), Atom('s')))))

formula9 = Or(And(And(Atom('P'), Not(Atom('R'))), And(Not(Atom('Q')), Atom('R'))), Atom('S')) # (p ∧ (¬q ∧ r) ∧ ¬r) ∨ s
formula10 = Or(And(And(Atom('P'), Not(Atom('R'))), Not(And(Atom('Q'), Atom('R')))), Atom('S')) # (p ∧ ¬(q ∧ r) ∧ ¬r) ∨ s

print(formula9)
print(is_negation_normal_form(formula9))

print(formula10)
print(is_negation_normal_form(formula10))


"""print()
# teste função atoms
print(f'Os atomos da fórmula {formula8} são: {atoms(formula8)}')

# teste função length
print(f'O tamanho da fórmula {formula8} é: {length(formula8)}')

# teste função subformulas
print(f'As subfórmulas da fórmula {formula8} são: {subformulas(formula8)}')

# teste função number_of_atoms
print(f'O número de atômicas na fórmula {formula8} são: {number_of_atoms(formula8)}')

# teste função number_of_connectives
print(f'O número de conectivos da fórmula {formula8} são: {number_of_connectives(formula8)}')

print()

# teste da função is_literal
print(f'A verificação se a formula {formula1} é um literal é: {is_literal(formula1)}')
print(f'A verificação se a formula {formula1} é um literal é: {is_literal(formula2)}')
print(f'A verificação se a formula {formula1} é um literal é: {is_literal(formula8)}')
#is_literal(formula2)
#is_literal(formulaTeste)

print()

# teste da função is_clause
print(f'A verificação se a formula {formula3} é uma cláusula é: {is_clause(formula3)}')
print(f'A verificação se a formula {formula4} é uma cláusula é: {is_clause(formula4)}')
is_clause(formula3)
is_clause(formula4)

print()

print(f'A verificação se a formula {And(formula3, formula5)} esta em CNF é: {is_cnf(And(formula3, formula5))}')
print(f'A verificação se a formula {And(formula3, formula4)} esta em CNF é: {is_cnf(And(formula3, formula4))}')"""

