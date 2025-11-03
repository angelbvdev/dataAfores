import pandas as pd

# 1. Cargar el dataset
df = pd.read_csv("../1_data/10_rendimientos_precio_bolsa.csv")  

# 2. Convertir tipos de datos
df['fecha'] = pd.to_datetime(df['fecha'], errors='coerce')

# Renombrar columna 'monto' a 'rendimiento'
df.rename(columns={'monto': 'rendimiento'}, inplace=True)

# 3. Revisar valores faltantes
print("Valores nulos por columna:")
print(df.isnull().sum())

# Eliminar filas con fecha o rendimiento faltante
df = df.dropna(subset=['fecha', 'rendimiento'])

# 4. Eliminar duplicados
print(f"Duplicados encontrados: {df.duplicated().sum()}")
df = df.drop_duplicates()

# 5. Estandarizar texto
# Eliminar espacios al inicio/final y pasar a minúsculas
df['afore'] = df['afore'].str.strip().str.lower()
df['tipo_recurso'] = df['tipo_recurso'].str.strip().str.lower()
df['plazo'] = df['plazo'].str.strip().str.lower()

# Revisar valores únicos
print("AFOREs únicos:", df['afore'].unique())
print("Tipos de recurso únicos:", df['tipo_recurso'].unique())
print("Plazos únicos:", df['plazo'].unique())


# 6. Guardar el dataset limpio
df.to_csv("afore_limpio.csv", index=False)
print("Dataset limpio guardado como 'afore_limpio.csv'")

# 7. Resumen final
print("Resumen del dataset limpio:")
print(df.describe())
