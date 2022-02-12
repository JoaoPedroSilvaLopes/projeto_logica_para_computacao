from copy import *
from formula import *
from functions import atoms


def satisfiability_brute_force(formula):
    
    listaAtomicas = sorted(atoms(formula))
    
    interpretacao = []
    return sat(formula, listaAtomicas, interpretacao)


def sat(formula, listaAtomicas, interpretacao):
    
    copiaListaAtomicas = listaAtomicas.copy()
    
    if copiaListaAtomicas == []:
        return pegarAtomicasVerdadeiras(interpretacao) if truth_value(formula, interpretacao) else False
    
    atomicaRemovida = copiaListaAtomicas.pop()
    interpretacaoComTrue = interpretacao + [[atomicaRemovida, True]]
    
    interpretacaoComFalse = interpretacao + [[atomicaRemovida, False]]
    
    resultado = sat(formula, copiaListaAtomicas, interpretacaoComTrue)
    return resultado if resultado != False else sat(formula, copiaListaAtomicas, interpretacaoComFalse)


def simplificarInterpretacao(listaAtomicas, interpretacao):
    
    for i in interpretacao:
        for j in listaAtomicas:
            if Not(i[0]) == j:
                interpretacao.append([j, not i[1]])
                del(listaAtomicas[j])
    
    return listaAtomicas, interpretacao


def truth_value(formula, interpretacao):
    
    if isinstance(formula, Atom):
        for valoracao in interpretacao:
            if str(formula) == valoracao[0]:
                return valoracao[1]

    elif isinstance(formula, Not):
        return not truth_value(formula.inner, interpretacao)
        
    elif isinstance(formula, And):
        return True if truth_value(formula.left, interpretacao) and truth_value(formula.right, interpretacao) else False
  
    else:
        return True if truth_value(formula.left, interpretacao) or truth_value(formula.right, interpretacao) else False


def pegarAtomicasVerdadeiras(interpretacao):
    
    listaDeAtomicasVerdadeiras = []
    
    for valoracao in interpretacao:
        listaDeAtomicasVerdadeiras.append(valoracao[0]) if valoracao[1] == True and valoracao[0].split('_')[-1] != 's' else listaDeAtomicasVerdadeiras
        
    return listaDeAtomicasVerdadeiras

