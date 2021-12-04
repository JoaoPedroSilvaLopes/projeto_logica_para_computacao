# Esse arquivo se baseia em exemplificar as instruções passadas pelo
# professor no PDF Tema dos Projetos para facilitar o entendimento.
#
# -------------RESUMO DOCUMENTO: Temas dos Projetos - Lógica para Computação.pdf-----------------
# O projeto se baseia em encontrar soluções através dos dados ao
# invés de seguir instruções.
#
# * A temática do projeto é aprender um conjunto de regras para identificar
# patologias da coluna vertebral.
#
# * Existem pacientes com patologia e paciente sem patologias chamados de normais.
#
# Existem as informações que cada paciente deve possuir, que são:
# - Ângulo de incidência pélvica (PI)
# - Ângulo de versão pélvica (PT)
# - Ângulo de lordose (LA)
# - Inclinação sacral (SS)
# - Raio Pélvico (RP)
# - Grau de deslizamento (GS)
#
# * Os dados estarao em vários arquivos e cada arquivo possui informações descritas acima
# sobre os pacientes. E cada arquivo contém colunas com intervalos de valores dessas
# informações.
#
# OBS1: Cada coluna é chamada de ATRIBUTO!
# OBS2: Os nomes dos arquivos são do formato column_bin_<f>a_<n>p.csv, em que <f>
# é a quantidade atributos e <n> é a quantidade de pacientes dentro arquivo.
#
# EXEMPLO: no arquivo column_bin_5a_3p.csv se espera que tenha 5 atributos e 3 pacientes,
# e o mesmo será representado da seguinte forma:
#
# PI <= 42.09; PI <= 70.62; PI <= 80.61; GS <= 37.89; GS <= 57.55; P
# 0          ; 0          ; 1          ; 0          ; 1          ; 1
# 0          ; 0          ; 0          ; 0          ; 0          ; 1
# 0          ; 0          ; 0          ; 1          ; 1          ; 0
#
# * Analisando o exemplo nota-se que o paciente 1 foi diagnosticado com patologia,
# o paciente 2 tambem foi diagnosticado com patologia e o paciente 3 não foi, logo o mesmo
# é considerado normal. Com esses resultados podemos criar um conjunto de regras em que cada
# regra é referida a um tipo de informação, ou seja, com esse exemplo podemos extrair 2 regras:
# - [PI <= 80.61, PI > 70.62] => P (Possui patologia)
# - [GS > 57.55] => P (Possui patologia)
#
# * Portanto com os dados do arquivo .csv seria possível determinar um conjunto de regras que
# possa identificar um paciente com ou sem patologia.
#
# Então o conjunto de regras deve se aplicar a todos os pacientes com patologia e não devem
# ser aplicadas em nenhum paciente normal.
#
# * Obtenção de conjunto de regras: A aplicação deverá ter como parâmetros um número natural m
# maior que zero que representa a quantidade de regras e um arquivo column_bin_<f>a_<n>p.csv.
# Então a aplicação deverá determinar se existe um conjunto de m regras para classificar os
# pacientes de forma correta a partir das entradas.
#
# OBS3: Caso exista a aplicação deverá apresentar o conjunto de regras e caso não exista a
# aplicação indicar dizer essa inexistencia.
#
# * DICAS: Usar variáveis atômicas
# - Xa,i,p
# - Xa,i,n
# - Xa,i,s
# - Ci,j
#
# Em que 'a' é um atributo,
# Em que 'i' é um natural com 1 <= i <= m, que representa a i-ésima regra.
# Em que 'j' é um natural com 1 <= j <= n, em que n representa a quantidade de pacientes.
#
# Durante a modelagem as atômicas seguirão os seguintes significados:
# - v(Xa,i,p) = é True (T) se e somente se o atributo 'a' ocorre positivamente na regra 'i'
# - v(Xa,i,n) = é True (T) se e somente se o atributo 'a' ocorre negativamente na regra 'i'
# - v(Xa,i,s) = é True (T) se o atributo 'a' não aparece na regra 'i'
# - v(Ci,j) = é True (T) se a regra 'i' cobre o paciente 'j', ou seja, quando a 'i' se aplica a 'j'
#
# * RESTRIÇÕES: com o arquivo column_bin_<f>a_<n>p.csv e o natural m, se deve construir restrições
# da aprendizagem de regras utilizando uma fórmula da lógica proposicional com as atômicas citadas
# anteriormente. Serão cinco restrições:
# - Primeira restrição: Para cada atributo e regra existem 3 possibilidades.
# O atributo aparece positivamente na regra, o atributo aparece negativamente na regra
# ou o atributo não aparece na regra.
#
# - Segunda restrição: Cada regra deve possuir algum atributo aparecendo na mesma.
#
# - Terceira restrição: Para cada paciente sem patologia e regra, algum atributo do paciente não
# pode ser aplicado à regra.
#
# - Quarta restrição: Para cada paciente com patologia, regra e atributo. Se o atributo do
# paciente não se aplicar ao da regra, então a regra não cobre esta paciente.
#
# - Quinta restrição: Cada paciente com patologia deve ser cobrido com alguma das regras.
#
# * Após obter as regras, deve-se verificar se o conjunto de regras consegue classificar
# corretamente todos os indivíduos do arquivo. Cada paciente deve receber um diagnóstico
# baseado na utilização das regras. Após isso, deve-se verificar se o diagnóstico bate com
# o diagnóstico do arquivo.


