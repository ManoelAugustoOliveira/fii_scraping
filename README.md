# Formação de Carteira FII

Objetivo: Montar uma carteira de investimentos em fundos imobiliários através da análise 
combinatória de multiplos ativos, obter uma seleção que possua o menor custo de aquisição (price)
com o maior retorno (Dividend Yield) através da combinação de n ativos.

Fonte: Será realizado um processo de Web scraping no site https://www.fundamentus.com.br buscando
por fundos imobiliários que compõem o IFIX (Índice de Fundos de Investimento Imobiliários)

## Metodologia
### Fórmula das Combinações:

A fórmula usada para calcular o número de **combinações** é a seguinte:


$$ C(n, k) = \frac{n!}{k!(n-k)!} $$

Onde:
- **C(n, k)** é o número de combinações possíveis de **n** elementos tomados **k** a cada vez.
- **n** é o número total de elementos.
- **k** é o número de elementos escolhidos por combinação.
- **!** (fatorial) significa o produto de todos os números inteiros positivos até esse número. Por exemplo, 5! = 5 × 4 × 3 × 2 × 1 = 120.

Por exemplo, se você tem 115 ativos e deseja selecionar subconjuntos de 5 ativos para compor diferentes carteiras de investimentos, a fórmula será:


$$ C(115, 5) = \frac{115!}{5!(115-5)!} = \frac{115!}{5!110!} $$

Isso retorna o número total de combinações possíveis.

### Resultados obtidos no exemplo:
- **Combinação**: ('BCFF11', 'CPTS11', 'DEVA11', 'RBRF11', 'VGHF11')
- **Total de Preços**: 70.35
- **Total de Rendimento Bruto**: 11.38
- **Rentabilidade anual**: 16.18%

### Disclaimer:
Este projeto tem como foco **demonstrar técnicas de análise combinatória** e **otimização de carteiras de investimento**. As informações fornecidas não constituem aconselhamento financeiro e **não garantem rendimentos futuros**. A decisão de realizar investimentos deve ser baseada em análises detalhadas, preferencialmente com o auxílio de um consultor financeiro certificado.

### Limitações:
1. **Complexidade Computacional**:
    - A análise combinatória pode resultar em **números extremamente grandes de combinações** conforme o tamanho da lista de ativos aumenta. Isso pode causar problemas de desempenho e **demora na execução**.
    - Para conjuntos muito grandes de dados, o processo pode **demorar bastante** ou até mesmo exceder a memória disponível do sistema.​

