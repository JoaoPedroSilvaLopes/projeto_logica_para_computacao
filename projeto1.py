import csv

from semantics import *
from functions import *

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


# colocar todas as formulas em um ORzao
def or_all(list_formulas):
    
    first_formula = list_formulas[0] # Pegar a primeira formula da lista das células
    del list_formulas[0] # Deletar a primeira formula para não haver repetição

    for formula in list_formulas: # For para percorrer toda a lista das células
        first_formula = Or(first_formula, formula) # Juntar todas as formulas em um grande OU condicional

    return first_formula # Retornar todas as células juntas com OU's


# colocar todas as formulas em um ANDzao
def and_all(list_formulas):
    
    first_formula = list_formulas[0] # Pegar a primeira formula da lista das células
    del list_formulas[0] # Deletar a primeira formula para não haver repetição

    for formula in list_formulas: # For para para percorrer toda a lista das células
        first_formula = And(first_formula, formula) # Juntar todas as formulas em um grande E condicional

    return first_formula # Retornar todas as células juntas com E's


# criar o grid com os dados dos pacientes
def criarTabelaPacientes(arquivo):
    
    with open(arquivo) as csv_file: # CRIAR GRID
        vetor = []
        csv_reader = csv.reader(csv_file, delimiter=',')
            
        for i in csv_reader:
            vetor.append(i)
    
        return vetor


# OK
def restrição1(grid, quantRegras):
    """[summary]
    Para cada atributo e regra existem 3 possibilidades. O atributo aparece positivamente na 
    regra, o atributo aparece negativamente na regra ou o atributo não aparece na regra. 

    Returns: and_all(formula_restrição1)
    """
    
    formula_restrição1 = [] # formula para a restrição 1
    
    for i in grid: # for para percorrer o grid
        i.pop() # remover o ultimo elemento da linha
    
    for j in range(len(grid[0])): # for para percorrer as colunas da primeira linha do grid
        for i in range(quantRegras): # for para percorrer a quantidade de regras
            lista_or = [] # lista para ORs
            
            lista_or.append(str(Atom('X_' + str(grid[0][j]) + '_' + str(i + 1) + '_p'))) # atomica Xa,i,p
            lista_or.append(str(Atom('X_' + str(grid[0][j]) + '_' + str(i + 1) + '_n'))) # atomica Xa,i,n
            lista_or.append(str(Atom('X_' + str(grid[0][j]) + '_' + str(i + 1) + '_s'))) # atomica Xa,i,s
            
            formula_restrição1.append(or_all(lista_or)) # Adicionar na formula da restrição 1 a formula de todas as atomicas com OR
            
    return and_all(formula_restrição1) # juntar todas as formulas de ORs em um ANDzao


# OK        
def restrição2(grid, quantRegras):
    """[summary]
    Cada regra deve possuir algum atributo aparecendo na mesma.
    
    Returns: and_all(formula_restrição2)
    """
    
    formula_restrição2 = [] # formula para a restrição 2
    
    for i in grid: # for para percorrer o grid
        i.pop() # remover o ultimo elemento da linha
    
    for i in range(quantRegras): # for para percorrer a quantidade de regras
        lista_or = [] # lista para ORs
        for j in range(len(grid[0])): # for para percorrer as colunas da primeira linha do grid
            lista_or.append(Not(Atom('X_' + str(grid[0][j]) + '_' + str(i + 1) + '_s'))) # Not(Xa,i,s) para construir a segunda restrição

        formula_restrição2.append(or_all(lista_or)) # Adicionar na formula da restrição 2 a formula de todas as atomicas com OR
            
    return and_all(formula_restrição2) # juntar todas as formulas de ORs em um ANDzao


# OK 
def restrição3(grid, quantRegras):
    """[summary]
    Para cada paciente sem patologia e regra, algum atributo do paciente não
    pode ser aplicado à regra.
    
    Returns: restrição4(grid, quantRegras)
    """
    
    formula_restrição3 = [] # formula para a restrição 3
    lista_pacientesSaudaveis = []
    gridParcial = [] # linha dos atributos
    
    for j in grid: # for para percorrer as linhas do grid 
        if j[-1] == str('P'): # se o ultimo elemento da linha for P
            j.pop() # remover o ultimo elemento da linha
            gridParcial.append(j)  
            
    for i in grid: # for para percorrer as linhas do grid 
        if i[-1] == str(0): # se o ultimo elemento da linha for 0 (evidenciando que o paciente é saudável)
            i.pop() # remover o ultimo elemento da linha
            lista_pacientesSaudaveis.append(i) # Adicionar linha em que o paciente é saudável na lista
                   
    for i in lista_pacientesSaudaveis: # for para percorrer as linhas do grid lista_pacientesSaudaveis
        formula_parcial = []
        for j in range(quantRegras): # for para percorrer a quantidade de regras
            lista_or = [] # lista para ORs
            for index, y in enumerate(i): # for para percorrer a linha j e contabilizar o index
                
                #print(index)
                teste = gridParcial[0][index]
                print(teste)
                
                """if y == str(1): # se o elemento da linha for 1
                    
                    #teste = gridParcial[0][index]
                    #print(teste)
                    
                    lista_or.append(Atom('X_' + str(teste) + '_' + str(j + 1) + '_n')) # criação da atomica
                    
                elif y == str(0): # se o elemento da linha for 0
                    
                    #teste = gridParcial[0][index]
                    #print(teste)
                    
                    lista_or.append(Atom('X_' + str(teste) + '_' + str(j + 1) + '_p')) # criação da atomica"""
                    
                    
                    
                    
            #formula_parcial.append(or_all(lista_or)) # adicionar a lista_or em ORzao e adicionar o resultado na lista formula_parcial
        #formula_restrição3.append(and_all(formula_parcial)) # adicionar a lista formula_parcial em ANDzao e adicionar o resultado na lista formula_restrição3   
             
    return False #and_all(formula_restrição3) # juntar todas as formulas de ANDs em um ANDzao


