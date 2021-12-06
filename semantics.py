from formula import *
from functions import atoms


# VERIFICAR O VALOR VERDADE DA FORMULA COM TAL INTERPRETAÇÃO  
def truth_value(formula, interpretation):
    
    if isinstance(formula, Atom): # se a fórmula seja uma atomica
        for formulaArray in interpretation: # Percorrer o array de interpretações parciais
            if f'{formula}' == f'{formulaArray[0]}': # Se tal atomica estiver na interpretação
                return formulaArray[1] # Retornar a sua interpretação parcial

    elif isinstance(formula, Not): # se a fórmula possui o operador NOT
        if truth_value(formula.inner, interpretation) == True or truth_value(formula.inner, interpretation) == False: # Caso a formula dentro do not for True ou False
            return not truth_value(formula.inner, interpretation) # retornar a valoração contrária
        
    elif isinstance(formula, And): # se a fórmula possui o operador binário AND
        if truth_value(formula.left, interpretation) == False or truth_value(formula.right, interpretation) == False: # Caso pelo menos uma das duas formulas for False
            return False # Retornar False
        
        else: # Se não
            return True # Retornar True
  
    elif isinstance(formula, Or): # se a fórmula possui o operador binário OR
        if truth_value(formula.left, interpretation) == True or truth_value(formula.right, interpretation) == True: # Caso pelo menos uma das duas formulas for True
            return True # Retornar True
        
        else: # Se não
            return False # Retornar False
 
    elif isinstance(formula, Implies): # se a fórmula possui o operador binário Implies
        if truth_value(formula.left, interpretation) == False or truth_value(formula.right, interpretation) == True: # Caso pelo menos a formula da esquerda for False ou a formula da direita for True
            return True # Retornar True
        
        else: # Se não
            return False # Retornar False


# VERIFICAR A SATISFABILIDADE DE FORMA BRUTA
def satisfiability_brute_force(formula):

    list_atoms = atoms(formula) # Lista das atomicas da formula
    interpretation_parcial = [] # Interpretação parcial (caso possua)
    lista_sem_valoracao = [] # Lista para guardar as atomicas que estao na interpretação parcial
                    
    for interpretacao in interpretation_parcial: # for para percorrer a interpretação parcial
        lista_sem_valoracao.append(interpretacao[0]) # acrescentar o primeiro elemento de interpretacao a lista_sem_valoracao
    
    list_atoms = remove_atoms(list_atoms, lista_sem_valoracao) # remover as atomicas que ja possuem valoracao de list_atoms

    return sat(formula, list_atoms, interpretation_parcial) # retornar a função sat


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
        

# REMOVER ATOMICAS QUE JA POSSUEM INTERPRETAÇÃO PARCIAL DA LIST_ATOMS  
def remove_atoms(list_atoms, interpretation_parcial):
    
    lista_atoms_nao_removidos = [] # lista para guardar as atomicas não removidas
    
    for linha in list_atoms: # percorrer os elementos da list_atoms
        if str(linha) not in interpretation_parcial: # se o elemento não estiver na interpretation_parcial
            lista_atoms_nao_removidos.append(linha) # acrescentar elemento na lista_atoms_nao_removidos
              
    return lista_atoms_nao_removidos # retornar lista_atoms_removidos


# CONVERTER FORMULAS EM ANDs UTILIZANDO DE EQUIVALENCIA LÓGICA
def conversor(formula):
    
    if isinstance(formula, Atom): # se a fórmula seja uma atomica 
        return formula # retornar formula
    
    elif isinstance(formula, Not): # se a fórmula possui o operador NOT
        if isinstance(formula.inner, Atom): # se a formula dentro da negação for um ATOM
            return formula # retornar formula
        
        else: # se não
            formula = conversor(formula.inner) # chamar de forma recursiva a função conversor para a formula dentro da negação
            return formula # retornar formula
    
    elif isinstance(formula, And): # se a fórmula possui o operador binário AND
        formula = And(conversor(formula.left), conversor(formula.right)) # chamar de forma recursiva a função conversor para a formula da esquerda e da direita
    
    elif isinstance(formula, Or): # se a fórmula possui o operador binário OR
        formula = Not(And(Not(conversor(formula.left)), Not(conversor(formula.right)))) # chamar de forma recursiva a função conversor para a formula da esquerda e da direita evidenciando a propriedade -(A AND B) = (-A OR -B)

    elif isinstance(formula, Implies): # se a fórmula possui o operador binário Implies
        formula_parcial = Or(Not(conversor(formula.left)), conversor(formula.right)) # chamar de forma recursiva a função conversor para a formula da esquerda e da direita evidenciando a propriedade (A -> B) = (-A OR B)
        formula = conversor(formula_parcial) # # chamar de forma recursiva a função conversor para a formula_parcial evidenciando a propriedade -(A AND B) = (-A OR -B)
    
    return formula # retornar formula


# SIMPLIFICADOR DE NOT
def simplificador_de_not(formula):
    
    if isinstance(formula, Atom): # se a fórmula seja uma atomica 
        return formula # retornar fórmula
    
    elif isinstance(formula, Not): # se a fórmula possui o operador NOT
        if isinstance(formula.inner, Not): # se a formula dentro da negação for outra negação
            formula = simplificador_de_not(formula.inner.inner) # chamar de forma recursiva a função simplificador_de_not da formula dentro da negação
            return formula # retornar fórmula
        
        else:
            formula = Not(simplificador_de_not(formula.inner)) # chamar de forma recursiva a negação da função simplificador_de_not da formula dentro da negação
            return formula # retornar fórmula
    
    elif isinstance(formula, And) or isinstance(formula, Or) or isinstance(formula, Implies): # Se a formula possuir qualquer operador binário
        formula.left = simplificador_de_not(formula.left) # chamar de forma recursiva a função simplificador_de_not para a formula da esquerda
        formula.right = simplificador_de_not(formula.right) # chamar de forma recursiva a função simplificador_de_not para a formula da direita
        
    return formula # retornar fórmula
