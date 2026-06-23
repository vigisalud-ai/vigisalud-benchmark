#!/usr/bin/env python3
"""
Generador de datos sintéticos para VigiSalud-Benchmark.
Incluye feriados, fines largos y asuetos variables.
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta

class FeriadosArgentinos:
    """Manejador de feriados argentinos (fijos y trasladables)."""

    @staticmethod
    def get_feriados_anio(anio):
        """Devuelve todos los feriados de un año con manejo de fines largos."""
        feriados_fijos = [
            # Feriados fijos
            datetime(anio, 1, 1),    # Año Nuevo
            datetime(anio, 5, 1),     # Día del Trabajo
            datetime(anio, 5, 25),    # Día de la Revolución de Mayo
            datetime(anio, 7, 9),     # Día de la Independencia
            datetime(anio, 12, 8),    # Inmaculada Concepción
            datetime(anio, 12, 25),   # Navidad

            # Feriados trasladables (aproximados)
            FeriadosArgentinos._get_pascua(anio) - timedelta(days=2),  # Viernes Santo
            FeriadosArgentinos._get_pascua(anio) + timedelta(days=60), # Malvinas (2 abril, si cae entre semana)
        ]

        # Agregar feriados que a veces se hacen puente
        feriados_extras = []
        for fecha in feriados_fijos:
            # Si el feriado cae jueves, agregar viernes como "puente"
            if fecha.weekday() == 3:  # Jueves
                feriados_extras.append(fecha + timedelta(days=1))
            # Si cae martes, agregar lunes como "puente"
            elif fecha.weekday() == 1:  # Martes
                feriados_extras.append(fecha - timedelta(days=1))

        return feriados_fijos + feriados_extras

    @staticmethod
    def _get_pascua(anio):
        """Calcula Domingo de Pascua (algoritmo de Gauss)."""
        a = anio % 19
        b = anio % 4
        c = anio % 7
        d = (19 * a + 24) % 30
        e = (2 * b + 4 * c + 6 * d + 5) % 7
        dia = d + e

        if dia < 10:
            return datetime(anio, 3, 22 + dia)
        else:
            return datetime(anio, 4, dia - 9)

    @staticmethod
    def es_fin_largo(fecha, feriados):
        """Detecta fines de semana largos (viernes o lunes feriado)."""
        if fecha in feriados:
            return True

        # Si es viernes y el lunes es feriado (fin largo)
        if fecha.weekday() == 4:  # Viernes
            lunes = fecha + timedelta(days=3)
            if lunes in feriados:
                return True

        # Si es lunes y el viernes fue feriado (fin largo)
        if fecha.weekday() == 0:  # Lunes
            viernes = fecha - timedelta(days=3)
            if viernes in feriados:
                return True

        return False

def main():
    print("🏥 Generando datos sintéticos VigiSalud con feriados...")

    # 3 años de datos diarios
    dates = pd.date_range("2023-01-01", "2025-12-31", freq="D")

    # Configuración basada en experiencia real
    BASE_CONSULTAS = 45
    weekly_pattern = {
        0: 0.85,  # lunes: -15%
        1: 0.95,  # martes: -5%
        2: 1.00,  # miércoles: base
        3: 1.05,  # jueves: +5%
        4: 1.25,  # viernes: +25%
        5: 1.15,  # sábado: +15%
        6: 1.10   # domingo: +10%
    }

    # Precalcular todos los feriados para el período
    todos_feriados = []
    for anio in [2023, 2024, 2025]:
        todos_feriados.extend(FeriadosArgentinos.get_feriados_anio(anio))

    # Para asuetos inesperados (ej: paro, duelo, etc.)
    # Agregamos algunos días aleatorios como "asueto imprevisto"
    asuetos_imprevistos = []
    for anio in [2023, 2024, 2025]:
        # 2-3 asuetos imprevistos por año
        for _ in range(np.random.randint(2, 4)):
            mes = np.random.randint(1, 13)
            dia = np.random.randint(1, 29)
            # No superponer con feriados ya existentes
            fecha_candidata = datetime(anio, mes, dia)
            if fecha_candidata not in todos_feriados:
                asuetos_imprevistos.append(fecha_candidata)

    todos_dias_no_laborables = todos_feriados + asuetos_imprevistos

    data = []
    for date in dates:
        weekday = date.weekday()
        date_datetime = date.to_pydatetime()

        # FACTORES DE DEMANDA
        week_factor = weekly_pattern[weekday]

        # Estacionalidad
        month = date.month
        if month in [12, 1, 2]:  # verano
            season_factor = 0.90
        elif month in [6, 7, 8]:  # invierno
            season_factor = 1.05
        else:
            season_factor = 1.0

        # FERIADOS Y FINES LARGOS (¡CRÍTICO!)
        es_feriado = date_datetime in todos_feriados
        es_asueto_imprevisto = date_datetime in asuetos_imprevistos
        es_fin_largo = FeriadosArgentinos.es_fin_largo(date_datetime, todos_feriados)

        if es_feriado or es_asueto_imprevisto:
            # Feriados: demanda muy baja (solo urgencias reales)
            feriado_factor = 0.4  # -60%
        elif es_fin_largo:
            # Fines largos: demanda similar a domingo pero extendida
            feriado_factor = 0.7  # -30%
        else:
            feriado_factor = 1.0

        # Días alrededor de feriados también afectados
        dia_despues_feriado = False
        dia_antes_feriado = False

        for feriado in todos_feriados:
            if abs((date_datetime - feriado).days) == 1:
                if date_datetime > feriado:
                    dia_despues_feriado = True
                else:
                    dia_antes_feriado = True

        if dia_despues_feriado:
            # Día después de feriado: +20% (acumulación)
            feriado_factor *= 1.2
        elif dia_antes_feriado:
            # Día antes de feriado: -15% (preparativos)
            feriado_factor *= 0.85

        # Ruido realista ±15%
        noise = np.random.normal(1.0, 0.15)

        # CONSULTAS FINALES (con todos los factores)
        consultas = BASE_CONSULTAS * week_factor * season_factor * feriado_factor * noise
        consultas = int(max(8, min(85, consultas)))  # Límites realistas expandidos

        # FEATURES (ahora incluyendo contexto feriados)
        row = {
            'fecha': date,
            'consultas': consultas,
            'dia_semana': weekday,
            'mes': month,
            'es_fin_de_semana': 1 if weekday >= 5 else 0,
            'es_verano': 1 if month in [12, 1, 2] else 0,
            'es_invierno': 1 if month in [6, 7, 8] else 0,
            'trimestre': (month - 1) // 3 + 1,
            'dia_del_anio': date.dayofyear,
            'semana_del_anio': date.isocalendar()[1],
            'es_feriado': 1 if es_feriado else 0,
            'es_asueto_imprevisto': 1 if es_asueto_imprevisto else 0,
            'es_fin_largo': 1 if es_fin_largo else 0,
            'dia_despues_feriado': 1 if dia_despues_feriado else 0,
            'dia_antes_feriado': 1 if dia_antes_feriado else 0,
            'densidad_poblacion': np.random.normal(100, 20),
            'porcentaje_mayores_65': np.random.normal(15, 3),
        }
        data.append(row)

    df = pd.DataFrame(data)

    # Targets para predicción (7 y 14 días)
    df['target_7d'] = df['consultas'].shift(-7).fillna(BASE_CONSULTAS)
    df['target_14d'] = df['consultas'].shift(-14).fillna(BASE_CONSULTAS)

    # Guardar
    df.to_csv('data/synthetic.csv', index=False)

    # Estadísticas descriptivas
    stats = df['consultas'].describe()
    feriados_count = df['es_feriado'].sum()
    fines_largos_count = df['es_fin_largo'].sum()

    print(f"✅ Datos generados: {len(df)} días")
    print(f"📊 Consultas/día: avg={stats['mean']:.1f}, std={stats['std']:.1f}")
    print(f"🎯 Feriados: {feriados_count} días")
    print(f"🏖️  Fines largos: {fines_largos_count} días")
    print(f"📍 Guardado: data/synthetic.csv")

    # Mostrar ejemplo de patrón de feriado
    ejemplo_feriado = df[df['es_feriado'] == 1].iloc[0]
    print(f"📅 Ejemplo feriado: {ejemplo_feriado['fecha']} -> {ejemplo_feriado['consultas']} consultas")

if __name__ == "__main__":
    main()
