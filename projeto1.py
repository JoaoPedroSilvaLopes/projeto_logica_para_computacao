import csv

from semantics import *
from functions import *
import time

arquivo1 = 'dados_pacientes/column_bin_3a_4p.csv'
quantRegras1 = 2

"""
ATOMICAS:

X a, i, p
X a, i, n
x a, i, s
C i, j

a = atributo
i = natural representando a iesima regra (1 <= i <= m)
j = natural representando a quantidade de pacientes (1 <= j <= n)
n = quantidade de pacientes

v(X a, i, p) = é True (T) se e somente se o atributo 'a' ocorre positivamente na regra 'i'
v(X a, i, n) = é True (T) se e somente se o atributo 'a' ocorre negativamente na regra 'i'
v(X a, i, s) = é True (T) se o atributo 'a' não aparece na regra 'i'
v(C i, j) = é True (T) se a regra 'i' cobre o paciente 'j', ou seja, quando a 'i' se aplica a 'j'

- Quarta restrição: Para cada paciente com patologia, regra e atributo. Se o atributo do
paciente não se aplicar ao da regra, então a regra não cobre esta paciente.

"""


# COLOCAR TODAS AS FORMULAS EM UM ORZAO
def or_all(list_formulas):
    
    first_formula = list_formulas[0] # Pegar a primeira formula da lista das células
    del list_formulas[0] # Deletar a primeira formula para não haver repetição

    for formula in list_formulas: # For para percorrer toda a lista das células
        first_formula = Or(first_formula, formula) # Juntar todas as formulas em um grande OU condicional

    return first_formula # Retornar todas as células juntas com OU's


# COLOCAR TODAS AS FORMULAS EM UM ANDZAO
def and_all(list_formulas):
    
    first_formula = list_formulas[0] # Pegar a primeira formula da lista das células
    del list_formulas[0] # Deletar a primeira formula para não haver repetição

    for formula in list_formulas: # For para para percorrer toda a lista das células
        first_formula = And(first_formula, formula) # Juntar todas as formulas em um grande E condicional

    return first_formula # Retornar todas as células juntas com E's


# CRIAR O GRID COM OS DADOS DOS PACIENTES
def criarTabelaPacientes(arquivo):
    
    with open(arquivo) as csv_file: # CRIAR GRID
        vetor = []
        csv_reader = csv.reader(csv_file, delimiter=',')
            
        for i in csv_reader:
            vetor.append(i)
    
        return vetor

    
# RESTRIÇÃO 1
def restricao1(grid, quantRegras):
    """[summary]
    Para cada atributo e regra existem 3 possibilidades. O atributo aparece positivamente na 
    regra, o atributo aparece negativamente na regra ou o atributo não aparece na regra. 

    Returns: and_all(formula_restricao1)
    """
    
    formula_restricao1 = [] # formula para a restrição 1
    
    for i in grid: # for para percorrer o grid
        i.pop() # remover o ultimo elemento da linha
    
    for j in range(len(grid[0])): # for para percorrer as colunas da primeira linha do grid
        for i in range(quantRegras): # for para percorrer a quantidade de regras
            lista_and = [] # setar lista como vazio
            lista_parcial = [] # lista parcial que serve como auxiliar na construção da formula
            
            lista_and.append(Atom('X_' + str(grid[0][j]) + '_' + str(i + 1) + '_p')) # atomica Xa,i,p
            lista_and.append(Not(Atom('X_' + str(grid[0][j]) + '_' + str(i + 1) + '_n'))) # atomica -Xa,i,n
            lista_and.append(Not(Atom('X_' + str(grid[0][j]) + '_' + str(i + 1) + '_s'))) # atomica -Xa,i,s
            
            lista_parcial.append(and_all(lista_and)) # adicionar lista_and em um and_all e adicionar o resultado na lista_parcial
            lista_and.clear() # limpar a lista de AND
            
            lista_and.append(Not(Atom('X_' + str(grid[0][j]) + '_' + str(i + 1) + '_p'))) # atomica -Xa,i,p
            lista_and.append(Atom('X_' + str(grid[0][j]) + '_' + str(i + 1) + '_n')) # atomica Xa,i,n
            lista_and.append(Not(Atom('X_' + str(grid[0][j]) + '_' + str(i + 1) + '_s'))) # atomica -Xa,i,s]
            
            lista_parcial.append(and_all(lista_and)) # adicionar lista_and em um and_all e adicionar o resultado na lista_parcial
            lista_and.clear() # limpar a lista de AND

            lista_and.append(Not(Atom('X_' + str(grid[0][j]) + '_' + str(i + 1) + '_p'))) # atomica -Xa,i,p
            lista_and.append(Not(Atom('X_' + str(grid[0][j]) + '_' + str(i + 1) + '_n'))) # atomica -Xa,i,n
            lista_and.append(Atom('X_' + str(grid[0][j]) + '_' + str(i + 1) + '_s')) # atomica Xa,i,s

            lista_parcial.append(and_all(lista_and)) # adicionar lista_and em um and_all e adicionar o resultado na lista_parcial
            formula_restricao1.append(or_all(lista_parcial)) # adicionar a lista_parcial em um or_all e adicionar o resulta na formula_restrição1
           
    return and_all(formula_restricao1) # juntar todas as formulas de ORs em um ANDzao


