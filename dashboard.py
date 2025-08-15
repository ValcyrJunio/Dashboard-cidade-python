# Importar bibliotecas
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os


# Carregar os Dados


caminho_pedidos = "olist_orders_dataset.csv"
caminho_clientes = "olist_customers_dataset.csv"
caminho_itens = "olist_order_items_dataset.csv"

try:
    df_pedidos = pd.read_csv(caminho_pedidos)
    df_clientes = pd.read_csv(caminho_clientes)
    df_itens = pd.read_csv(caminho_itens)
    print("\nArquivos lidos com sucesso!")
except FileNotFoundError as e:
    print(f"\n Erro ao ler arquivos: {e}")
    print("Verifique se os arquivos estão na mesma pasta do seu script.")
    exit()


# União dos dataframes


df_completo = pd.merge(df_pedidos, df_clientes, on='customer_id', how='left')
df_completo = pd.merge(df_completo, df_itens, on='order_id', how='left')

print("\n=== DataFrames unidos ===")
print(df_completo.info())

#Defini a pasta de destino e o nome do arquivo
pasta_destino = "Analises feitas"
nome_arquivo = "Analise.png"

caminho_completo = os.path.join(pasta_destino, nome_arquivo)

#Cria a pasta se ela não existir
os.makedirs(pasta_destino, exist_ok =True)



# Cria a figura e os eixos

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(18, 8)) 
plt.style.use('seaborn-v0_8-darkgrid')

# TOP 10 CIDADES
print("\nGerando Gráfico 1: Top 10 Cidades com Mais Pedidos")
if 'customer_city' in df_completo.columns:
    pedidos_por_cidade = df_completo['customer_city'].value_counts().head(10)
    sns.barplot(x=pedidos_por_cidade.index, y=pedidos_por_cidade.values, palette='viridis', ax=ax1)
    ax1.tick_params(axis='x', rotation=45)
    ax1.set_title("Top 10 Cidades com Mais Pedidos")
    ax1.set_xlabel("Cidade")
    ax1.set_ylabel("Número de Pedidos")
else:
    print("A coluna 'customer_city' não foi encontrada.")

# RÁFICO 2: DISTRIBUIÇÃO DOS VALORES 
print("\nGerando Gráfico 2: Distribuição do Valor Total dos Pedidos")
if 'price' in df_completo.columns:
    valores_pedidos = df_completo.groupby('order_id')['price'].sum()
    sns.histplot(valores_pedidos, bins=50, kde=True, ax=ax2)
    ax2.set_title('Distribuição do Valor Total dos Pedidos')
    ax2.set_xlabel('Valor do Pedido (R$)')
    ax2.set_ylabel('Frequência')
else:
    print(" A coluna 'price' não foi encontrada.")



plt.tight_layout()
plt.savefig(caminho_completo) # Salva os gráficos em um arquivo .png
plt.show()

print(f"Gráfico salvo em: {caminho_completo}")
