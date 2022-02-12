import csv
import time
from algoritmoDeForcaBruta import *
from funcoesAuxiliaresProjeto import *
from copy import deepcopy


def criarTabelaPacientes(arquivo):
    
    with open(arquivo) as csv_file:
        
        grid = []
        csv_reader = csv.reader(csv_file, delimiter=',')
        
        for linha in csv_reader:
            grid.append(linha)
    
        return grid


def restricao1(grid, numeroDeRegras):
    
    gridCopia = deepcopy(grid)
    gridCopia.pop()
    formulaRestricao1 = []
    
    for atributoPrimeiraLinha in gridCopia:
        for regra in range(numeroDeRegras):
            listaAuxiliar = []
            for posicao in range(3):
                listaDeAtomicas = []
                SignificadosAtomicas = ['p', 'n', 's']
                
                for significado in SignificadosAtomicas:
                    listaDeAtomicas.append(Not(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_' + str(significado))))
                    
                listaDeAtomicas[posicao] = listaDeAtomicas[posicao].inner
                listaAuxiliar.append(transformarEmConjuncao(listaDeAtomicas))
                
            formulaRestricao1.append(transformarEmDisjuncao(listaAuxiliar))
    
    return transformarEmConjuncao(formulaRestricao1)    

  
def restricao2(grid, numeroDeRegras):
    
    gridCopia = deepcopy(grid)
    gridCopia.pop()
    formulaRestricao2 = []
    
    for regra in range(numeroDeRegras):
        listaAuxiliar = []
        for atributosDoGrid in gridCopia:
            listaAuxiliar.append(Not(Atom('X_' + str(atributosDoGrid) + '_' + str(regra + 1) + '_s')))
        
        formulaRestricao2.append(transformarEmDisjuncao(listaAuxiliar))
    
    return transformarEmConjuncao(formulaRestricao2)


def restricao3(grid, primeiraLinha, numeroDeRegras):
    
    gridCopia = deepcopy(grid)
    formulaRestricao3 = []
    listaDeDadosPacientesSaudaveis = filtrarDadosPacientes(gridCopia, '0')
            
    for dadosPacientes in listaDeDadosPacientesSaudaveis:
        formulaAuxiliar = []
        for regra in range(numeroDeRegras):
            listaAuxiliar = []
            for index, dado in enumerate(dadosPacientes[0]):
                significadoAtomica = '_n' if dado == '1' else '_p'
                listaAuxiliar.append(Atom('X_' + str(primeiraLinha[index]) + '_' + str(regra + 1) + significadoAtomica))
                
            formulaAuxiliar.append(transformarEmDisjuncao(listaAuxiliar))
              
        formulaRestricao3.append(transformarEmConjuncao(formulaAuxiliar))               

    return transformarEmConjuncao(formulaRestricao3)


def restricao4(grid, primeiraLinha, numeroDeRegras):
    
    gridCopia = deepcopy(grid)
    formula_restricao4 = []
    ListaDeDadosPacientesDoentes = filtrarDadosPacientes(gridCopia, '1')
    
    for dadosPacientes in ListaDeDadosPacientesDoentes:
        formulaAuxiliar = []
        for regra in range(numeroDeRegras):
            listaAuxilidar = []
            for index, dado in enumerate(dadosPacientes[0]):
                significadoDaAtomica = '_n' if dado == '1' else '_p'
                listaAuxilidar.append(Or(Not(Atom('X_' + str(primeiraLinha[index]) + '_' + str(regra + 1) + significadoDaAtomica)), Not(Atom('C_' + str(regra + 1) + '_' + str(dadosPacientes[1])))))
                
            formulaAuxiliar.append(transformarEmConjuncao(listaAuxilidar))
            
        formula_restricao4.append(transformarEmConjuncao(formulaAuxiliar))
    
    return transformarEmConjuncao(formula_restricao4)


def restricao5(grid, numeroDeRegras):
    
    gridCopia = deepcopy(grid)
    formulaRestricao5 = []
    PacientesDoentes = filtrarDadosPacientes(gridCopia, '1')
    
    for paciente in PacientesDoentes:
        listaAuxiliar = []
        for regra in range(numeroDeRegras):
            listaAuxiliar.append(Atom('C_' + str(regra + 1) + '_' + str(paciente[1])))
            
        formulaRestricao5.append(transformarEmDisjuncao(listaAuxiliar))
    
    return transformarEmConjuncao(formulaRestricao5)
    

def solucao(arquivo, numeroDeRegras):
    
    if (numeroDeRegras <= 0):
        return print('QUANTIDADE DE REGRAS INVÁLIDA\n')
    
    formulaFinal = transformarEmConjuncao([restricao1(arquivo[0], numeroDeRegras), restricao2(arquivo[0], numeroDeRegras), restricao3(arquivo, arquivo[0], numeroDeRegras), restricao4(arquivo, arquivo[0], numeroDeRegras), restricao5(arquivo, numeroDeRegras)])
    resultado = satisfiability_brute_force(formulaFinal)
    
    if resultado == False:
        return print('NÃO EXISTE RESULTADO SATISFATÍVEL PARA ESSA QUANTIDADE DE REGRAS\n')
    
    resultados = organizarResultados(resultado)
    gerarRegras(resultados[0], numeroDeRegras)
        
    return laudarPacientes(resultados[1])


print('\n=========================== SOLUÇÃO ===========================\n')
start_time = time.time()
solucao(criarTabelaPacientes('dados_pacientes/column_bin_20a_30p.csv'), 10)
end_time = time.time()
print('\nTEMPO DE EXECUÇÃO:', end_time - start_time ,'\n')
