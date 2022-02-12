import csv
import time
from algoritmoDPLL import *
from copy import deepcopy
from funcoesAuxiliaresProjeto import *


def abrirTabelaCNF(CNF):
    
    with open(CNF) as arquivo:
        
        grid = []
        
        for linha in arquivo:
            if linha[0] != 'c' and linha[0] != 'p' and linha[0] != '%' and linha[0] != '0' and linha[0] != ' ':
                linhaInt = []
                
                linha = linha.split(' ')
                linha.pop(-1)
                
                for elemento in linha:
                    linhaInt.append(int(elemento))
                
                grid.append(linhaInt)

    return grid


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
    
    for atributoPrimeiraLinha in gridCopia:
        for regra in range(numeroDeRegras):
            
            listaDeAtomicas = []
            
            listaDeAtomicas.append(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_p'))
            listaDeAtomicas.append(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_n'))
            listaDeAtomicas.append(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_s'))
            
            formulaCompleta.append(listaDeAtomicas)
            listaDeAtomicas = []
            
            listaDeAtomicas.append(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_p'))
            listaDeAtomicas.append(Not(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_n')))
            listaDeAtomicas.append(Not(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_s')))
            
            formulaCompleta.append(listaDeAtomicas)
            listaDeAtomicas = []
            
            listaDeAtomicas.append(Not(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_p')))
            listaDeAtomicas.append(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_n'))
            listaDeAtomicas.append(Not(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_s')))
            
            formulaCompleta.append(listaDeAtomicas)
            listaDeAtomicas = []
            
            listaDeAtomicas.append(Not(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_p')))
            listaDeAtomicas.append(Not(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_n')))
            
            formulaCompleta.append(listaDeAtomicas)
            listaDeAtomicas = []
            
            listaDeAtomicas.append(Not(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_p')))
            listaDeAtomicas.append(Not(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_s')))
            
            formulaCompleta.append(listaDeAtomicas)
            listaDeAtomicas = []
            
            listaDeAtomicas.append(Not(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_n')))
            listaDeAtomicas.append(Not(Atom('X_' + str(atributoPrimeiraLinha) + '_' + str(regra + 1) + '_s')))
            
            formulaCompleta.append(listaDeAtomicas)
    
    return

  
def restricao2(grid, numeroDeRegras):
    
    gridCopia = deepcopy(grid)
    gridCopia.pop()
    
    for regra in range(numeroDeRegras):
        listaAuxiliar = []
        for atributosDoGrid in gridCopia:
            listaAuxiliar.append(Not(Atom('X_' + str(atributosDoGrid) + '_' + str(regra + 1) + '_s')))
        
        formulaCompleta.append(listaAuxiliar)
    
    return


def restricao3(grid, primeiraLinha, numeroDeRegras):
    
    gridCopia = deepcopy(grid)
    listaDeDadosPacientesSaudaveis = filtrarDadosPacientes(gridCopia, '0')
            
    for dadosPacientes in listaDeDadosPacientesSaudaveis:
        for regra in range(numeroDeRegras):
            listaAuxiliar = []
            for index, dado in enumerate(dadosPacientes[0]):
                significadoAtomica = '_n' if dado == '1' else '_p'
                listaAuxiliar.append(Atom('X_' + str(primeiraLinha[index]) + '_' + str(regra + 1) + significadoAtomica))
                
            formulaCompleta.append(listaAuxiliar)          

    return


def restricao4(grid, primeiraLinha, numeroDeRegras):
    
    gridCopia = deepcopy(grid)
    ListaDeDadosPacientesDoentes = filtrarDadosPacientes(gridCopia, '1')
    
    for dadosPacientes in ListaDeDadosPacientesDoentes:
        for regra in range(numeroDeRegras):
            for index, dado in enumerate(dadosPacientes[0]):
                significadoDaAtomica = '_n' if dado == '1' else '_p'
                lista1 = [Not(Atom('X_' + str(primeiraLinha[index]) + '_' + str(regra + 1) + significadoDaAtomica)), Not(Atom('C_' + str(regra + 1) + '_' + str(dadosPacientes[1])))]
                formulaCompleta.append(lista1)
    
    return


def restricao5(grid, numeroDeRegras):
    
    gridCopia = deepcopy(grid)
    PacientesDoentes = filtrarDadosPacientes(gridCopia, '1')
    
    for paciente in PacientesDoentes:
        listaAuxiliar = []
        for regra in range(numeroDeRegras):
            listaAuxiliar.append(Atom('C_' + str(regra + 1) + '_' + str(paciente[1])))

        formulaCompleta.append(listaAuxiliar)
    
    return

    
def solucao(arquivo, numeroDeRegras):
    
    if numeroDeRegras == 0:
        
        arquivoDIMACS = abrirTabelaCNF(arquivo)
        resultado = DPLL(arquivoDIMACS)
        
        if resultado == False:
            return print('NÃO EXISTE RESULTADO SATISFATÍVEL ESSA FÓRMULA\n')
        
        return print(f'RESULTADO SATISFATÍVEL: {resultado}')
    
    elif numeroDeRegras > 0:
    
        restricao1(arquivo[0], numeroDeRegras)
        restricao2(arquivo[0], numeroDeRegras)
        restricao3(arquivo, arquivo[0], numeroDeRegras)
        restricao4(arquivo, arquivo[0], numeroDeRegras)
        restricao5(arquivo, numeroDeRegras)
        
        formulaDIMACS, numeroAtomicas, listaAtomicasNumeros = transformarEmDIMACS(formulaCompleta)
        criarArquivosDIMACS(formulaDIMACS, numeroAtomicas)
        
        arquivoDIMACS = abrirTabelaCNF('dadosPacientes.txt')
        resultado = DPLL(arquivoDIMACS)
        
        if resultado == False:
            return print('NÃO EXISTE RESULTADO SATISFATÍVEL PARA ESSA QUANTIDADE DE REGRAS\n')
        
        resultadoFinal = removerNegacoes(resultado)
        resultadoFinal = transformarEmAtomicas(resultadoFinal, listaAtomicasNumeros)
        resultadoFinal = organizarResultados(resultadoFinal)
        gerarRegras(resultadoFinal[0], numeroDeRegras)
        
        return laudarPacientes(resultadoFinal[1])
    
    return print('NUMERO DE REGRAS INVÁLIDA')


def transformarEmAtomicas(resultado, listaAtomicasNumeros):
    
    resultadoAtomicas = []
    
    for elementos in resultado:
        for posicao in listaAtomicasNumeros:
            if elementos == posicao[0]:
                resultadoAtomicas.append(str(posicao[1]))
                
    return resultadoAtomicas


def transformarEmDIMACS(formulaCNF):
    
    listaDeClausulas = []
    listaNumerosEAtomicas = []
    formulaDIMACS = []
    numeroAtomicas = 0
    
    for clausula in formulaCNF:
        for literal in clausula:
            if isinstance(literal, Atom):
                listaDeClausulas.append(literal)
                        
    for index, clausula in enumerate(set(listaDeClausulas)):
        listaNumerosEAtomicas.append([index + 1, clausula])
        numeroAtomicas += 1 
    
    for clausula in formulaCNF:
        listaAuxiliar = []
        for literal in clausula:
            for teste in listaNumerosEAtomicas:
                if literal == Not(teste[1]):
                    listaAuxiliar.append(teste[0] * -1)
                    
                elif literal == teste[1]:
                    listaAuxiliar.append(teste[0])
                    
        formulaDIMACS.append(listaAuxiliar)
                
    return formulaDIMACS, numeroAtomicas, listaNumerosEAtomicas


def criarArquivosDIMACS(formulaDIMACS, numeroAtomicas):
    
    numeroClausulas = 0
    
    for clausula in formulaDIMACS:
        numeroClausulas += 1
    
    with open("dadosPacientes.txt", "w") as arquivo:
        
        arquivo.writelines('c This Formular is generated by mcnf\n')
        arquivo.writelines('c\n')
        arquivo.writelines('c\n')
        arquivo.writelines(f'p cnf {numeroAtomicas} {numeroClausulas}\n')

        
        for clausula in formulaDIMACS:
            
            clausula = str(clausula).replace(',', '')
            clausula = str(clausula).replace('[', '')
            clausula1 = str(clausula).replace(']', '')
            
            arquivo.writelines(f'{clausula1} 0\n')
    
    return


formulaCompleta = []

print('\n=========================== SOLUÇÃO ===========================\n')
start_time = time.time()
solucao(criarTabelaPacientes('dados_pacientes/column_bin_20a_30p.csv'), 4)

# FORMULAS INSATISFATÍVEIS
solucao('TestesDIMACSCNF/Fórmulas Insatisfatíveis/uuf50-01.cnf', 0)
solucao('TestesDIMACSCNF/Fórmulas Insatisfatíveis/uuf50-02.cnf', 0)
solucao('TestesDIMACSCNF/Fórmulas Insatisfatíveis/uuf50-03.cnf', 0)
solucao('TestesDIMACSCNF/Fórmulas Insatisfatíveis/uuf250-01.cnf', 0)
solucao('TestesDIMACSCNF/Fórmulas Insatisfatíveis/uuf250-02.cnf', 0)
solucao('TestesDIMACSCNF/Fórmulas Insatisfatíveis/uuf250-03.cnf', 0)

# FORMULAS SATISFATÍVEIS
solucao('TestesDIMACSCNF/Fórmulas Satisfatíveis/uf50-01.cnf', 0)
solucao('TestesDIMACSCNF/Fórmulas Satisfatíveis/uf50-02.cnf', 0)
solucao('TestesDIMACSCNF/Fórmulas Satisfatíveis/uf50-03.cnf', 0)
solucao('TestesDIMACSCNF/Fórmulas Satisfatíveis/uf250-01.cnf', 0)
solucao('TestesDIMACSCNF/Fórmulas Satisfatíveis/sw100-1-500.cnf', 0)
solucao('TestesDIMACSCNF/Fórmulas Satisfatíveis/logistics.a-828.cnf', 0)
solucao('TestesDIMACSCNF/Fórmulas Satisfatíveis/logistics.c-1141.cnf', 0)
solucao('TestesDIMACSCNF/Fórmulas Satisfatíveis/flat200-1-600', 0)

end_time = time.time()
print('\nTEMPO DE EXECUÇÃO:', end_time - start_time ,'\n')
