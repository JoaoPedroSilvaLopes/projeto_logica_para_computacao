import csv
from semantics import *
from functions import *
import time
from copy import deepcopy


# COLOCAR TODAS AS FORMULAS EM UM ORZAO
def orzao(list_formulas):
    
    first_formula = list_formulas[0] # Pegar a primeira formula da lista das células
    del list_formulas[0] # Deletar a primeira formula para não haver repetição

    for formula in list_formulas: # For para percorrer toda a lista das células
        first_formula = Or(first_formula, formula) # Juntar todas as formulas em um grande OU condicional

    return first_formula # Retornar todas as células juntas com OU's


# COLOCAR TODAS AS FORMULAS EM UM ANDZAO
def andzao(list_formulas):
    
    first_formula = list_formulas[0] # Pegar a primeira formula da lista das células
    del list_formulas[0] # Deletar a primeira formula para não haver repetição

    for formula in list_formulas: # For para para percorrer toda a lista das células
        first_formula = And(first_formula, formula) # Juntar todas as formulas em um grande E condicional

    return first_formula # Retornar todas as células juntas com E's


# CRIAR O GRID COM OS DADOS DOS PACIENTES
def criarTabelaPacientes(arquivo):
    
    with open(arquivo) as csv_file: # abrir o arquivo .csv com os dados
        vetor = [] # vetor para guardar as listas
        csv_reader = csv.reader(csv_file, delimiter=',') # ler o arquivo e delimitar e separar os dados por virgula
        
        for i in csv_reader: # for para percorrer csv_reader
            vetor.append(i) # acrescentar os dados no vetor
    
        return vetor # retornar vetor

    
# RESTRIÇÃO 1
def restricao1(grid, quantRegras):
    """[summary]
    Para cada atributo e regra existem 3 possibilidades. O atributo aparece positivamente na 
    regra, o atributo aparece negativamente na regra ou o atributo não aparece na regra. 

    Returns: andzao(formula_restricao1)
    """
    
    gridCopia = deepcopy(grid)
    formula_restricao1 = [] # formula para a restrição 1
    gridCopia.pop() # remover o ultimo elemento do grid
    
    for j in gridCopia: # for para percorrer as colunas da primeira linha do grid
        for i in range(quantRegras): # for para percorrer a quantidade de regras
            lista_and = [] # setar lista como vazio
            lista_parcial = [] # lista parcial que serve como auxiliar na construção da formula
            
            lista_and.append(Atom('X_' + str(j) + '_' + str(i + 1) + '_p')) # atomica Xa,i,p
            lista_and.append(Not(Atom('X_' + str(j) + '_' + str(i + 1) + '_n'))) # atomica -Xa,i,n
            lista_and.append(Not(Atom('X_' + str(j) + '_' + str(i + 1) + '_s'))) # atomica -Xa,i,s
            
            lista_parcial.append(andzao(lista_and)) # adicionar lista_and em um andzao e adicionar o resultado na lista_parcial
            lista_and.clear() # limpar a lista de AND
            
            lista_and.append(Not(Atom('X_' + str(j) + '_' + str(i + 1) + '_p'))) # atomica -Xa,i,p
            lista_and.append(Atom('X_' + str(j) + '_' + str(i + 1) + '_n')) # atomica Xa,i,n
            lista_and.append(Not(Atom('X_' + str(j) + '_' + str(i + 1) + '_s'))) # atomica -Xa,i,s
            
            lista_parcial.append(andzao(lista_and)) # adicionar lista_and em um andzao e adicionar o resultado na lista_parcial
            lista_and.clear() # limpar a lista de AND

            lista_and.append(Not(Atom('X_' + str(j) + '_' + str(i + 1) + '_p'))) # atomica -Xa,i,p
            lista_and.append(Not(Atom('X_' + str(j) + '_' + str(i + 1) + '_n'))) # atomica -Xa,i,n
            lista_and.append(Atom('X_' + str(j) + '_' + str(i + 1) + '_s')) # atomica Xa,i,s

            lista_parcial.append(andzao(lista_and)) # adicionar lista_and em um andzao e adicionar o resultado na lista_parcial
            formula_restricao1.append(orzao(lista_parcial)) # adicionar a lista_parcial em um orzao e adicionar o resulta na formula_restrição1
        
    return andzao(formula_restricao1) # juntar todas as formulas de ORs em um ANDzao


