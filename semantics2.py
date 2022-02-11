from copy import deepcopy
from formula import *


def DPLL(formulaCNF):

    return DPLLCheck(formulaCNF, interpretacao = [])

    
def DPLLCheck(formulaCNF, interpretacao):
    
    copiaCNF = deepcopy(formulaCNF)
    copiaCNF, interpretacao = propagacaoDeUnidade(copiaCNF, interpretacao)
    
    if copiaCNF == []:
        return pegarAtomicasVerdadeiras(interpretacao)
    
    elif [] in copiaCNF:
        return False
    
    atomica = pegarAtomica(copiaCNF)
    
    S1 = copiaCNF + [[atomica]]
    S2 = copiaCNF + [[Not(atomica)]]
    
    resultado = DPLLCheck(S1, interpretacao)
    
    if resultado != False:
        return resultado
    
    return DPLLCheck(S2, interpretacao)
    
      
def propagacaoDeUnidade(formulaCNF, interpretacao):
    
    while existeClausulaUnitaria(formulaCNF):

        literal = unidadeLiteral(formulaCNF)
        interpretacao = interpretacao + [literal]
        
        formulaCNF = removerClausulasComLiteral(formulaCNF, literal)
        formulaCNF = removerComplementoDoLiteral(formulaCNF, literal)
        
    return formulaCNF, interpretacao


def pegarAtomica(formulaCNF):

    listaAtomicas = []
            
    for clausula in formulaCNF:
        for literal in clausula:
            if isinstance(literal, Atom):
                listaAtomicas.append(literal)
                
    if list(set(listaAtomicas)) != []:
        return listaAtomicas.pop()
    
    return


def existeClausulaUnitaria(formulaCNF):
    
    for clausula in formulaCNF:
        if len(clausula) == 1:
            return True
    
    return False


def unidadeLiteral(formulaCNF):
    
    for clausula in formulaCNF:
        if len(clausula) == 1:
            for literal in clausula:
                return literal
        
    return None


def removerClausulasComLiteral(formulaCNF, literal):
    
    teste = []
    listaComLiteral = []
    
    for clausula in formulaCNF:
        if literal in clausula:
            listaComLiteral.append(clausula)
    
    for clausula in formulaCNF:
        if clausula not in listaComLiteral:
            teste.append(clausula)
            
    return teste


def removerComplementoDoLiteral(formulaCNF, literal):

    if isinstance(literal, Atom):
        for clausula in formulaCNF:
            if Not(literal) in clausula:
                clausula = clausula.remove(Not(literal))
        
    elif isinstance(literal, Not):
        for clausula in formulaCNF:
            if literal.inner in clausula:
                clausula = clausula.remove(literal.inner)
                    
    return formulaCNF


def pegarAtomicasVerdadeiras(interpretacao):
    
    listaDeAtomicasVerdadeiras = []
    
    for valoracaoLiteral in interpretacao:
        listaDeAtomicasVerdadeiras.append(f'{valoracaoLiteral}') if not isinstance(valoracaoLiteral, Not) and str(valoracaoLiteral).split('_')[-1][0] != 's' else listaDeAtomicasVerdadeiras
        
    return listaDeAtomicasVerdadeiras

