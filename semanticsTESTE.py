from copy import deepcopy
from formula import *
from collections import Counter


def DPLL(formulaCNF):

    return DPLLCheck(formulaCNF, interpretacao = [])

    
def DPLLCheck(formulaCNF, interpretacao):
    
    copiaCNF = deepcopy(formulaCNF)
    copiaCNF, interpretacao = propagacaoDeUnidade(copiaCNF, interpretacao)
    
    if copiaCNF == []:
        #print(sorted(set(interpretacao)))
        return interpretacao #pegarAtomicasVerdadeiras(interpretacao)
    
    elif [] in copiaCNF:
        return False
    
    atomica = pegarAtomica(formulaCNF)
    
    S1 = copiaCNF + [[atomica]]
    S2 = copiaCNF + [[atomica * -1]]
    
    resultado = DPLLCheck(S1, interpretacao)
    
    if resultado != False:
        return resultado
    
    return DPLLCheck(S2, interpretacao)
    
      
def propagacaoDeUnidade(formulaCNF, interpretacao):
    
    #print(formulaCNF)
    
    while existeClausulaUnitaria(formulaCNF):

        literal = unidadeLiteral(formulaCNF)
        interpretacao = interpretacao + [literal]
        
        formulaCNF = removerClausulasComLiteral(formulaCNF, literal)
        formulaCNF = removerComplementoDoLiteral(formulaCNF, literal)
        
    return formulaCNF, interpretacao


def pegarAtomica(frequencia):
    
    frequencias = Counter(frequencia).most_common()
    maisFrequente = frequencias.pop(0)
    atomica = maisFrequente[0]
    frequencia = list(filter((atomica).__ne__, frequencia))
    frequencia = list(filter((atomica * -1).__ne__, frequencia))
    
    return atomica, frequencia


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


"""def pegarAtomicasVerdadeiras(interpretacao):
    
    listaDeAtomicasVerdadeiras = []
    
    for valoracaoLiteral in interpretacao:
        listaDeAtomicasVerdadeiras.append(f'{valoracaoLiteral}') if not isinstance(valoracaoLiteral, Not) and str(valoracaoLiteral).split('_')[-1][0] != 's' else listaDeAtomicasVerdadeiras
        
    return listaDeAtomicasVerdadeiras"""


X1 = Atom('p')
X2 = Atom('q')
X3 = Atom('r')
X4 = Atom('s')
X5 = Atom('t')
X6 = Atom('c')

teste = [[X1, X3], [Not(X3), X6, X5], [X3, X5, X2], [Not(X1), X3, X6], [X4, X5], [Not(X1)]]
teste1 = [[X1, X2, X3], [X2, Not(X3)], [Not(X3)]]
teste2 = [[Not(X1)], [X1, X2], [X1, X3], [Not(X2), Not(X3), Not(X4), Not(X5)], [Not(X1), X4], [Not(X4), Not(X5)]]

#DPLL(teste)