# RESTRIÇÃO 2        
def restricao2(grid, quantRegras):
    """[summary]
    Cada regra deve possuir algum atributo aparecendo na mesma.
    
    Returns: and_all(formula_restricao2)
    """
    
    formula_restricao2 = [] # formula para a restrição 2
    
    for i in grid: # for para percorrer o grid
        i.pop() # remover o ultimo elemento da linha
    
    for i in range(quantRegras): # for para percorrer a quantidade de regras
        lista_or = [] # lista para ORs
        for j in range(len(grid[0])): # for para percorrer as colunas da primeira linha do grid
            lista_or.append(Not(Atom('X_' + str(grid[0][j]) + '_' + str(i + 1) + '_s'))) # Not(Xa,i,s) para construir a segunda restrição

        formula_restricao2.append(or_all(lista_or)) # Adicionar na formula da restrição 2 a formula de todas as atomicas com OR
        
    return and_all(formula_restricao2) # juntar todas as formulas de ORs em um ANDzao


# RESTRIÇÃO 3
def restricao3(grid, quantRegras):
    """[summary]
    Para cada paciente sem patologia e regra, algum atributo do paciente não
    pode ser aplicado à regra.
    
    Returns: restricao4(grid, quantRegras)
    """
    
    formula_restricao3 = [] # formula para a restrição 3
    lista_pacientesSaudaveis = [] # grid dos pacientes
    
    primeiraLinha = grid.pop(0) # linha dos atributos
    primeiraLinha.pop() # remover coluna 'P'
           
    for i in grid: # for para percorrer as linhas do grid 
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
                    
            formula_parcial.append(or_all(lista_or)) # adicionar a lista_or em ORzao e adicionar o resultado na lista formula_parcial
        formula_restricao3.append(and_all(formula_parcial)) # adicionar a lista formula_parcial em ANDzao e adicionar o resultado na lista formula_restricao3   
    
    return and_all(formula_restricao3) # juntar todas as formulas de ANDs em um ANDzao


# RESTRIÇÃO 4
def restricao4(grid, quantRegras):
    """[summary]
    Para cada paciente com patologia, regra e atributo. Se o atributo do
    paciente não se aplicar ao da regra, então a regra não cobre esta paciente.
    
    Returns and_all(formula_restricao4)
    """
    
    formula_restricao4 = []
    primeiraLinha = grid.pop(0)
    primeiraLinha.pop()
            
    for index, j in enumerate(grid): # for percorrer as linhas do grid e contabilizar o index
        formula_parcial = []
        if j[-1] == str(1): # se o ultimo elemento da linha for 0
            listaParcial = primeiraLinha # linha com os atributos
            j.pop() # remover o ultimo elemento da linha
            for i in range(quantRegras): # for para percorrer a quantidade de regras
                lista_and = [] # lista para ANDs
                for index1, y in enumerate(j): # for percorrer a linha j e contabilizar o index
                    if y == str(1): # se o elemento da linha for 1
                        lista_and.append(Implies(Atom(Atom('X_' + str(listaParcial[index1]) + '_' + str(i + 1) + '_n')), Not(Atom('C_' + str(i + 1) + '_' + str(index + 1))))) # criação da atomica
                        
                    elif y == str(0): # se o elemento da linha for 0
                        lista_and.append(Implies(Atom(Atom('X_' + str(listaParcial[index1]) + '_' + str(i + 1) + '_p')), Not(Atom('C_' + str(i + 1) + '_' + str(index + 1))))) # criação da atomica

                formula_parcial.append(and_all(lista_and)) # adicionar a lista_and em ANDzao e adicionar o resultado na lista formula_parcial
            formula_restricao4.append(and_all(formula_parcial)) # adicionar a lista formula_parcial em ANDzao e adicionar o resultado na lista formula_restricao4
    
    return and_all(formula_restricao4) # juntar todas as formulas de ANDs em um ANDzao


# RESTRIÇÃO 5
def restricao5(grid, quantRegras):
    """[summary]
    cada paciente com PATOLOGIA deve possuir ser coberto por alguma das regras
    
    Returns: and_all(formula_restricao5)
    """
    
    formula_restricao5 = [] # formula para a restrição 5
    contador = 1 # contador dos pacientes
                
    for j in grid: # for para percorrer as linhas do grid
        if j[-1] == str(1): # se o ultimo elemento da linha for 1
            lista_or = [] # lista para ORs 
            for i in range(quantRegras): # for para percorrer a quantidade de regras
                lista_or.append(Atom('C_' + str(i + 1) + '_' + str(contador))) # criação da atomica
            
            formula_restricao5.append(or_all(lista_or)) # Adicionar na formula da restrição 5 a formula de todas as atomicas com OR
            contador += 1 # adicionar mais um ao contador dos pacientes
 
    return and_all(formula_restricao5) # juntar todas as formulas de ORs em um ANDzao


