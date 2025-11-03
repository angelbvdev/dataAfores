import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set(style="whitegrid")

#1. Cargar datos
df = pd.read_csv("../2_cleaning/afore_limpio.csv")
df['fecha'] = pd.to_datetime(df['fecha'])

#2. Estadísticas generales
print("Estadísticas generales de rendimientos:")
print(df['rendimiento'].describe())

print("\nValores mínimos y máximos:")
print(f"Mínimo: {df['rendimiento'].min()}%")
print(f"Máximo: {df['rendimiento'].max()}%")
print(f"Promedio: {df['rendimiento'].mean():.2f}%")
print(f"Desviación estándar: {df['rendimiento'].std():.2f}%")

# 3. Análisis por año
df['año'] = df['fecha'].dt.year
df['mes'] = df['fecha'].dt.month

# Promedio anual
promedio_anual = df.groupby('año')['rendimiento'].mean()
print("\nPromedio anual de rendimientos:")
print(promedio_anual)

# Desviación estándar anual (volatilidad)
volatilidad_anual = df.groupby('año')['rendimiento'].std()
print("\nVolatilidad anual (std):")
print(volatilidad_anual)

#4. Meses destacados
# Mejor mes
mejor_mes = df.loc[df['rendimiento'].idxmax()]
print("\nMejor mes:")
print(mejor_mes[['fecha', 'rendimiento']])

# Peor mes
peor_mes = df.loc[df['rendimiento'].idxmin()]
print("\nPeor mes:")
print(peor_mes[['fecha', 'rendimiento']])

#5. Visualizaciones

# 5a. Evolución temporal
plt.figure(figsize=(14,6))
sns.lineplot(data=df, x='fecha', y='rendimiento')
plt.title("Evolución del rendimiento de AFORE (12 meses, promedio ponderado)")
plt.xlabel("Fecha")
plt.ylabel("Rendimiento (%)")
plt.show()

# 5b. Histograma de rendimientos
plt.figure(figsize=(10,5))
sns.histplot(df['rendimiento'], bins=50, kde=True)
plt.title("Distribución de los rendimientos")
plt.xlabel("Rendimiento (%)")
plt.ylabel("Frecuencia")
plt.show()

# 5c. Rendimiento promedio por año
plt.figure(figsize=(10,5))
sns.barplot(x=promedio_anual.index, y=promedio_anual.values, palette="Blues_d")
plt.title("Rendimiento promedio anual")
plt.xlabel("Año")
plt.ylabel("Rendimiento (%)")
plt.show()

# 5d. Volatilidad anual
plt.figure(figsize=(10,5))
sns.barplot(x=volatilidad_anual.index, y=volatilidad_anual.values, palette="Reds_d")
plt.title("Volatilidad anual de rendimientos")
plt.xlabel("Año")
plt.ylabel("Desviación estándar (%)")
plt.show()

# 5e. Heatmap de rendimientos por mes y año
pivot = df.pivot_table(index='mes', columns='año', values='rendimiento', aggfunc='mean')
plt.figure(figsize=(12,6))
sns.heatmap(pivot, annot=True, fmt=".2f", cmap="coolwarm")
plt.title("Rendimiento promedio por mes y año")
plt.xlabel("Año")
plt.ylabel("Mes")
plt.show()