# RESTRIÇÃO 2        
def restricao2(grid, quantRegras):
    """[summary]
    Cada regra deve possuir algum atributo aparecendo na mesma.
    
    Returns: andzao(formula_restricao2)
    """
    
    gridCopia = deepcopy(grid)
    formula_restricao2 = [] # formula para a restrição 2
    gridCopia.pop() # remover o ultimo elemento do grid
    
    for i in range(quantRegras): # for para percorrer a quantidade de regras
        lista_or = [] # lista para ORs
        for j in gridCopia: # for para percorrer as colunas da primeira linha do grid
            lista_or.append(Not(Atom('X_' + str(j) + '_' + str(i + 1) + '_s'))) # Not(Xa,i,s) para construir a segunda restrição

        formula_restricao2.append(orzao(lista_or)) # Adicionar na formula da restrição 2 a formula de todas as atomicas com OR
    
    return andzao(formula_restricao2) # juntar todas as formulas de ORs em um ANDzao


# RESTRIÇÃO 3
def restricao3(grid, quantRegras):
    """[summary]
    Para cada paciente sem patologia e regra, algum atributo do paciente não
    pode ser aplicado à regra.
    
    Returns: restricao4(grid, quantRegras)
    """
    
    gridCopia = deepcopy(grid)
    formula_restricao3 = [] # formula para a restrição 3
    lista_pacientesSaudaveis = [] # grid dos pacientes
    
    primeiraLinha = gridCopia.pop(0) # linha dos atributos
    primeiraLinha.pop() # remover coluna 'P'
           
    for i in gridCopia: # for para percorrer as linhas do grid 
        if i[-1] == str(0): # se o ultimo elemento da linha for 0 (evidenciando que o paciente é saudável)
            i.pop() # remover o ultimo elemento da linha
            lista_pacientesSaudaveis.append(i) # Adicionar linha em que o paciente é saudável na lista
                   
    for i in lista_pacientesSaudaveis: # for para percorrer as linhas do grid lista_pacientesSaudaveis
        formula_parcial = []
        for j in range(quantRegras): # for para percorrer a quantidade de regras
            lista_or = [] # lista para ORs
            for index, y in enumerate(i): # for para percorrer a linha j e contabilizar o index                    
                if y == str(1): # se o elemento da linha for 1
                    lista_or.append(Atom('X_' + str(primeiraLinha[index]) + '_' + str(j + 1) + '_n')) # criação da atomica
                        
                elif y == str(0): # se o elemento da linha for 0
                    lista_or.append(Atom('X_' + str(primeiraLinha[index]) + '_' + str(j + 1) + '_p')) # criação da atomica    
                    
            formula_parcial.append(orzao(lista_or)) # adicionar a lista_or em ORzao e adicionar o resultado na lista formula_parcial
        formula_restricao3.append(andzao(formula_parcial)) # adicionar a lista formula_parcial em ANDzao e adicionar o resultado na lista formula_restricao3   
    
    return andzao(formula_restricao3) # juntar todas as formulas de ANDs em um ANDzao


