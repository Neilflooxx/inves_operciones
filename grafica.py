import numpy as np
import matplotlib.pyplot as plt
from itertools import combinations

def pedir_restriccion():
    tipo = input("\n¿Es una ecuación (=) o inecuación? (Escriba =, <=, >=, <, >): ").strip()
    c1 = float(input("Coeficiente de x1: "))
    c2 = float(input("Coeficiente de x2: "))
    const = float(input("Constante (lado derecho): "))
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

def resolver_y_graficar(restricciones, a, b):
    x_vals = np.linspace(0, 20, 400)
    lines = []
    eq_restricciones = [r for r in restricciones if r[2] == "="]

    for c1, c2, tipo, const in restricciones:
        if c2 != 0:
            y_vals = (const - c1 * x_vals) / c2
        else:
            y_vals = np.full_like(x_vals, np.nan)
            y_vals[np.abs(x_vals - (const / c1)) < 0.01] = 0
        lines.append((x_vals, y_vals, f"{c1}x₁ {tipo} {c2}x₂ = {const}", tipo, c1, c2, const))

    vertices = []
    if eq_restricciones:
        eq = eq_restricciones[0]  # Tomamos una sola ecuación por simplicidad
        for c1, c2, tipo, const in restricciones:
            if (c1, c2, tipo, const) == eq:
                continue
            A = np.array([[eq[0], eq[1]], [c1, c2]])
            B = np.array([eq[3], const])
            try:
                punto = np.linalg.solve(A, B)
                x, y = punto
                if es_factible(x, y, restricciones):
                    vertices.append((x, y))
            except:
                continue
    else:
        for (c1_1, c2_1, tipo1, const1), (c1_2, c2_2, tipo2, const2) in combinations(restricciones, 2):
            A = np.array([[c1_1, c2_1], [c1_2, c2_2]])
            B = np.array([const1, const2])
            try:
                punto = np.linalg.solve(A, B)
                x, y = punto
                if es_factible(x, y, restricciones):
                    vertices.append((x, y))
            except:
                continue

    if not vertices:
        print("❌ No hay región factible.")
        return

    Z_values = []
    print("\n📌 Puntos factibles y sus valores de Z:")
    for x, y in vertices:
        z = a * x + b * y
        Z_values.append(z)
        print(f"  ➤ Punto ({x:.2f}, {y:.2f})  →  Z = {z:.2f}")

    max_Z = max(Z_values)
    opt_idx = Z_values.index(max_Z)
    x_opt, y_opt = vertices[opt_idx]

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

    plt.figure(figsize=(9,6))
    colors = ['green', 'blue', 'purple', 'orange', 'brown', 'black']
    for i, (x_l, y_l, label, *_ ) in enumerate(lines):
        plt.plot(x_l, y_l, label=label, color=colors[i % len(colors)])
    plt.contourf(X, Y, region_mask.astype(int), levels=[0.5, 1], colors=['#ffff99'], alpha=0.6)
    plt.plot(x_opt, y_opt, 'ro', markersize=10, label=f'Óptimo: ({x_opt:.2f}, {y_opt:.2f})')
    plt.text(x_opt + 0.3, y_opt, f'Z = {max_Z:.2f}', fontsize=10, color='red')
    plt.xlim(0, 15)
    plt.ylim(0, 20)
    plt.xlabel("x₁")
    plt.ylabel("x₂")
    plt.title("Z máximo solo en intersección válida (si hay ecuación)")
    plt.legend()
    plt.grid(True)
    plt.show()

print("🎯 Método gráfico con ecuación opcional (restricción exacta)")

print("📌 Ingrese la función objetivo Z = ax₁ + bx₂")
a = float(input("Coeficiente de x₁: "))
b = float(input("Coeficiente de x₂: "))

restricciones = [
    (1, 0, ">=", 0),
    (0, 1, ">=", 0)
]

print("\n🔹 Ingrese al menos 2 restricciones adicionales:")
for i in range(2):
    print(f"\nRestricción #{i+1}")
    restricciones.append(pedir_restriccion())

while True:
    resolver_y_graficar(restricciones, a, b)
    resp = input("¿Deseas agregar otra restricción? (s/n): ").strip().lower()
    if resp == "s":
        restricciones.append(pedir_restriccion())
    else:
        break
print("✅ Proceso finalizado.")
