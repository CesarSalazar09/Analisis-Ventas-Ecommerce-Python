import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv('data.csv', encoding='latin1')
print("Primeras 5 filas del dataset")
print(df.head(5))

print("Información sobre el dataset")
print(df.info())

print("Estadisticas")
print(df.describe())

# 1. Manejar valores nulos
#Los pedidos sin Costumer ID puede ser de invitados. Para un análisis de clientes, lo eliminaremos.
df.dropna(subset=['CustomerID'],inplace=True)
#2. Corregir tipo de datos
#Convertir la columna de fecha a formato datetime
df['InvoiceDate']=pd.to_datetime(df['InvoiceDate'])
#Convertir CustomerID a tipo string para evitar se tratado como número
df['CustomerID']=df['CustomerID'].astype(int)
df['CustomerID']=df['CustomerID'].astype(str)

#3.Crear nuevas columnas
df['TotalPrice']=df['Quantity']*df['UnitPrice']
df['Hour']=df['InvoiceDate'].dt.hour
df['Month']=df['InvoiceDate'].dt.month
df['DayofWeek']=df['InvoiceDate'].dt.day_name()

#4. Limpiar datos negativos
df=df[df['Quantity']>0]

print("Datos limpios y con nuevas columnas")
print(df.head(40))

#Análisis y visualización
#Pregunta 1: ¿Cuáles son los 10 productos más vendidos?
df_producto_mas_vendidos = df.groupby('Description')['Quantity'].sum().sort_values(ascending=False).head(10)
print(df_producto_mas_vendidos)
plt.figure(figsize=(12, 6))
df_producto_mas_vendidos.plot(kind='barh',color='skyblue')
plt.title("Top 10 productos más vendidos")
plt.xlabel("Cantidad vendida")
plt.ylabel("Producto")
plt.gca().invert_yaxis()
plt.show()

#Pregunta 2: ¿En qué meses se vende más?
df_ventas_por_mes = df.groupby('Month')['TotalPrice'].sum()
print(df_ventas_por_mes)
plt.figure(figsize=(10,5))
df_ventas_por_mes.plot(kind='line',marker='o', color='green')
for index, value in df_ventas_por_mes.items():
    label=f'{int(value):,}'
    plt.text(index,value,' '+label, va='center')

plt.title("Ventas por mes")
plt.xlabel("Mes")
plt.ylabel("Ingresos Totales")
plt.xticks(ticks=np.arange(1, 13), labels=['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
plt.grid(True)
plt.show()

#Pregunta 3: ¿De qué países provienen nuestros clientes?
df_paises= df.groupby('Country')['CustomerID'].nunique().sort_values(ascending=False).head(10)
print(df_paises)
plt.figure(figsize=(12, 6))
df_paises.plot(kind='bar', color='lightcoral')
plt.title("Número de clientes por país")
plt.xlabel("País")
plt.ylabel("Número de clientes")
plt.xticks(rotation=45)
plt.show()



