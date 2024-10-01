import requests
import pandas as pd

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

# INSTANCIA AAPL
api_key = '70f5d7b2d3b80682f0f157c8d097955d'
stock = 'NVDA'
start_date = '2022-11-10'
end_date = '2023-10-10'

# Hacemos uso de la función y llamamos los datos
historical_data = get_historical_prices(stock, start_date, end_date, api_key) # Utilizar función con AAPL

# Creamos el Data Frame
historical_data['r_i'] = historical_data['adjClose'].pct_change()
historical_data.head(10)

#----------------------------TAREA--------------------------
# Sacar info. de 1 año para 5 acciones
# Mis acciones serán: NVDA, TSLA, T, ORCL, & VZ

# Aplicar función a dichas acciones
api_key = 'nfnDS1BFxH2hqtKXHRralrV26dionWf6'
start_date = '2022-11-10'
end_date = '2023-11-10'

acciones = ['NVDA', 'TSLA', 'T', 'ORCL', 'VZ'] # Hacer arreglo de acciones para ejecutar código más rápido

combined_data = pd.DataFrame()

# Fetch and combine historical data for all stocks
for stock in acciones:
    historical_data = get_historical_prices(stock, start_date, end_date, api_key)
    if not historical_data.empty:
        historical_data.rename(columns={'adjClose': stock}, inplace=True) # Renombrar adjClose como el nombre de la accion
        historical_data[f'return_{stock}'] = historical_data[stock].pct_change() # Calcular retornos de cada acción
        combined_data = pd.concat([combined_data, historical_data], axis=1)

#combined_data = combined_data[acciones, 'returns'] # Escoger columnas que nos interesan (los adjClose de cada una de las acciones)
combined_data.head()
peso = 1/len(acciones)

return_columns = [f'return_{stock}' for stock in acciones]

combined_data = combined_data[acciones + return_columns] # Seleccionar columnas de interés (adjClose y returns de cada acción)
combined_data.head()

for stock in acciones:
  #combined_data[f'Rp_{stock}'] = combined_data[f'return_{stock}'] * peso
  combined_data['Rp'] = peso* sum(combined_data[f'return_{stock}'] for stock in acciones)

combined_data.head()