# OK
def restrição4(grid, quantRegras):
    """[summary]
    Para cada paciente com patologia, regra e atributo. Se o atributo do
    paciente não se aplicar ao da regra, então a regra não cobre esta paciente.
    
    Returns and_all(formula_restrição4)
    """
    
    formula_restrição4 = [] # formula para a restrição 4
    primeiraLinha = [] # linha dos atributos
    
    for j in grid: # for para percorrer as linhas do grid 
        if j[-1] == str('P'): # se o ultimo elemento da linha for P
            j.pop() # remover o ultimo elemento da linha
            primeiraLinha.append(j)
            
    for index, j in enumerate(grid): # for percorrer as linhas do grid e contabilizar o index
        formula_parcial = []
        if j[-1] == str(1): # se o ultimo elemento da linha for 0
            listaParcial = primeiraLinha # linha com os atributos
            j.pop() # remover o ultimo elemento da linha
            for i in range(quantRegras): # for para percorrer a quantidade de regras
                lista_and = [] # lista para ANDs
                for index1, y in enumerate(j): # for percorrer a linha j e contabilizar o index
                    if y == str(1): # se o elemento da linha for 1
                        lista_and.append(str(Implies(Atom(Atom('X_' + str(listaParcial[0][index1]) + '_' + str(i + 1) + '_n')), Not(Atom('C_' + str(i + 1) + '_' + str(index)))))) # criação da atomica
                        
                    else: # se o elemento da linha for 0
                        lista_and.append(str(Implies(Atom(Atom('X_' + str(listaParcial[0][index1]) + '_' + str(i + 1) + '_p')), Not(Atom('C_' + str(i + 1) + '_' + str(index)))))) # criação da atomica
                      
                formula_parcial.append(and_all(lista_and)) # adicionar a lista_and em ANDzao e adicionar o resultado na lista formula_parcial
                
            formula_restrição4.append(and_all(formula_parcial)) # adicionar a lista formula_parcial em ANDzao e adicionar o resultado na lista formula_restrição4
    
    return and_all(formula_restrição4) # juntar todas as formulas de ANDs em um ANDzao


# OK
def restrição5(grid, quantRegras):
    """[summary]
    cada paciente com PATOLOGIA deve possuir ser coberto por alguma das regras
    
    Returns: and_all(formula_restrição5)
    """
    
    formula_restrição5 = [] # formula para a restrição 5
    contador = 1 # contador dos pacientes
                
    for j in grid: # for para percorrer as linhas do grid
        if j[-1] == str(1): # se o ultimo elemento da linha for 1
            lista_or = [] # lista para ORs 
            for i in range(quantRegras): # for para percorrer a quantidade de regras
                lista_or.append(str(Atom('C_' + str(i + 1) + '_' + str(contador)))) # criação da atomica
            
            formula_restrição5.append(or_all(lista_or)) # Adicionar na formula da restrição 5 a formula de todas as atomicas com OR
            contador += 1 # adicionar mais um ao contador dos pacientes
 
    return and_all(formula_restrição5) # juntar todas as formulas de ORs em um ANDzao



def solucao(grid, quantRegras):
    
    #print(restrição3(grid, quantRegras))

    formula_final = And(And(restrição1(grid, quantRegras), restrição2(grid, quantRegras)), restrição3(grid, quantRegras))
    print(formula_final)
    
    return False #print(formula_final)


# TESTE DE RESTRIÇÕES
teste = criarTabelaPacientes(arquivo1)
teste1 = restrição1(criarTabelaPacientes(arquivo1), quantRegras1)
teste2 = restrição2(criarTabelaPacientes(arquivo1), quantRegras1)
teste3 = restrição3(criarTabelaPacientes(arquivo1), quantRegras1)
teste4 = restrição4(criarTabelaPacientes(arquivo1), quantRegras1)
teste5 = restrição5(criarTabelaPacientes(arquivo1), quantRegras1)

#print(teste)
#print("")
#print(teste1)
#print("")
#print(teste2)
#print("")
print(teste3)
#print("")
#print(teste4)
#print("")
#print(teste5)
#print("")

solucaoTeste = solucao(criarTabelaPacientes(arquivo1), quantRegras1)
print(solucaoTeste)