# SOLUÇÃO
def solucao(arquivo, quantRegras):  
     
    teste1 = restricao1(criarTabelaPacientes(arquivo), quantRegras)
    teste2 = restricao2(criarTabelaPacientes(arquivo), quantRegras)
    teste3 = restricao3(criarTabelaPacientes(arquivo), quantRegras)
    teste4 = restricao4(criarTabelaPacientes(arquivo), quantRegras)
    teste5 = restricao5(criarTabelaPacientes(arquivo), quantRegras)

    formula_final = And(And(And(teste1, teste2), And(teste3, teste4)), teste5)
    resultado = satisfiability_brute_force(formula_final)
    
    valores_dados = []
    lista_parcial = []
    
    if resultado != False: # se o resultado for diferente de falso
        for array in resultado: # percorrer a lista com as atomicas com valoração verdadeira
            lista_segregada = array.split('_') # segregar os elementos pela string '_'
            if array.split('_')[0] == 'X': # Caso 
                lista_segregada.pop(0) # remover primeiro elemento
                if lista_segregada[-1] == 'p': # se o ultimo elemento for a string 'p'
                    lista_segregada.pop() # remover o ultimo elemento
                    lista_parcial.append(lista_segregada) # acrescentar lista_segredada à lista_parcial
                    
                elif lista_segregada[-1] == 'n': # se o ultimo elemento for a string 'n'
                    lista_segregada.pop() # remover o ultimo elemento
                    lista_segregada[0] = lista_segregada[0].replace('<=', '>') # fazer a inversão de desigualdades
                    lista_parcial.append(lista_segregada) # acrescentar lista_segredada à lista_parcial
                    
    regras = criar_regras(lista_parcial, quantRegras)
    
    grid_pacientes = criarTabelaPacientes(arquivo)
    linha_atributos = grid_pacientes.pop(0)
    linha_atributos.pop()
    
    for i in grid_pacientes:
        valores_dados.append(i.pop())
    
    laudarPacientes(regras, grid_pacientes, linha_atributos, valores_dados, quantRegras)


# CRIAR REGRAS
def criar_regras(lista_parcial, quantRegras):
    
    lista_final_de_regras = []

    for regras in range(quantRegras): # for para percorrer a quantidade de regras
        lista_parcial_de_regras = [] # lista auxiliar para construir as regras
        
        for lista_de_regras in lista_parcial: # for para percorrer as linhas da lista parcial
            if str(lista_de_regras[-1]) == str(regras + 1): # se o ultimo elemento da linha for igual ao numero da regra
                lista_parcial_de_regras.append(lista_de_regras[0]) # acrescentar o primeiro elemento da linha (atributo) à lista_parcial_de_regras
                
        lista_final_de_regras.append(lista_parcial_de_regras) # acrescentar a lista_parcial_de_regras à lista_final_de_regras
            
    for index, i in enumerate(lista_final_de_regras): # percorrer lista_final_de_regras para criar a mensagem das regras
        print(f'REGRA {index + 1}: {i} => P')
        
    return lista_final_de_regras


# LAUDAR OS PACIENTES COM BASE NAS REGRAS E COMPARAR COM OS DADOS DO ARQUIVO
def laudarPacientes(lista_final_de_regras, grid_pacientes, linha_atributos, valores_dados, quantRegras):
    
    formula_valores_pacientes = []
    formula_valores_regras = []
    
    for i in grid_pacientes:
        formula_parcial = []
        for index, j in enumerate(i):
            if j == str(1):
                formula_parcial.append(linha_atributos[index])
                
            else:
                teste = linha_atributos[index].replace('<=', '>')   
                formula_parcial.append(teste)
        
        formula_valores_pacientes.append(formula_parcial)  
    
    for index, pacientes in enumerate(formula_valores_pacientes):
        teste1 = []
        for i in lista_final_de_regras:
            formula_teste = []
            for j in i:
                for atributos_pacientes in pacientes:
                    if atributos_pacientes == j:
                        formula_teste.append(atributos_pacientes)
            
            if formula_teste != i:
                teste1.append(0)
                
            else:
                teste1.append(1)
        
        formula_valores_regras.append(teste1)  
    
    laudo_final = []  
    for index, i in enumerate(formula_valores_regras):
        if 1 in i: # significa que o paciente obedece alguma regra
            laudo_final.append('1')
        
        else:
            laudo_final.append('0')
                  
    if laudo_final == valores_dados:
        return print(f'OS PACIENTES FORAM CORRETAMENTE DIAGNOSTICADOS COM {quantRegras} REGRAS')

        
    else:
        return print(f'OS PACIENTES NÃO FORAM CORRETAMENTE DIAGNOSTICADOS COM {quantRegras} REGRAS')


print('SOLUÇÃO')
start_time = time.time()
solucao(arquivo1, quantRegras1)
end_time = time.time()
print('Tempo de execução:', end_time - start_time)
