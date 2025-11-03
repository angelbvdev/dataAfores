Predicción de Rendimientos de AFOREs - Dashboard Interactivo

Este proyecto es un **dashboard interactivo** que permite visualizar y predecir los rendimientos anuales de las AFOREs en México. El objetivo es mostrar un flujo completo de un proyecto de **Data Science**, desde la limpieza de datos hasta la predicción y visualización interactiva.

---

**Estructura del proyecto**

* `1_data_preparation.py` : Limpieza y agregación de datos
* `2_train_predict.py` : Entrenamiento del modelo y predicción
* `3_dashboard.py` : Dashboard interactivo con Dash
* `afore_limpio.csv` : Dataset original limpio
* `afore_anual.csv` : Dataset anual preparado
* `rf_afore_model.pkl` : Modelo entrenado (Random Forest)
* `encoder_afore.pkl` : Encoder para AFOREs
* `README.md` : Documentación del proyecto

---

**Descripción de los scripts**

1. `data_preparation.py`

   * Limpia y prepara el dataset original (`afore_limpio.csv`).
   * Convierte fechas a formato `datetime` y agrega columnas de año y mes.
   * Calcula rendimiento promedio anual por AFORE y guarda `afore_anual.csv`.

2. `train_predict.py`

   * Entrena un **Random Forest Regressor** para predecir el rendimiento anual de cada AFORE.
   * Codifica las AFOREs con **One-Hot Encoding**.
   * Evalúa el modelo usando **Mean Squared Error (MSE)**.
   * Permite predecir rendimientos para un año futuro.
   * Guarda el **modelo entrenado** y el **encoder** (`.pkl`).

3. `dashboard.py`

   * Dashboard interactivo hecho con **Dash**.
   * Permite seleccionar un año y mostrar predicciones de rendimiento de todas las AFOREs.
   * Muestra un **gráfico de barras interactivo** y un mensaje indicando cuál AFORE tendría el mayor rendimiento.

---

**Funcionalidades**

* Limpieza y preparación de datos de AFOREs.
* Visualización de rendimientos históricos (opcional).
* Entrenamiento de modelo de predicción (Random Forest).
* Predicción de rendimientos futuros para un año específico.
* Dashboard interactivo para explorar predicciones de forma visual.

---

**Requisitos**

* Python ≥ 3.9
* Librerías:

  * pandas
  * numpy
  * matplotlib
  * seaborn
  * scikit-learn
  * plotly
  * dash
  * joblib

Se instalan con:

```bash
pip install pandas numpy matplotlib seaborn scikit-learn plotly dash joblib
```

---

**Cómo ejecutar**

1. Preparar los datos:

```bash
python 1_data_preparation.py
```

2. Entrenar el modelo y generar predicciones:

```bash
python 2_train_predict.py
```

3. Ejecutar el dashboard interactivo:

```bash
python 3_dashboard.py
```

* Abrirá un servidor local en el navegador (por defecto `http://127.0.0.1:8050`).

---

**Limitaciones**

* El modelo actual predice principalmente basado en históricos y no considera factores macroeconómicos como tasas de interés, inflación o volatilidad de mercado.
* Para años futuros, las posiciones de las AFOREs tienden a mantenerse similares al histórico.
* Este proyecto es un ejemplo de pipeline de Data Science y dashboard interactivo, ideal para principiantes.

---

**Mejoras futuras**

* Incorporar series temporales y tendencias históricas por AFORE.
* Agregar variables externas como inflación, tasas de interés o rendimiento del IPC.
* Usar modelos de series temporales como **Prophet, ARIMA o LSTM** para predicciones más realistas.
* Visualizar históricos de rendimiento junto con predicciones en el dashboard.

---

**Autor**

* Angel Burgos
* Proyecto de portafolio en Data Science / Machine Learning
