# VigiSalud-Benchmark 🏥

[![Python 3.11](https://img.shields.io/badge/Python-3.11-blue)](https://www.python.org/)
[![License: AGPL-3.0](https://img.shields.io/badge/License-AGPL--3.0-blue)](https://opensource.org/licenses/AGPL-3.0)
[![MAE Baseline](https://img.shields.io/badge/MAE_Baseline-7.2-brightgreen)](#-baseline-oficial)
[![Status: Active](https://img.shields.io/badge/Status-Active-success)](#)
[![Hardware: Moto G56](https://img.shields.io/badge/Hardware-Moto_G56_Termux-success)](#-hardware-compatible)

**Benchmark abierto para predicción de demanda en guardias médicas. Superá MAE 7.2.**

Desarrollado desde un **Moto G56 con Termux** para garantizar accesibilidad en entornos de salud pública con recursos limitados.

---

## 🚀 Quick Start

### 1. Clonar repositorio
```bash
git clone https://github.com/vigisalud-ai/vigisalud-benchmark.git
cd vigisalud-benchmark
```

### 2. Instalar dependencias (solo 3 paquetes)
```bash
pip install -r requirements.txt
```

### 3. Generar datos sintéticos basados en patrones reales
```bash
python generate_data.py
```

### 4. Ejecutar baseline oficial
```bash
python baseline.py
```

**Salida esperada:**
```
🏥 Generando datos sintéticos VigiSalud con feriados...
✅ Datos generados: 1095 días
📊 Consultas/día: avg=45.1, std=8.7
🎯 Feriados: 28 días
🏖️  Fines largos: 15 días

🧠 Entrenando baseline VigiSalud...
📊 Entrenando con 876 días...
✅ Baseline entrenado
🎯 MAE: 7.2 consultas/día
📈 Train: 876 días, Test: 219 días
💡 ¿Superás 7.2? ¡Envía tu modelo!
```

---

## 📊 Baseline Oficial

| Métrica | Valor | Objetivo Real en Producción |
|---------|-------|----------------------------|
| **MAE Baseline** | 7.2 consultas/día | **7-10 consultas/día** |
| **Modelo** | Random Forest (100 árboles) | - |
| **Features** | 12 variables temporales + feriados | - |
| **Período** | 3 años sintéticos (2023-2025) | - |
| **Split** | Temporal 80/20 (no shuffle) | - |

> ⚠️ **Nota importante:** El MAE 7.2 con datos sintéticos es **consistente con el objetivo de producción de 7-10 consultas/día**. Datos reales típicamente tienen más variabilidad.

### Configuración del Baseline
```python
from sklearn.ensemble import RandomForestRegressor

model = RandomForestRegressor(
    n_estimators=100,
    max_depth=10,
    random_state=42,        # Para reproducibilidad
    n_jobs=-1              # Usar todos los cores disponibles
)
```

---

## 🎯 Cómo Participar

### Paso 1: Entrenar tu modelo
```bash
# Clona el repositorio y modifica baseline.py o crea tu propio script
python tu_modelo.py
```

### Paso 2: Evaluar contra el baseline
```python
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

# Cargar datos de test (últimos 20% - temporal split)
test_data = pd.read_csv("data/synthetic.csv")
split_idx = int(len(test_data) * 0.8)
test_data = test_data.iloc[split_idx:]

# Definir features (12 en total)
features = [
    'dia_semana', 'mes', 'es_fin_de_semana', 'es_verano', 
    'es_invierno', 'trimestre', 'dia_del_anio', 'semana_del_anio',
    'es_feriado', 'es_fin_largo', 'dia_despues_feriado', 'dia_antes_feriado'
]

# Generar predicciones
y_true = test_data['target_7d']
y_pred = tu_modelo.predict(test_data[features])

# Calcular métricas
mae = mean_absolute_error(y_true, y_pred)
rmse = mean_squared_error(y_true, y_pred, squared=False)
r2 = r2_score(y_true, y_pred)

print(f"MAE:  {mae:.2f} consultas/día")
print(f"RMSE: {rmse:.2f}")
print(f"R²:   {r2:.4f}")
print(f"\n✅ Baseline: 7.2 | Tu modelo: {mae:.2f}")
```

### Paso 3: Enviar Pull Request
Si superás **MAE 7.2**, envía un PR con:
- ✅ Código del modelo (limpio y documentado)
- ✅ Métricas de evaluación (MAE, RMSE, R²)
- ✅ Hardware utilizado y tiempo de entrenamiento
- ✅ Descripción breve de la estrategia
- ✅ Archivo `results.json` con métricas

**Formato de results.json:**
```json
{
  "model_name": "Mi Modelo XGBoost",
  "author": "Tu Nombre",
  "hardware": "Moto G56 + Termux",
  "training_time_seconds": 45.3,
  "metrics": {
    "mae": 6.85,
    "rmse": 8.12,
    "r2": 0.876
  },
  "features_used": 12,
  "notes": "Agregué normalización y tuning de hiperparámetros"
}
```

---

## 📁 Estructura del Repositorio

```
vigisalud-benchmark/
├── data/
│   ├── synthetic.csv           # Datos sintéticos (3 años, 1095 registros)
│   └── README_data.md          # Diccionario de variables
├── src/
│   ├── generate_data.py        # Generador de datos sintéticos
│   ├── baseline.py             # Modelo baseline oficial (Random Forest)
│   └── utils.py                # Funciones auxiliares de evaluación
├── results/
│   ├── baseline_results.json   # Métricas del baseline
│   └── leaderboard.md          # Ranking de modelos (actualizado)
├── requirements.txt            # Dependencias (pandas, scikit-learn, numpy)
├── LICENSE                     # AGPL-3.0
└── README.md                   # Este archivo
```

---

## 🔬 Dataset Sintético

### Características Generales
| Aspecto | Detalle |
|---------|---------|
| **Período** | 2023-01-01 a 2025-12-31 (3 años completos) |
| **Frecuencia** | Diaria (1,095 registros) |
| **Rango de valores** | 10-80 consultas/día |
| **Media** | ~45 consultas/día |
| **Desviación estándar** | ~12.3 consultas/día (con feriados) |

### Variables (12 Features + 1 Target)

#### Features Temporales (12)
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `dia_semana` | int | Lunes=0, Domingo=6 |
| `mes` | int | Mes del año (1-12) |
| `es_fin_de_semana` | bool | 1 si sábado/domingo |
| `es_verano` | bool | 1 si Dic-Feb (hemisferio sur) |
| `es_invierno` | bool | 1 si Jun-Ago |
| `trimestre` | int | Trimestre del año (1-4) |
| `dia_del_anio` | int | Día del año (1-365) |
| `semana_del_anio` | int | Semana ISO del año (1-52) |
| `es_feriado` | bool | 1 si es feriado oficial |
| `es_fin_largo` | bool | 1 si es fin de semana largo |
| `dia_despues_feriado` | bool | 1 si es día después de feriado |
| `dia_antes_feriado` | bool | 1 si es día antes de feriado |

#### Target (1)
| Variable | Tipo | Descripción |
|----------|------|-------------|
| `target_7d` | int | Promedio de consultas en próximos 7 días |

### Patrones Incluidos

```python
# Patrón semanal
- Viernes: +25% (mayor accidentabilidad)
- Lunes: -15% (menor demanda inicial)
- Feriados: -60% (solo urgencias reales)
- Fines largos: -30% (demanda extendida)

# Patrón estacional
- Verano: -10% (menos consultas)
- Invierno: +5% (más consultas)

# Efectos feriados
- Día antes feriado: -15% (preparativos)
- Día después feriado: +20% (acumulación)
```

### Validación de Datos
```python
# Cargar y validar
import pandas as pd

df = pd.read_csv("data/synthetic.csv")
print(f"Registros: {len(df)}")           # Debe ser 1095
print(f"Columnas: {len(df.columns)}")    # Debe ser 13
print(df.info())                         # Verificar tipos
print(df.describe())                     # Estadísticas
```

---

## 🏗️ Filosofía del Proyecto

| Principio | Implementación | Por qué importa |
|-----------|----------------|-----------------|
| **Realismo** | MAE 7.2 vs objetivo producción 7-10 | Métricas honestas y alcanzables |
| **KISS** | 3 scripts, 1 CSV, 3 dependencias | Accesible para cualquier profesional |
| **Accesibilidad** | Corre en Moto G56 + Termux | Llegar a hospitales con recursos limitados |
| **Transparencia** | Random Forest interpretable | Médicos deben confiar en predicciones |
| **Impacto real** | Basado en experiencia clínica real | Soluciones que funcionan en terreno |

---

## 📊 Contexto Clínico Real

**MAE 7.2 significa:**
- En una guardia de 45 consultas/día: **~16% de error**
- **Clínicamente aceptable** para planificación de turnos
- **Realista** para datos con alta variabilidad natural
- **Desafiante pero alcanzable** para investigadores

**Objetivo de producción: 7-10 consultas/día**
- Basado en experiencia real con datos mixtos
- Considera variabilidad de entornos hospitalarios reales
- Incluye factores impredecibles de la práctica clínica

---

## 📊 Performance Benchmarks

### Hardware de Referencia

| Sistema | RAM | Tiempo Entrenamiento | Versión Python |
|---------|-----|---------------------|-----------------|
| Moto G56 (Termux) | 8GB | ~120s | 3.11 |
| Manjaro Linux (i5-10210U) | 8GB | ~5s | 3.11 |
| Colab Free Tier | 12GB | ~2s | 3.11 |

**Nota:** El objetivo es que cualquier modelo pueda entrenar en menos de 5 minutos.

---

## 🔒 Seguridad y Ética

- ✅ **Datos 100% sintéticos:** No contiene información de pacientes reales
- ✅ **Anonimización completa:** Patrones basados en estadísticas agregadas
- ✅ **Compatible con RGPD/Ley 25.326:** No requiere comités de ética para uso
- ✅ **Transparencia algorítmica:** Modelos interpretables, no cajas negras
- ✅ **Licencia abierta:** AGPL-3.0 asegura que mejoras vuelvan a la comunidad

---

## 📄 Licencia

**GNU Affero General Public License v3 (AGPL-3.0)**

### ¿Qué significa AGPL v3 para este proyecto?

**Filosofía:** Software para salud pública debe mantenerse público, accesible y mejorado colaborativamente.

- **Puedes:** Usar, modificar, distribuir libremente
- **Debes:** Mantener la licencia AGPL-3.0 en derivados
- **Responsabilidad:** Si ofreces el software como servicio, debes compartir el código fuente
- **Garantía:** Sin garantías; úsalo bajo tu responsabilidad

Ver archivo [LICENSE](LICENSE) para términos completos.

---

## 🤝 Contribuciones

### ¿Quién puede contribuir?

- 👨‍⚕️ **Médicos y profesionales de salud** - Validar patrones, sugerir mejoras clínicas
- 🧠 **Investigadores en IA/ML** - Nuevos algoritmos, optimizaciones
- 💻 **Desarrolladores** - Refactoring, tests, documentación
- 🏥 **Administradores hospitalarios** - Feedback de implementación real
- 📊 **Data scientists** - Feature engineering, análisis exploratorio

### Proceso de Contribución

1. **Discutir primero** - Para cambios grandes, abre una Issue
2. **Seguir el formato** - Código limpio, docstrings en español/inglés
3. **Mantener compatibilidad** - Debe funcionar en Moto G56 (Termux)
4. **Incluir tests** - Validar nuevas funcionalidades
5. **Documentar cambios** - Actualizar README y CHANGELOG

### Checklist para PR
- [ ] Código formateado (Black, 88 caracteres)
- [ ] Tests pasando (`pytest`)
- [ ] Docstrings completos
- [ ] README actualizado
- [ ] `results.json` con métricas

---

## 📞 Contacto y Soporte

### Canales de Comunicación

| Canal | Uso | Tiempo Respuesta |
|-------|-----|-----------------|
| **Issues en GitHub** | Bugs, features, preguntas técnicas | 48-72h |
| **Discussions** | Discusiones generales, feedback | 1 semana |
| **Email** | Implementación en hospitales | 24-48h |
| **Twitter/X** | Updates y noticias | N/A |

**Reportar un bug:**
```markdown
## Descripción
[Qué pasó]

## Pasos para reproducir
1. ...
2. ...

## Comportamiento esperado
[Qué debería pasar]

## Sistema
- OS: [Linux/macOS/Windows]
- Python: 3.11
- Hardware: [Moto G56/Laptop/Cloud]
```

---

## 📚 Citar este Benchmark

### En trabajos académicos (BibTeX)
```bibtex
@software{vigisalud_benchmark_2026,
  title     = {VigiSalud-Benchmark: Open Benchmark for Healthcare Demand Prediction},
  author    = {López, Héctor},
  year      = {2026},
  publisher = {GitHub},
  url       = {https://github.com/vigisalud-ai/vigisalud-benchmark},
  note      = {Baseline MAE: 7.2 consultas/día, AGPL-3.0 License}
}
```

### En artículos (APA)
López, H. (2026). VigiSalud-Benchmark: Open benchmark for healthcare demand prediction [Software]. GitHub. https://github.com/vigisalud-ai/vigisalud-benchmark

---

## 🏥 Ecosistema Relacionado

### Proyectos del Mismo Autor

| Proyecto | Descripción | Licencia | Estado |
|----------|-------------|---------|--------|
| **[VigiSalud](https://github.com/vigisalud-ai/vigisalud)** | Sistema principal de predicción con dashboard | MIT | Activo |
| **[Argentina Hub](https://github.com/hectory2k/argentina-hub)** | Capa de datos públicos argentinos + Censo 2022 | AGPL-3.0 + CC-BY | Activo |
| **[VigiSalud-Benchmark](https://github.com/vigisalud-ai/vigisalud-benchmark)** | Este benchmark (estandarización) | AGPL-3.0 | Activo |
| **[Odysseus](https://github.com/hectory2k/odysseus)** | Stack local de RAG + embeddings | MIT | Mantenido |

### Integraciones Compatibles

- 🐘 **PostgreSQL/Supabase** - Para datos productivos
- 🚀 **GitHub Actions** - CI/CD automático
- 📊 **Telegram** - Alertas de predicción
- 🤖 **Ollama** - Modelos locales para narrativas clínicas

---

## ⭐ ¿Por qué participar?

### No es solo un logro técnico

Superar **MAE 7.2** contribuye a:

- 🏥 **Mejor planificación de recursos** en guardias médicas
- ⏱️ **Reducción de tiempos de espera** para pacientes
- 💰 **Uso más eficiente del presupuesto** sanitario
- 🧑‍⚕️ **Condiciones de trabajo más predecibles** para personal
- 📈 **Investigación abierta** en sistemas de salud

### Reconocimiento

- Tu nombre en el leaderboard
- Co-autoría en papers (si corresponde)
- Soporte para implementación hospitalaria
- Acceso anticipado a nuevas features

---

## 🧪 Testing y Validación

### Ejecutar tests
```bash
pytest tests/ -v --cov=src
```

### Coverage mínimo
- ✅ Generate data: 95%+
- ✅ Baseline model: 90%+
- ✅ Utils: 85%+

---

## 📋 FAQ

**P: ¿Qué versión de Python necesito?**
R: Python 3.11+. Verificá con `python --version`

**P: ¿Mi modelo puede usar librerías externas?**
R: Sí, pero debe estar documentado en requirements.txt. Preferimos modelos que corran en hardware básico.

**P: ¿Los datos cambiarán?**
R: La versión 1.0 es estable. Nuevas versiones tendrán compatibilidad hacia atrás.

**P: ¿Puedo usar datos reales?**
R: No en este benchmark. Este es sintético por privacidad. Para datos reales, contactanos directamente.

**P: ¿Hay dinero involucrado?**
R: No. Este es un proyecto colaborativo sin ánimo de lucro.

---

## 📈 Roadmap

### v1.0 (Actual)
- ✅ Baseline Random Forest
- ✅ Dataset sintético realista con feriados
- ✅ Documentación completa

### v1.1 (Próximo)
- 🔄 Integración con datos reales de Las Lomitas (anonimizados)
- 🔄 Leaderboard dinámico
- 🔄 Análisis de importancia de features

### v2.0 (Futuro)
- 🔮 Predicción multi-paso temporal
- 🔮 Subregiones diferentes
- 🔮 Integración con VigiSalud dashboard oficial

---

## 💪 Créditos

**Desarrollado por:** Héctor López  
**Institución:** Distrito Sanitario N°2, Las Lomitas, Formosa  

---

**¿Tu modelo es mejor? ¡Podría estar ayudando a salvar vidas! 🚀**

Envía tu PR hoy: [vigisalud-benchmark/pulls](https://github.com/vigisalud-ai/vigisalud-benchmark/pulls)
