import numpy as np
import skfuzzy as fuzz
import matplotlib.pyplot as plt
from skfuzzy import control as ctrl


#Definindo as variáveis do Sistema
temperatura = ctrl.Antecedent(np.arange(15, 30, 45), 'temperatura')
preco = ctrl.Antecedent(np.arange(1, 3.5, 4), 'preco')
consumo = ctrl.Consequent(np.arange(500, 6000, 8000), 'consumo')

# Definindo as funções de pertinencia para a temperatura
temperatura['baixa'] = fuzz.gaussmf(temperatura.universe, [6.395, 15])
temperatura['media'] = fuzz.gaussmf(temperatura.universe, 6.395,30)
temperatura['alta'] = fuzz.gaussmf(temperatura.universe, [6.369,45])

#Definindo as funções de pertinência para o preço
preco['baixo'] = fuzz.gaussmf(preco.universe, [1.061,1])
preco['médio'] = fuzz.gaussmf(preco.universe, [1.061, 3.05])
preco['alto'] = fuzz.gaussmf(preco.universe, [1.061, 3.05])

# Definindo as funções de pertinência de saída para o consumo
consumo['pequeno'] = fuzz.gaussmf(consumo.universe, [-2250, 500])
consumo['médio'] = fuzz.gaussmf(consumo.universe, [500, 3250])
consumo['grande'] = fuzz.gaussmf(consumo.universe, [3250,6000])

# Base de Conhecimento/Regras
rule1 = ctrl.Rule(temperatura['baixa'] & preco['baixo'], consumo['grande'])
rule2 = ctrl.Rule(temperatura['baixa'] & preco['médio'], consumo['médio'])
rule3 = ctrl.Rule(temperatura['baixa'] & preco['alto'], consumo ['pequeno'])
rule4 = ctrl.Rule(temperatura['media'] & preco['baixo'], consumo['grande'])
rule5 = ctrl.Rule(temperatura['media'] & preco['baixo'], consumo ['grande'])
rule6 = ctrl.Rule(temperatura['media'] & preco['alto'], consumo['pequeno'])
rule7 = ctrl.Rule(temperatura['alta'] & preco['baixo'], consumo['grande'])
rule8 = ctrl.Rule(temperatura['alta'] & preco['médio'], consumo['médio'])
rule9 = ctrl.Rule(temperatura['alta'] & preco['alto'], consumo['pequeno'])

# Sistema Fuzzy e Simulação
consumo_ctrl = ctrl.ControlSystem([rule1, rule2, rule3, rule4, rule5, rule6, rule7, rule8, rule9])
consumo_simulador = ctrl.ControlSystemSimulation(consumo_ctrl)


# Entranda da temperatura
while True:
  temp = float(input('Digite a Temperatura em ºC: '))
  if(temp<15 or temp >45):
    print('A temperatura deve estar entre 15º a 45º')
    continue
  consumo_simulador.input['temperatura'] = temp
  break

# Entrada do preço 
while True:
  valor = float(input('Digite o Preço em R$: '))
  if(valor<1 or valor>3.5):
    print('O Preço deve ser maior que 1R$ e menor que 3.5R$')
    continue
  consumo_simulador.input['preco'] = valor
  break

# Validando os resultados da Inferência Fuzzy e da  Defuzzificação
consumo_simulador.compute()
print('O Consumo é de %d ' % round(consumo_simulador.output['consumo']))


