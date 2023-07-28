# %%
import pandas as pd
import numpy as np

import matplotlib.pyplot as plt
from matplotlib import colors
from matplotlib.ticker import PercentFormatter


# %%
# Carregar dados e e substituir espaços em branco por NaN

valores_vazios = [" "]
dados = pd.read_csv("flora_volks_dados.csv", sep = ";", na_values = valores_vazios)

# %%
#Resumo dos dados. Número de dados NaN.
display(dados)

print(dados.info())

#print(dados.isna().any())
print(dados.isna().sum())

#dados['Número'] = pd.to_numeric(dados['Número'],errors = 'coerce')

# %%
# Retirar espaços em branco no início e no fim das células

dados['autor'] = dados['autor'].str.strip()

# %%
display(dados)

# %%
# Excluir linhas sem dado de família
# 0 -> exclui linhas, 1 -> exclui colunas
dados_com_fam = dados.dropna(subset=['Família'], axis = 0)

# %%
#Excluir dados sem gênero
dados_com_gen = dados.dropna(subset=['Gênero'], axis = 0)
#display(dados_com_gen)
print(dados_com_gen.info())

# %%
#Adicionar 'sp.' nos gêneros sem espécies
dados_com_gen["sp"] = dados_com_gen["sp"].fillna('sp.')
print(dados_com_gen.info())

# %%
#Selecionanado linhas específicas para consultar Famílias
dados_com_gen.loc[dados_com_gen.Família == 'Amaranthaceae']

# %%
#Agrupar dados por Família, Gênero e espécie
dados_agrupados = dados_com_gen.groupby(['Família','Gênero','sp'])['sp'].count().reset_index(name='counts')
display(dados_agrupados)

# %%
#Agrupar famílias
grouped_fam = dados_agrupados.groupby(["Família"])['Família'].count().reset_index(name='counts')

grouped_fam['%'] = 100*grouped_fam['counts']/grouped_fam['counts'].sum()

# %%
print(grouped_fam)

# %%
# Gráfico da proporção de espécies por família
fig, ax = plt.subplots()

ax.bar(grouped_fam['Família'],grouped_fam['%'], width=1, edgecolor="white", linewidth=0.7, color='black')

ax.set(ylim=(0, 15), yticks=np.arange(1,15,2))

ax.set_ylabel('%')
ax.set_xlabel('Famílias')
ax.set_title('Proporção de espécies por famílias')

fig.set_size_inches(11, 4)

labels = ax.get_xticklabels()
plt.setp(labels, rotation=90, horizontalalignment='center')
plt.savefig('prop_familias', bbox_inches='tight')
plt.show()

# %%
#Histograma do número de espécies por família
fig, axs = plt.subplots()

axs.set_ylabel('Número de famílias')
axs.set_xlabel('Número de espécies')

axs.set(xlim=(0, 18), xticks=np.arange(1,18,1))

axs.hist(grouped_fam['counts'], bins=np.arange(1, 18, 1), color='black')
plt.savefig('hist_familia', bbox_inches='tight')

# %%
num_esp = grouped_fam['counts'].sum()
num_fam = grouped_fam['Família'].nunique()

# %%
#Agrupar gêneros
grouped_gen = dados_agrupados.groupby(["Gênero"])['Gênero'].count().reset_index(name='counts')
num_gen = grouped_gen['Gênero'].nunique()

# %%
print(f'Número de famílias: {num_fam}')
print(f'Número de espécies: {num_esp}')
print(f'Número de gêneros: {num_gen}')

# %%
print(grouped_gen)

# %%
#Histograma do número de espécies por gênero.
fig, axs = plt.subplots()

axs.set_ylabel('Número de gêneros')
axs.set_xlabel('Número de especies')

axs.hist(grouped_gen['counts'], bins=np.arange(1, 7, 1), color='black')

plt.savefig('hist_genero', bbox_inches='tight')

# %%
#Agrupar dados 'Família','Gênero','sp','Hábito','Origem','Substrato','Endemismo'
dados_agrupados2 = dados_com_gen.groupby(['Família','Gênero','sp','Hábito','Origem','Substrato','Endemismo'])['sp'].count().reset_index(name='counts')
display(dados_agrupados2)

# %%
display(dados_agrupados2['Hábito'].unique())

# %%
#Substituir alguns termos sobre hábito
sub = {'Erva, Subarbusto':'Subarbusto', 'Arbusto, Erva, Subarbusto':'Arbusto', 'Arbusto, Subarbusto':'Arbusto',
       'Arbusto,Árvore':'Árvore', 'Arbusto, Árvore, Subarbusto':'Árvore','Arbusto, Árvore':'Árvore','Arbusto, árvore':'Árvore',
       'Arbusto, subarbusto':'Arbusto', 'Liana/volúvel/trepadeira, Subarbusto':'Subarbusto','Liana/volúvel/trepadeira':'Liana'}
dados_agrupados2 = dados_agrupados2.replace(sub)

# %%
#Agrupar dados de hábito
grouped_hab = dados_agrupados2.groupby(['Hábito'])['sp'].count().reset_index(name='frequência')
display(dados_agrupados2['Hábito'].unique())
display(grouped_hab)

# %%
#Histogram com ocorrencia de hábitos
fig, axs = plt.subplots()

axs.set_ylabel('Número de espécies')
axs.set_xlabel('Hábito')

axs.bar(x=grouped_hab.Hábito, height=grouped_hab.frequência, color = 'black')

plt.savefig('hist_habito', bbox_inches='tight')

# %%
display(dados_agrupados2['Substrato'].unique())

# %%
#Substituir termos de substrato
sub = {'Rupícola,Terrícola':'Rupícola, Terrícola'}
dados_agrupados2 = dados_agrupados2.replace(sub)

# %%
#Agrupar dados de substrato
grouped_subs = dados_agrupados2.groupby(['Substrato'])['sp'].count().reset_index(name='frequência')
display(dados_agrupados2['Substrato'].unique())
display(grouped_subs)

# %%
#Histograma com dados de substratos
fig, axs = plt.subplots()

axs.set_ylabel('Número de espécies')
axs.set_xlabel('Substrato')

axs.bar(x=grouped_subs.Substrato, height=grouped_subs.frequência, color = 'black')
#axs.hist(dados_agrupados2['Hábito'], color='black')

plt.savefig('hist_substrato', bbox_inches='tight')

# %%
display(dados_agrupados2['Endemismo'].unique())

# %%
#Agrupar dados de endemismo
grouped_endem = dados_agrupados2.groupby(['Endemismo'])['sp'].count().reset_index(name='frequência')
display(dados_agrupados2['Endemismo'].unique())
display(grouped_endem)

# %%
#Histograma com dados de endemismos
fig, axs = plt.subplots()

axs.set_ylabel('Número de espécies')
axs.set_xlabel('Endemismo')

axs.bar(x=grouped_endem.Endemismo, height=grouped_endem.frequência, color = 'black')


plt.savefig('hist_endemismo', bbox_inches='tight')

# %%
display(dados_agrupados2['Origem'].unique())

# %%
#Agrupar dados de origem.
grouped_orig = dados_agrupados2.groupby(['Origem'])['sp'].count().reset_index(name='frequência')
display(grouped_orig)

# %%
#Histograma com dados de origem.
fig, axs = plt.subplots()

axs.set_ylabel('Número de espécies')
axs.set_xlabel('Origem')

axs.bar(x=grouped_orig.Origem, height=grouped_orig.frequência, color = 'black')

plt.savefig('hist_origem', bbox_inches='tight')