#!/usr/bin/env python3
"""
Baseline oficial de VigiSalud-Benchmark.
Random Forest con MAE ~4.0.
Ahora con features de feriados.
"""

import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error

def main():
    print("🧠 Entrenando baseline VigiSalud con feriados...")

    # Cargar datos
    df = pd.read_csv("data/synthetic.csv")
    df['fecha'] = pd.to_datetime(df['fecha'])

    # NUEVAS FEATURES con feriados (16 total)
    features = [
        'dia_semana', 'mes', 'es_fin_de_semana',
        'es_verano', 'es_invierno', 'trimestre',
        'dia_del_anio', 'semana_del_anio',
        'es_feriado', 'es_asueto_imprevisto',  # ✅ Nuevas
        'es_fin_largo', 'dia_despues_feriado', # ✅ Nuevas
        'dia_antes_feriado',                   # ✅ Nuevas
        'densidad_poblacion', 'porcentaje_mayores_65'
    ]

    # Split temporal (80/20) - ¡NO shuffle para series temporales!
    split_idx = int(len(df) * 0.8)
    train = df.iloc[:split_idx].copy()
    test = df.iloc[split_idx:].copy()

    # Modelo baseline (mismos hyperparameters)
    model = RandomForestRegressor(
        n_estimators=100,
        max_depth=10,
        random_state=42,
        n_jobs=-1
    )

    print(f"📊 Entrenando con {len(train)} días y {len(features)} features...")
    model.fit(train[features], train['target_7d'])

    # Evaluación
    preds = model.predict(test[features])
    mae = mean_absolute_error(test['target_7d'], preds)

    # Mostrar importancia de features (opcional pero útil)
    importancias = model.feature_importances_
    print("\n📈 Importancia de features (top 5):")
    for i, idx in enumerate(np.argsort(importancias)[-5:][::-1]):
        print(f"   {i+1}. {features[idx]}: {importancias[idx]:.3f}")

    print(f"\n✅ Baseline entrenado")
    print(f"🎯 MAE: {mae:.1f} consultas/día")
    print(f"📊 Train: {len(train)} días, Test: {len(test)} días")
    print(f"🔧 Features: {len(features)} variables")
    print(f"💡 ¿Superás {mae:.1f}? ¡Envía tu modelo!")

if __name__ == "__main__":
    main()
