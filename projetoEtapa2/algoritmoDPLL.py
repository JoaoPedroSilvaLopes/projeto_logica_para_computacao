from copy import deepcopy
from formula import *

def DPLL(formulaCNF):
    
    return DPLLCheck(formulaCNF, interpretacao = [])


def DPLLCheck(formulaCNF, interpretacao):
    
    copiaCNF = deepcopy(formulaCNF)
    copiaCNF, interpretacao = propagacaoDeUnidade(copiaCNF, interpretacao)
    
    if copiaCNF == []:
        return sorted(interpretacao)
    
    elif [] in copiaCNF:
        return False
    
    atomica = pegarAtomica(copiaCNF)
    
    S1 = copiaCNF + [[atomica]]
    S2 = copiaCNF + [[atomica * -1]]
    
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
            if literal > 0:
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
    
    if literal > 0:
        for clausula in formulaCNF:
            if (literal * -1) in clausula:
                clausula = clausula.remove(literal * -1)
                
    elif literal < 0:
        for clausula in formulaCNF:
            if (literal * -1) in clausula:
                clausula = clausula.remove(literal * -1)
                    
    return formulaCNF