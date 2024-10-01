import requests
import pandas as pd
from IPython.display import display


# Función
def get_historical_prices(stock, start_date, end_date, api_key):
    url = f'https://financialmodelingprep.com/api/v3/historical-price-full/{stock}?from={start_date}&to={end_date}&apikey={api_key}'
    response = requests.get(url)
    data = response.json()
    historical_prices = data.get('historical', [])
    historical_prices = pd.DataFrame(historical_prices) # Para que convierta a DF

    historical_prices = pd.DataFrame(historical_prices).set_index('date')
    historical_prices.index = pd.to_datetime(historical_prices.index, format='%Y-%m-%d')
    historical_prices.index.name = 'date' # Poner como índice las fechas

    historical_prices.sort_index(ascending=True, inplace=True) # Ordenar de forma ascendente

    return historical_prices

# Sacar info. de 1 año para 15 acciones
# Mis acciones serán: 'NVDA', 'INTC', 'PLTR', 'TSLA', 'AAPL', 'BBD', 'T', 'WBD', 'SOFI', 'NIO', 'SNAP', 'BTG', 'F', 'AAL', 'BAC'

# Aplicar función a dichas acciones
api_key = '70f5d7b2d3b80682f0f157c8d097955d'
start_date = '2022-11-10'
end_date = '2023-11-10'

# Hacer arreglo de acciones para ejecutar código más rápido
acciones = acciones = ['NVDA', 'INTC', 'PLTR', 'TSLA', 'AAPL', 'BBD', 'T', 'WBD', 'SOFI', 'NIO', 'SNAP', 'BTG', 'F', 'AAL', 'BAC']


# Inicializar los DataFrames para precios ajustados, volúmenes & returns
precios = pd.DataFrame()
volumen = pd.DataFrame()
returns = pd.DataFrame()

# Iterar sobre cada acción para obtener los datos históricos
for stock in acciones:
    historical_data = get_historical_prices(stock, start_date, end_date, api_key)
    if not historical_data.empty:
        # Procesar datos de precios ajustados
        precios_data = historical_data[['adjClose']].rename(columns={'adjClose': stock}) # Extraer precios ajustados
        precios = pd.concat([precios, precios_data], axis=1)

        # Procesar datos de volumen
        volumen_data = historical_data[['volume']].rename(columns={'volume': f'vol_{stock}'}) # Extraer volumen de la df
        volumen = pd.concat([volumen, volumen_data], axis=1)

        # Procesar datos returns
        returns_data = historical_data[['adjClose']].pct_change().rename(columns={'adjClose': f'return_{stock}'}) #Definir returns
        returns = pd.concat([returns, returns_data], axis=1)

# Mostrar las primeras filas de cada DataFrame para verificar
print("DataFrame de precios ajustados:")
display(precios.head())

#print("\nDataFrame de volúmenes:")
display(volumen.head())

print("\nDataFrame de returns:")
display(returns.head())

# Definir pesos ponderado por el volumen
# Se necesita hacer una nueva columna en el df de volumen en el que haya una suma del volumen por cada día
suma1 = volumen.iloc[0,:].sum() # Hacer la 1era suma
print("Suma1: ", suma1)


# Definir df para pesos de cada acción ponderada por el volumen
# En el 1er caso, el peso es igual al volumen de cada acción entre la suma total de los volúmenes de dicho día
# A partir de ahí, el peso de hoy es el peso de ayer multiplicado por el rendimiento de hoy
pesos = pd.DataFrame(index=returns.index, columns=returns.columns)

for i in range(len(returns)):
    if i == 0:
        # Para el primer día, calcular pesos como volumen/suma1
        pesos.iloc[i, :] = volumen.iloc[i, :] / suma1
    else:
        # Para los días siguientes, calcular pesos como peso anterior * retorno
        pesos.iloc[i, :] = pesos.iloc[i-1, :] * (1 + returns.iloc[i, :])

# Mostrar resultados
pesos.columns = acciones
print("\n-------------PESOS MATRIX-------------\n")
display(pesos.head())

# Definir vector transpuesto de la serie de tiempo con el peso del portafolio por día
serie_tiempo = pd.DataFrame(index=returns.index)
serie_tiempo['Rp'] = pesos.sum(axis=1)
display(serie_tiempo.head())

# Sacar de la serie de pesos del portafolio, el rendimiento del portafolio
ret_port = serie_tiempo.pct_change()
ret_port.columns = ['return_portfolio'] # Renombrar columna para entendimiento
display(ret_port.head())

# Si la base de la inversión es 1000, entonces nuestro retorno del portafolio sería:
ret_port['return_portfolio'] = serie_tiempo['Rp'] * 1000
display(ret_port.head())