#-------------------------ALTERAÇÕES DO REPOSITÓRIO SEMANA 01-------------------------------

"""
COMMIT DIA - 11/11/2021
- Inserção de metas para serem cumpridas durante a semana no READ ME
- Inserção de arquivos necessários que o professor disponibilizou para o projeto prático da etapa 1, não inserindo os arquivos que se tratam logica proposicional de primeira ordem
- Conclusão de algumas funções
- Consertar Função: significa que a mesma esta funcionando, mas não em todos os casos necessários
- Implementar Função: significa que a mesma não esta funcionando ou nem foi iniciada
- Foco em utilizar os conceitos de equivalencia lógica para transformar as formulas em fórmulas que só possuam a negação e o operador binário AND
para que facilite a detecção de satisfabilidade

COMMIT DIA - 13/11/2021
- Implementações das funções: number_of_atoms, is_clause, is_negation_normal_form, is_cnf, substitution

COMMIT DIA - 22/11/2021
- Implementações das funções: is_term, is_dnf, truth_value

COMMIT DIA - 25/11/2021
- Adicionar de arquivos .csv dos dados dos pacientes
- Implementação da função criarTabelaPacientes: serve para ler os dados do arquivo .csv e criar um grid com os dados
- Implementação das funções and_all e or_all: para criar grande formulas com OR's e AND's
- Implementação das funções restrição1, restrição2 e restrição5: serve para criar as devidas restrições para a criação da grande formula dos dados dos pacientes
- A fazer restrição4 e restrição5: ainda falta completar as outras duas restrições para a criação da grande formula dos dados dos pacientes
- Implementação de conversor para AND e simplificador de NOT (função facultativa)

COMMIT DIA - 28/11/2021
- Implementação da criação das regras com a função solucao(arquivo, quantRegras) na pasta projeto1.py
- Implementação da função satisfiability_brute_force(formula) na pasta semantics.py
- Implementação da função sat(formula, list_atoms, interpretation_parcial) na pasta semantics.py
- Implementação da função de remove_atoms(list_atoms, interpretation_parcial) na pasta semantics.py

COMMIT DIA 29/11/2021
- Implementação da função laudarPacientes(lista_final_de_regras, grid_pacientes, linha_atributos, valores_dados, quantRegras) na pasta projeto1.py
- Implementação de uma função propria para criar as regras chamada de criar_regras(lista_parcial, quantRegras) na pasta projeto1.py
- Alterações no README baseado na alterações
- Exclusão da pasta main (pois estava sem utilidade)
- Inserção de comentários adicionais e organização do codigo como um todo

COMMIT DIA 04/12/2021
- Alterações e melhorias em algumas funções como: restrições 1, 2, 3, 4 e 5, solucao e laudarPacientes
- Adição de comentários adicionais
"""