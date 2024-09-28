'''
Formação de Carteira FII

Objetivo: Montar uma carteira de investimentos em fundos imobiliários através da análise 
combinatória de multiplos ativos, obter uma seleção que possua o menor custo de aquisição (preço) e
maior retorno (Dividend Yield).
    
'''
# In[Instalar os pacotes]

!pip install pandas
!pip install matplotlib
!pip install seaborn
!pip install selenium
!pip install tqdm

# In[Biliotecas Utilizadas]
# https://selenium-python.readthedocs.io/

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import math
from tqdm import tqdm
from itertools import combinations
from selenium import webdriver
from selenium.webdriver.common.by import By


# In[Web scraping]

# Ler o código dos fundos listados no IFIX
df_fundos = pd.read_csv('IFIXDia_16-09-24.csv')

# Inicializa as variavéis que serão salvas
df_fundos['price'] = None
df_fundos['sector'] = None
df_fundos['marketCap'] = None
df_fundos['dividendRate'] = None

# define o drive de busca que será o google chrome
driver =  webdriver.Chrome()

# Itera sobre cada fundo realizando uma busca no site fundamentos e obtem as informações
for i in df_fundos["TICKER"]:
    
    try:    
        driver.get(f"https://www.fundamentus.com.br/detalhes.php?papel={i}")
        
        # Scraping dos dados desejados
        price = driver.find_elements(By.CLASS_NAME, 'txt')[3].text.replace(",", ".")
        setor = driver.find_elements(By.CLASS_NAME, 'txt')[13].text
        marketCap = driver.find_elements(By.CLASS_NAME, 'txt')[21].text.replace(".","")
        dividendRate = driver.find_elements(By.CLASS_NAME, 'txt')[39].text.replace(",", ".")

        # Salvar os dados no dataframe
        df_fundos.loc[df_fundos['TICKER'] == i, "price"] = price
        df_fundos.loc[df_fundos['TICKER'] == i, "sector"] = setor
        df_fundos.loc[df_fundos['TICKER'] == i, "marketCap"] =  marketCap
        df_fundos.loc[df_fundos['TICKER'] == i, "dividendRate"] = dividendRate
        
        print(f'Obtendo os dados do fundo: {i}')

    except:
        print(f'Erro ao obter os dados do fundo imobiliário: {i}')

driver.quit()

# In[Limpeza]

# Identificando valores ausentes
df_fundos.isnull().sum()

# O fundo imobiliário "CYCR11" não possui dados no site
# logo iremos exlui-lo do registro.
df_fundos[df_fundos['price'].isna()]

# Remover a linha de ativos sem valores
df_fundos_limpo = df_fundos.dropna()
df_fundos_limpo.isnull().sum()        

# Total de ativos por segmento
total_fundos_setor = df_fundos_limpo['sector'].value_counts().sort_values(ascending=False)
total_fundos_setor

# Identificando segmento vazio
df_fundos_limpo[df_fundos_limpo['sector'] == ""]

# O fundo "CACR11" não possui segmento especificado na plataforma
# logo iremos preencher o valor do setor  de atuação como "ausente"
df_fundos_limpo['sector'].replace("", "ausente", inplace=True)
df_fundos_limpo

# total de ativos por segmento
total_fundos_setor = df_fundos_limpo['sector'].value_counts().sort_values(ascending=False)
total_fundos_setor

# tipagem dos dados
df_fundos_limpo['price'] = df_fundos_limpo['price'].astype("float64")
df_fundos_limpo['marketCap'] = df_fundos_limpo['marketCap'].astype('float64')
df_fundos_limpo['dividendRate'] = df_fundos_limpo['dividendRate'].astype('float64')

# In[Estatísticas Descritivas]

# informações do conjunto de dados
df_fundos_limpo.info()

# descrição univariada dos fundos imobiliários
df_fundos_limpo.describe()

# frequencia do preco
df_fundos_limpo['price'].hist()
plt.title('Freq. de preço')
plt.xlabel('preço')
plt.ylabel('contagem')
plt.show()

# frequecia Market Cap
df_fundos_limpo['marketCap'].hist(bins=20)
plt.title('Freq, Market Cap')
plt.xlabel('marketCap')
plt.ylabel('Contagem')
plt.grid(True, alpha=0.3)
plt.show()

# Frequência dividendRate
df_fundos_limpo['dividendRate'].hist(bins=20)
plt.title('Freq. Dividend Rate')
plt.xlabel('dividendRate')
plt.ylabel('Contagem')
plt.grid(True, alpha=0.3)
plt.show()

sns.heatmap(df_fundos_limpo[['price', 'marketCap', 'dividendRate']].corr(), annot=True)
plt.title('Correlation')
plt.show()

# In[Seleção de ativos]

# Considerar para a combinação apenas ativos com valor patrimonial acima de 500 milhoes.
df_fundos_limpo_2 = df_fundos_limpo[df_fundos_limpo['marketCap'] >= 500000000.00]
df_fundos_limpo_2

# In[Total de combinações]

ticker_list = df_fundos_limpo_2['TICKER'].tolist()
combinacoes = 5

n = len(ticker_list)

def combinations_count(n, k):
    return math.comb(n, k)

total_combinations = combinations_count(n, combinacoes)

print(f"Total de combinações de {combinacoes} elementos -> total ativos({n}), combinacoes:({total_combinations:,})")

# In[Executando as combinações]

ticker_list = df_fundos_limpo_2['TICKER'].tolist()
price_list = df_fundos_limpo_2['price'].tolist()
dividendo_list = df_fundos_limpo_2['dividendRate'].tolist()

ticker_to_price = dict(zip(ticker_list, price_list))
ticker_to_dividendo = dict(zip(ticker_list, dividendo_list))

n = len(ticker_list)

# Calcular o número total de combinações para 5 elementos
def combinations_count(n, k):
    return math.comb(n, k)

total_combinations = combinations_count(n, 5)

# Inicializar variáveis para armazenar a melhor combinação
melhor_comb = None
melhor_preco_total = float('inf')  # Inicialmente infinito para garantir que qualquer preço será menor
melhor_rendimento = float('-inf')  # Inicialmente negativo infinito para garantir que qualquer rendimento será maior
melhor_dividendo = float('inf')

# Gerar combinações de 5 elementos
__combination = combinations(ticker_list, 5)

# Usar tqdm para criar a barra de progresso
for idx, combination in enumerate(tqdm(__combination, total=total_combinations, desc="Processando combinações")):

    # Calcular o total de preços para a combinação atual
    total_price = sum(ticker_to_price[ticker] for ticker in combination)

    # Calcular o total dos últimos dividendos para a combinação atual
    total_dividendo = sum(ticker_to_dividendo[ticker] for ticker in combination)

    # Calcular o rendimento como percentual
    rendimento = (total_dividendo / total_price * 100) if total_price != 0 else 0

    # Verificar se a combinação atual deve substituir a melhor combinação
    if (total_price < melhor_preco_total) and (rendimento > melhor_rendimento):
        melhor_comb = combination
        melhor_preco_total = total_price
        melhor_rendimento = rendimento
        melhor_dividendo = total_dividendo


print("Melhor Combinação Final:")
print(f"Combinação: {melhor_comb}")
print(f"Total de Preços: {melhor_preco_total:.2f}")
print(f"Total de Rendimento Bruto: {melhor_dividendo:.2f}")
print(f"Rendimento: {melhor_rendimento:.2f}%")