# RESTRIÇÃO 4
def restricao4(grid, quantRegras):
    """[summary]
    Para cada paciente com patologia, regra e atributo. Se o atributo do
    paciente não se aplicar ao da regra, então a regra não cobre esta paciente.
    
    Returns andzao(formula_restricao4)
    """
    
    gridCopia = deepcopy(grid)
    formula_restricao4 = [] # formula para a restrição 4
    primeiraLinha = gridCopia.pop(0) # pegar linha dos atributos do grid
    primeiraLinha.pop() # remover o ultimo elemento 'P'
            
    for index, j in enumerate(gridCopia): # for percorrer as linhas do grid e contabilizar o index
        formula_parcial = []
        if j[-1] == str(1): # se o ultimo elemento da linha for 1
            j.pop() # remover o ultimo elemento da linha
            for i in range(quantRegras): # for para percorrer a quantidade de regras
                lista_and = [] # lista para ANDs
                for index1, y in enumerate(j): # for percorrer a linha j e contabilizar o index
                    if y == str(1): # se o elemento da linha for 1
                        lista_and.append(Implies(Atom(Atom('X_' + str(primeiraLinha[index1]) + '_' + str(i + 1) + '_n')), Not(Atom('C_' + str(i + 1) + '_' + str(index + 1))))) # criação da atomica
                        
                    elif y == str(0): # se o elemento da linha for 0
                        lista_and.append(Implies(Atom(Atom('X_' + str(primeiraLinha[index1]) + '_' + str(i + 1) + '_p')), Not(Atom('C_' + str(i + 1) + '_' + str(index + 1))))) # criação da atomica

                formula_parcial.append(andzao(lista_and)) # adicionar a lista_and em ANDzao e adicionar o resultado na lista formula_parcial
            formula_restricao4.append(andzao(formula_parcial)) # adicionar a lista formula_parcial em ANDzao e adicionar o resultado na lista formula_restricao4
    
    return andzao(formula_restricao4) # juntar todas as formulas de ANDs em um ANDzao


# RESTRIÇÃO 5
def restricao5(grid, quantRegras):
    """[summary]
    cada paciente com PATOLOGIA deve possuir ser coberto por alguma das regras
    
    Returns: andzao(formula_restricao5)
    """
    
    gridCopia = deepcopy(grid)
    
    formula_restricao5 = [] # formula para a restrição 5
    contador = 1 # contador dos pacientes
    gridCopia.pop(0)
                
    for j in gridCopia: # for para percorrer as linhas do grid
        if j[-1] == str(1): # se o ultimo elemento da linha for 1
            lista_or = [] # lista para ORs 
            for i in range(quantRegras): # for para percorrer a quantidade de regras
                lista_or.append(Atom('C_' + str(i + 1) + '_' + str(contador))) # criação da atomica
            
            formula_restricao5.append(orzao(lista_or)) # Adicionar na formula da restrição 5 a formula de todas as atomicas com OR
            contador += 1 # adicionar mais um ao contador dos pacientes
    
    return andzao(formula_restricao5) # juntar todas as formulas de ORs em um ANDzao


