from formula import *
from functions import atoms


# VERIFICAR O VALOR VERDADE DA FORMULA COM TAL INTERPRETAÇÃO  
def truth_value(formula, interpretation):
    
    if isinstance(formula, Atom): # Verificar se a fórmula é uma atomica
        for formulaArray in interpretation: # Percorrer o array de interpretações parciais
            if f'{formula}' == f'{formulaArray[0]}': # Se tal atomica estiver na interpretação
                return formulaArray[1] # Retornar a sua interpretação parcial

    elif isinstance(formula, Not):
        if truth_value(formula.inner, interpretation) == True or truth_value(formula.inner, interpretation) == False:
            return not truth_value(formula.inner, interpretation)
        
    elif isinstance(formula, And):
        if truth_value(formula.left, interpretation) == False or truth_value(formula.right, interpretation) == False:
            return False
        
        else:
            return True
  
    elif isinstance(formula, Or):
        if truth_value(formula.left, interpretation) == True or truth_value(formula.right, interpretation) == True:
            return True
        
        else:
            return False
 
    elif isinstance(formula, Implies): # Verificar se a fórmula possui o operador binário Implies
        if truth_value(formula.left, interpretation) == False or truth_value(formula.right, interpretation) == True:
            return True
        
        else:
            return False


# VERIFICAR A SATISFABILIDADE DE FORMA BRUTA
def satisfiability_brute_force(formula):

    """
    interpretation_parcial = 
    [
        ['X_PI <= 42.09_1_p', False], ['X_PI <= 42.09_1_n', True], ['X_PI <= 42.09_1_s', False], ['X_PI <= 42.09_2_p', False], 
        ['X_PI <= 42.09_2_n', False], ['X_PI <= 42.09_2_s', True], ['X_PI <= 70.62_1_p', True], ['X_PI <= 70.62_1_n', False], 
        ['X_PI <= 70.62_1_s', False], ['X_PI <= 70.62_2_p', False], ['X_PI <= 70.62_2_n', False], ['X_PI <= 70.62_2_s', True], 
        ['X_GS <= 37.89_1_p', False], ['X_GS <= 37.89_1_n', False], ['X_GS <= 37.89_1_s', True], ['X_GS <= 37.89_2_p', False], 
        ['X_GS <= 37.89_2_n', True], ['X_GS <= 37.89_2_s', False], ['C_1_1', False], ['C_1_2', True], ['C_2_1', True], ['C_2_2', True]
    ]
    """

    list_atoms = atoms(formula) # Lista das atomicas da formula
    interpretation_parcial = []
    vetorA = []
                    
    for interpretacao in interpretation_parcial:
        vetorA.append(interpretacao[0])
    
    list_atoms = remove_atoms(list_atoms, vetorA)

    return sat(formula, list_atoms, interpretation_parcial)


# VERIFICAR AS POSSIBILIDADES DE SATISFABILIDADE
def sat(formula, list_atoms, interpretation_parcial):

    copia_list_atoms = list_atoms.copy() # copia da list atoms para ser alterada na chamada recursiva
    
    if list_atoms == []: # se list_atoms é um conjunto vazio
        if truth_value(formula, interpretation_parcial): # Caso o valor da interpretação seja verdadeiro
            lista_true = [] # lista auxiliar para coletar somente os valores true
            for array in interpretation_parcial: # for para percorrer a interpretação
                if array[-1] == True: # se o ultimo valor da linha for True
                    lista_true.append(array[0]) # acrescentar o primeiro valor à lista_true

            return lista_true # Retornar a interpretação so com os valores verdadeiros
        
        else: # Caso o valor da interpretação seja falso       
            return False # Retornar False
    
    atomica_removida = copia_list_atoms.pop() # remoção do ultimo elemento da copia da list_atoms
    
    interpretacao1 = interpretation_parcial + [[atomica_removida, True]] # interpretação1 da atomica removida com a valoracao True
    interpretacao2 = interpretation_parcial + [[atomica_removida, False]] # interpretação2 da atomica removida com a valoracao False
    
    resultado = sat(formula, copia_list_atoms, interpretacao1) # chamada recursiva para a primeira interpretação
    
    if resultado != False: # caso a chamada recursiva da primeira interpretação seja diferente de False
        return resultado # retornar resultado
    
    else: # se não
        resultado1 = sat(formula, copia_list_atoms, interpretacao2) # chamada recursiva para a segunda interpretação
        
        if resultado1 != False: # caso a chamada recursiva da segunda interpretação seja diferente de False
            return resultado1 # retornar resultado1
        
        else:
            return False # retornar False
            

"""def teste(formula, interpretation):
    
    if isinstance(formula, Atom):       
        interpretation.append([str(formula), True]) 
    
    elif isinstance(formula, Not):
        if isinstance(formula.inner, Atom):
            interpretation.append([str(formula.inner), False])
            
        else:
           teste(formula.inner, interpretation)

    elif isinstance(formula, And) or isinstance(formula, Or) or isinstance(formula, Implies):
        teste(formula.left, interpretation)
        teste(formula.right, interpretation)
    
    return sorted(list(interpretation))"""
        

# REMOVER ATOMICAS QUE JA POSSUEM INTERPRETAÇÃO PARCIAL DA LIST_ATOMS  
def remove_atoms(list_atoms, interpretation_parcial):
    
    lista_atoms_removidos = []
    
    for linha in list_atoms: # percorrer os elementos da list_atoms
        if str(linha) not in interpretation_parcial: # se o elemento não estiver na interpretation_parcial
            lista_atoms_removidos.append(linha) # acrescentar elemento na lista_atoms_removidos
              
    return lista_atoms_removidos # retornar lista_atoms_removidos


def conversor(formula):
    
    if isinstance(formula, Atom):
        return formula
    
    elif isinstance(formula, Not):
        if isinstance(formula.inner, Atom):
            return formula
        
        else:
            formula = conversor(formula.inner)
            return formula
    
    elif isinstance(formula, And):
        formula = And(conversor(formula.left), conversor(formula.right))
    
    elif isinstance(formula, Or):
        formula = Not(And(Not(conversor(formula.left)), Not(conversor(formula.right))))

    elif isinstance(formula, Implies):
        formulaParcial = Or(Not(conversor(formula.left)), conversor(formula.right))
        formula = conversor(formulaParcial)
    
    return formula


def simplificador_de_not(formula):
    
    if isinstance(formula, Atom):
        return formula
    
    elif isinstance(formula, Not):
        if isinstance(formula.inner, Not):
            formula = simplificador_de_not(formula.inner.inner)
            return formula
        
        else:
            formula = Not(simplificador_de_not(formula.inner))
            return formula
    
    elif isinstance(formula, And) or isinstance(formula, Or) or isinstance(formula, Implies):
        formula.left = simplificador_de_not(formula.left)
        formula.right = simplificador_de_not(formula.right)
        
    return formula
