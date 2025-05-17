import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

# ===================== FUNCIONES =====================

def pedir_restriccion():
    print("🔹 Tipos permitidos: = , <= , >= , < , >")
    tipo = input("¿Es ecuación (=) o inecuación? (Escriba =, <=, >=, <, >): ").strip()
    while tipo not in ['=', '<=', '>=', '<', '>']:
        tipo = input("⚠️ Tipo no válido. Escriba =, <=, >=, < o >: ").strip()

    try:
        c1 = float(input("Coeficiente de x1: "))
        c2 = float(input("Coeficiente de x2: "))
        const = float(input("Constante (lado derecho): "))
    except ValueError:
        print("❌ Error: Ingresa solo números.")
        return pedir_restriccion()

    return (c1, c2, tipo, const)

def es_factible(x, y, restricciones):
    for c1, c2, tipo, const in restricciones:
        lhs = c1 * x + c2 * y
        if tipo == "=" and not np.isclose(lhs, const, atol=1e-2):
            return False
        elif tipo == "<=" and not (lhs <= const + 1e-3):
            return False
        elif tipo == ">=" and not (lhs >= const - 1e-3):
            return False
        elif tipo == "<" and not (lhs < const):
            return False
        elif tipo == ">" and not (lhs > const):
            return False
    return x >= 0 and y >= 0

def encontrar_vertices(restricciones):
    vertices = []
    for (c1_1, c2_1, tipo1, const1), (c1_2, c2_2, tipo2, const2) in combinations(restricciones, 2):
        A = np.array([[c1_1, c2_1], [c1_2, c2_2]])
        B = np.array([const1, const2])
        try:
            punto = np.linalg.solve(A, B)
            x, y = punto
            if es_factible(x, y, restricciones):
                vertices.append((x, y))
        except np.linalg.LinAlgError:
            continue
    # Eliminar duplicados
    vertices = list(set(vertices))
    return vertices

def resolver_y_graficar(restricciones, a, b):
    x_vals = np.linspace(0, 20, 400)
    lines = []

    for c1, c2, tipo, const in restricciones:
        if c2 != 0:
            y_vals = (const - c1 * x_vals) / c2
        else:
            y_vals = np.full_like(x_vals, np.nan)
            y_vals[np.abs(x_vals - (const / c1)) < 0.01] = 0
        lines.append((x_vals, y_vals, f"{c1}x₁ {tipo} {c2}x₂ = {const}", tipo))

    # Encontrar vértices
    vertices = encontrar_vertices(restricciones)

    # Filtrar puntos que NO estén en los ejes (ignorar si x o y son 0)
    puntos_validos = [(x, y) for x, y in vertices if x > 0 and y > 0]

    # Evaluar función objetivo
    if puntos_validos:
        Z_values = [a * x + b * y for x, y in puntos_validos]
        max_Z = max(Z_values)
        opt_idx = Z_values.index(max_Z)
        x_opt, y_opt = puntos_validos[opt_idx]
    else:
        print("❌ No hay puntos internos factibles (lejos de los ejes).")
        return

    # Región factible
    X, Y = np.meshgrid(np.linspace(0, 20, 400), np.linspace(0, 20, 400))
    region_mask = np.ones_like(X, dtype=bool)
    for c1, c2, tipo, const in restricciones:
        lhs = c1 * X + c2 * Y
        if tipo == "=":
            region_mask &= np.isclose(lhs, const, atol=0.1)
        elif tipo == "<=":
            region_mask &= lhs <= const + 1e-3
        elif tipo == ">=":
            region_mask &= lhs >= const - 1e-3
        elif tipo == "<":
            region_mask &= lhs < const
        elif tipo == ">":
            region_mask &= lhs > const
    region_mask &= (X >= 0) & (Y >= 0)

    # Graficar
    plt.figure(figsize=(9,6))
    colors = ['green', 'blue', 'purple', 'orange', 'brown', 'black', 'darkred']
    for i, (x_l, y_l, label, _) in enumerate(lines):
        plt.plot(x_l, y_l, label=label, color=colors[i % len(colors)])
    plt.contourf(X, Y, region_mask.astype(int), levels=[0.5, 1], colors=['#ffff99'], alpha=0.6)
    plt.plot(x_opt, y_opt, 'ro', markersize=10, label=f'Óptimo: ({x_opt:.2f}, {y_opt:.2f})')
    plt.text(x_opt + 0.3, y_opt, f'Máx Z = {max_Z:.2f}', fontsize=10, color='red')

    # Zoom automático
    max_x = max([v[0] for v in puntos_validos]) if puntos_validos else 20
    max_y = max([v[1] for v in puntos_validos]) if puntos_validos else 20
    plt.xlim(0, max(5, max_x * 1.2))
    plt.ylim(0, max(5, max_y * 1.2))

    plt.xlabel("x₁")
    plt.ylabel("x₂")
    plt.title(f"Región factible y solución óptima\nMax Z = {a}x₁ + {b}x₂")
    plt.legend()
    plt.grid(True)
    plt.show()

    # Mostrar vértices y Z
    print("\n📊 Evaluación de Z en los puntos internos:")
    print("Punto | x₁     | x₂     | Z")
    print("--------------------------------------")
    for i, (x, y) in enumerate(puntos_validos):
        z_val = a * x + b * y
        print(f"{i+1}     | {x:.2f} | {y:.2f} | {z_val:.2f}")

    print(f"\n✅ Punto óptimo: ({x_opt:.2f}, {y_opt:.2f}), Z = {max_Z:.2f}")

# ===================== EJECUCIÓN =====================

print("🎯 Método gráfico dinámico con entrada de restricciones")

# Función objetivo
print("📌 Ingrese la función objetivo Z = ax₁ + bx₂")
try:
    a = float(input("Coeficiente de x₁: "))
    b = float(input("Coeficiente de x₂: "))
except ValueError:
    print("❌ Error: Solo se aceptan números.")
    exit()

# Ingreso de restricciones
restricciones = []
print("\n🔹 Ingrese al menos 2 restricciones:")
for i in range(2):
    print(f"\nRestricción #{i+1}")
    restricciones.append(pedir_restriccion())

# Agregar opción para seguir agregando restricciones
continuar = True
while continuar:
    resolver_y_graficar(restricciones, a, b)
    resp = input("¿Deseas agregar otra restricción? (s/n): ").strip().lower()
    if resp == "s":
        print(f"\nNueva restricción #{len(restricciones)+1}")
        restricciones.append(pedir_restriccion())
    else:
        continuar = False
        print("✅ Proceso finalizado. ¡Gracias por usar el graficador!")