# SOLUÇÃO
def solucao(arquivo, quantRegras):
    
    grid = criarTabelaPacientes(arquivo)

    formula_final = And(And(And(restricao1(grid[0], quantRegras), restricao2(grid[0], quantRegras)), And(restricao3(grid, quantRegras), restricao4(grid, quantRegras))), restricao5(grid, quantRegras)) # formula final é o and de todas as restrições
    resultado = satisfiability_brute_force(formula_final) # atribuir ao resultado o resultado de satisfiability_brute_force(formula_final)
    
    lista_parcialX = [] # lista para guardar as atomicas que começam com X
    lista_parcialC = [] # lista para guardar as atomicas que começam com C
    lista_dados = [] # lista para guardar os diagnosticos dos pacientes provenientes dos dados do arquivo
    quantPacientes = 0 # quantidade de pacientes
    
    if resultado != False: # se o resultado for diferente de falso
        for array in resultado: # percorrer a lista com as atomicas com valoração verdadeira
            lista_segregada = array.split('_') # segregar os elementos pela string '_'
            if array.split('_')[0] == 'X': # Caso a atomica comece com X
                lista_segregada.pop(0) # remover primeiro elemento
                if lista_segregada[-1] == 'p': # se o ultimo elemento for a string 'p'
                    lista_segregada.pop() # remover o ultimo elemento
                    lista_parcialX.append(lista_segregada) # acrescentar lista_segredada à lista_parcial
                    
                elif lista_segregada[-1] == 'n': # se o ultimo elemento for a string 'n'
                    lista_segregada.pop() # remover o ultimo elemento
                    lista_segregada[0] = lista_segregada[0].replace('<=', '>') # fazer a inversão de desigualdades
                    lista_parcialX.append(lista_segregada) # acrescentar lista_segredada à lista_parcial
                    
            else: # Caso a atomica comece com C
                lista_segregada.pop(0) # remover primeiro elemento no caso 'C'
                lista_parcialC.append(lista_segregada.pop(0)) # remover elemento que se refere as regras e acrescenta-lo a lista_parcialC
    
    else: # caso seja Falso
        return print('Resultado insatisfatível') # printar que é insatisfativel
                    
    criar_regras(lista_parcialX, quantRegras) # regras recebe a lista_final_de_regras provenientes da função criar_regras
    
    for index, i in enumerate(criarTabelaPacientes(arquivo)): # for para percorrer o grid pacientes
        quantPacientes = index # remover o ultimo elemento de grid_pacientes
        lista_dados.append(i.pop()) # pegar somente o ultimo elemento
        
    return laudarPacientes(lista_parcialC, lista_dados, quantPacientes, quantRegras) # retornar o laudo dos pacientes


# CRIAR REGRAS
def criar_regras(lista_parcial, quantRegras):
    
    lista_final_de_regras = [] # lista para guardar as regras

    for regras in range(quantRegras): # for para percorrer a quantidade de regras
        lista_parcial_de_regras = [] # lista auxiliar para construir as regras
        
        for lista_de_regras in lista_parcial: # for para percorrer as linhas da lista parcial
            if str(lista_de_regras[-1]) == str(regras + 1): # se o ultimo elemento da linha for igual ao numero da regra
                lista_parcial_de_regras.append(lista_de_regras[0]) # acrescentar o primeiro elemento da linha (atributo) à lista_parcial_de_regras
                
        lista_final_de_regras.append(lista_parcial_de_regras) # acrescentar a lista_parcial_de_regras à lista_final_de_regras
            
    for index, i in enumerate(lista_final_de_regras): # percorrer lista_final_de_regras para criar a mensagem das regras
        print(f'REGRA {index + 1}: {i} => P') # printar a regra em questão explanando qual é a regra e como a mesma é
        
    return lista_final_de_regras # retornar lista_final_de_regras


# LAUDAR OS PACIENTES COM BASE NAS REGRAS E COMPARAR COM OS DADOS DO ARQUIVO
def laudarPacientes(lista_parcialC, lista_dados, quantPacientes, quantRegras):
    
    laudo_final = ['0'] * quantPacientes # criar somente com elementos sendo 0 do tamanho da quantidade de pacientes
    lista_dados.pop(0) # remover o primeiro elemento da lista_dados
        
    for i in sorted(set(lista_parcialC)): # for para percorrer a lista_parcialC ordenada
        laudo_final[int(i) - 1] = '1' # substituir o valor do elemento da posição do laudo_final por 1 evidenciando que nessa posição o paciente é diagnosticado com patologia
        
    if laudo_final == lista_dados: # se a lista laudo_final for igual a lista valores_dados evidencia que os pacientes foram corretamente diagnosticados
        return print(f'OS PACIENTES FORAM CORRETAMENTE DIAGNOSTICADOS COM {quantRegras} REGRAS') # print do resultado
    
    else: # se não os pacientes não foram corretamente diagnosticados
        return print(f'OS PACIENTES NÃO FORAM CORRETAMENTE DIAGNOSTICADOS COM {quantRegras} REGRAS') # print do resultado


print('SOLUÇÃO')
start_time = time.time()
solucao('dados_pacientes/column_bin_3a_3p.csv', 2)
end_time = time.time()
print('Tempo de execução:', end_time - start_time)
