from functions import *

def transformarEmDisjuncao(ListaDeFormulas):
    
    primeiraFormula = ListaDeFormulas[0]
    del ListaDeFormulas[0]

    for formula in ListaDeFormulas:
        primeiraFormula = Or(primeiraFormula, formula)

    return primeiraFormula


def transformarEmConjuncao(ListaDeFormulas):
    
    primeiraFormula = ListaDeFormulas[0]
    del ListaDeFormulas[0]

    for formula in ListaDeFormulas:
        primeiraFormula = And(primeiraFormula, formula)

    return primeiraFormula


def filtrarDadosPacientes(grid, filtro):
    
    listaDadosPacientesFiltrados = []
    contador = 0
    
    for linha in grid: 
        if linha[-1] == filtro:
            linha.pop()
            listaDadosPacientesFiltrados.append([linha, contador])

        contador += 1
    
    return listaDadosPacientesFiltrados


def inverterValores(atomicaSplitada):
    
    atomicaSplitada[0] = atomicaSplitada[0].replace('<=', '>')
    return atomicaSplitada


def organizarResultados(resultado):

    atomicasIniciadasEmX = []
    atomicasIniciadasEmC = []
    
    for atomica in resultado:
        atomicaSplitada = atomica.split('_')
            
        if atomicaSplitada.pop(0) == 'X':
            atomicasIniciadasEmX.append(atomicaSplitada) if atomicaSplitada.pop() == 'p' else atomicasIniciadasEmX.append(inverterValores(atomicaSplitada))
   
        else:
            atomicasIniciadasEmC.append(atomicaSplitada)
                
    return atomicasIniciadasEmX, atomicasIniciadasEmC


def gerarRegras(dadosAtomicasIniciadasEmX, numeroDeRegras):

    conjuntoDeRegras = []
    
    for regra in range(numeroDeRegras):
        listaAuxiliar = []
        for atributoDaRegra in dadosAtomicasIniciadasEmX:
            listaAuxiliar.append(atributoDaRegra[0]) if atributoDaRegra[-1] == str(regra + 1) else listaAuxiliar == listaAuxiliar
                
        conjuntoDeRegras.append(listaAuxiliar)
            
    for index, regra in enumerate(conjuntoDeRegras):
        print(f'REGRA {index + 1}: {str(regra)[1:-1]} => P')

    print('')
    return conjuntoDeRegras


def laudarPacientes(dadosAtomicasIniciadasEmC):
    
    listaDeRegras = []

    for dado in dadosAtomicasIniciadasEmC:
        listaDeRegras.append(dado[0])
    
    for regra in sorted(set(listaDeRegras)):
        listaAuxiliar = []
        for dado in dadosAtomicasIniciadasEmC:
            if dado[0] == regra:
                listaAuxiliar.append(dado[1])
                
        print(f'REGRA {regra} SE APLICA AO(S) PACIENTE(S): {str(sorted(listaAuxiliar))[1:-1]}')