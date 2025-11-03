import pandas as pd

# Cargar dataset
df = pd.read_csv("10_rendimientos_precio_bolsa.csv") 

# Ver las primeras filas
print(df.head())

# Revisar info de columnas
print(df.info())

# Estadísticas básicas
print(df.describe())
