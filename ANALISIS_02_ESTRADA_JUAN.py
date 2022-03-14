#%%
import pandas as pd
import seaborn as sns

#%%
#Rutas de importación y exportación
sldb = pd.read_csv('synergy_logistics_database.csv', index_col=0, parse_dates=[5])
rutas = sldb.groupby(['direction','origin', 'destination', 'transport_mode'])
suma = rutas.sum()['total_value']
rutas = rutas['total_value'].describe()

rutas['suma_total'] = suma
rutas = rutas.reset_index()

exportaciones = rutas[ rutas['direction'] == 'Exports']
importaciones = rutas[rutas['direction'] == 'Imports']

#funcion de export y import
def sol1(df, top=10):
    suma_total_df = df['suma_total'].sum()
    most_used = df.sort_values(by='count', ascending=False).head(top)
    suma_total_top = most_used.suma_total.sum()

    total_usos = most_used['count'].sum()
    porcentaje = (suma_total_top / suma_total_df) * 10000
    porcentaje = int(porcentaje) / 100
    print(f'Las {top} rutas mas demandadas aportan {porcentaje}% de las ganancias, en un total de {total_usos} servicios')
    return most_used

#%%
#Resultado de rutas de exportación
print('El caso de las 10 rutas más usadas de Exportación es: ')
grafica_export = sol1(exportaciones)
grafica_export

#%%
#Resultado de rutas de exportación 
print('El caso de las 10 rutas más usadas de Importación es: ')
grafica_import = sol1(importaciones)
grafica_import

# %%
#Medio de trasporte utilizado
#Grafica de barras
sldb = pd.read_csv('synergy_logistics_database.csv', index_col=0, parse_dates=[5])
ax = sns.countplot(x='transport_mode', data=sldb)

# %%
#Medio de trasporte utilizado
#Grafica con la variación por año 

transportes_anuales = sldb.groupby(by=['year', 'transport_mode'])
valor_anual_transporte = transportes_anuales['total_value'].agg(pd.Series.sum)

info_transp_anual = pd.DataFrame()
info_transp_anual['valor_total'] = valor_anual_transporte
info_transp_anual['frecuencia'] = transportes_anuales['total_value'].describe()['count']

sns.lineplot(x='year', y='frecuencia', hue='transport_mode', data=info_transp_anual)

# %%
#Valor total de importaciones y exportaciones.
#Porcentajes de ganancias de exportaciones.
print('Países por porcentaje de ganancia en exportación: ')
sldb = pd.read_csv('synergy_logistics_database.csv', index_col=0, parse_dates=[5])
datos = sldb[ sldb['direction'] == 'Exports' ][['origin', 'total_value']]
suma = datos.groupby('origin').sum()
cuenta = datos.groupby('origin').count()
lista = suma.reset_index()
lista = lista.merge(cuenta, left_on='origin', right_index=True)
cols = {'total_value_x':'valor', 'total_value_y':'cant. servicios'}
lista = lista.rename(columns=cols)
lista['porcentaje'] = (lista['valor'] / lista['valor'].sum()) * 100
lista = lista.sort_values(by='valor', ascending=False)
lista['porcentaje acum.'] = lista.cumsum()['porcentaje']
lista

# %%
#Valor total de importaciones y exportaciones.
#Porcentajes de ganancias de importaciones.
print('Países por porcentaje de ganancia en importación: ')
datos = sldb[ sldb['direction'] == 'Imports' ][['origin', 'total_value']]
suma = datos.groupby('origin').sum()
cuenta = datos.groupby('origin').count()
lista = suma.reset_index()
lista = lista.merge(cuenta, left_on='origin', right_index=True)
cols = {'total_value_x':'valor', 'total_value_y':'cant. servicios'}
lista = lista.rename(columns=cols)
lista['porcentaje'] = (lista['valor'] / lista['valor'].sum()) * 100
lista = lista.sort_values(by='valor', ascending=False)
lista['porcentaje acum.'] = lista.cumsum()['porcentaje']
lista
# %%
