#include <iostream>
#include <vector>
#include <cmath>
#include <limits>
#include <algorithm>
#include <string>
#include <cctype> // Para tolower

using namespace std;

// ================================
// === Definición de Empleado ===
// ================================
struct Empleado {
    int id;
    string nombre;
    string dni;
    string area;
    double latitud;
    double longitud;

    Empleado(int id, string nombre, string dni, string area, double lat, double lon)
        : id(id), nombre(nombre), dni(dni), area(area), latitud(lat), longitud(lon) {}
};

// =================================
// === Nodo y KD-Tree (2D) ===
// =================================
struct NodoKD {
    Empleado emp;
    NodoKD* izquierda;
    NodoKD* derecha;

    NodoKD(Empleado e) : emp(e), izquierda(nullptr), derecha(nullptr) {}
};

class KDTree {
private:
    NodoKD* raiz;

    NodoKD* insertar(NodoKD* nodo, Empleado emp, int profundidad) {
        if (nodo == nullptr) return new NodoKD(emp);

        bool compararX = (profundidad % 2 == 0);
        if (compararX) {
            if (emp.latitud < nodo->emp.latitud)
                nodo->izquierda = insertar(nodo->izquierda, emp, profundidad + 1);
            else
                nodo->derecha = insertar(nodo->derecha, emp, profundidad + 1);
        } else {
            if (emp.longitud < nodo->emp.longitud)
                nodo->izquierda = insertar(nodo->izquierda, emp, profundidad + 1);
            else
                nodo->derecha = insertar(nodo->derecha, emp, profundidad + 1);
        }

        return nodo;
    }

    double distancia(double x1, double y1, double x2, double y2) {
        return sqrt(pow(x1 - x2, 2) + pow(y1 - y2, 2));
    }

    NodoKD* nearestNeighbor(NodoKD* nodo, Empleado target, int profundidad) {
        if (nodo == nullptr) return nullptr;

        bool compararX = (profundidad % 2 == 0);
        NodoKD* siguiente = (compararX ? (target.latitud < nodo->emp.latitud ? nodo->izquierda : nodo->derecha)
                                      : (target.longitud < nodo->emp.longitud ? nodo->izquierda : nodo->derecha));
        NodoKD* otro = (compararX ? (target.latitud < nodo->emp.latitud ? nodo->derecha : nodo->izquierda)
                                  : (target.longitud < nodo->emp.longitud ? nodo->derecha : nodo->izquierda));

        NodoKD* mejor = siguiente ? nearestNeighbor(siguiente, target, profundidad + 1) : nullptr;
        if (mejor == nullptr) mejor = nodo;

        double d1 = distancia(target.latitud, target.longitud, mejor->emp.latitud, mejor->emp.longitud);
        double d2 = distancia(target.latitud, target.longitud, nodo->emp.latitud, nodo->emp.longitud);

        if (d2 < d1) mejor = nodo;

        double distPlano = (compararX ? abs(target.latitud - nodo->emp.latitud)
                                      : abs(target.longitud - nodo->emp.longitud));

        if (distPlano < distancia(target.latitud, target.longitud, mejor->emp.latitud, mejor->emp.longitud)) {
            NodoKD* temp = (otro ? nearestNeighbor(otro, target, profundidad + 1) : nullptr);
            if (temp != nullptr) {
                double d3 = distancia(target.latitud, target.longitud, temp->emp.latitud, temp->emp.longitud);
                if (d3 < distancia(target.latitud, target.longitud, mejor->emp.latitud, mejor->emp.longitud))
                    mejor = temp;
            }
        }

        return mejor;
    }

public:
    vector<Empleado> listaEmpleados;

    KDTree() : raiz(nullptr) {}

    void insertar(Empleado emp) {
        raiz = insertar(raiz, emp, 0);
        listaEmpleados.push_back(emp);
    }

    Empleado nearestNeighbor(Empleado target) {
        NodoKD* result = nearestNeighbor(raiz, target, 0);
        return result ? result->emp : Empleado(-1, "No encontrado", "", "", 0, 0);
    }

    void mostrarTodos() {
        cout << "\n=== Lista de Empleados ===\n";
        for (auto& e : listaEmpleados) {
            cout << "ID: " << e.id << ", Nombre: " << e.nombre
                 << ", DNI: " << e.dni
                 << ", Area: " << e.area
                 << ", Ubicacion: (" << e.latitud << ", " << e.longitud << ")\n";
        }
    }

    bool eliminar(int id) {
        auto it = remove_if(listaEmpleados.begin(), listaEmpleados.end(),
                            [id](Empleado& e) { return e.id == id; });
        if (it != listaEmpleados.end()) {
            listaEmpleados.erase(it, listaEmpleados.end());
            reconstruirArbol();
            return true;
        }
        return false;
    }

    void reconstruirArbol() {
        raiz = nullptr;
        for (auto& e : listaEmpleados) {
            raiz = insertar(raiz, e, 0);
        }
    }

    vector<Empleado> buscarPorNombre(string patron) {
        transform(patron.begin(), patron.end(), patron.begin(), ::tolower);
        vector<Empleado> resultado;
        for (auto& e : listaEmpleados) {
            string nombreMin = e.nombre;
            transform(nombreMin.begin(), nombreMin.end(), nombreMin.begin(), ::tolower);
            if (nombreMin.find(patron) != string::npos)
                resultado.push_back(e);
        }
        return resultado;
    }

    vector<Empleado> buscarPorDNI(string patron) {
        transform(patron.begin(), patron.end(), patron.begin(), ::tolower);
        vector<Empleado> resultado;
        for (auto& e : listaEmpleados) {
            string dniMin = e.dni;
            transform(dniMin.begin(), dniMin.end(), dniMin.begin(), ::tolower);
            if (dniMin.find(patron) != string::npos)
                resultado.push_back(e);
        }
        return resultado;
    }
};

// =======================
// === Menú Principal ===
// =======================
void mostrarMenu() {
    system("cls");
    cout << "=========================================\n";
    cout << "   SISTEMA DE GESTIÓN DE EMPLEADOS\n";
    cout << "=========================================\n";
    cout << "1. Registrar empleado\n";
    cout << "2. Buscar empleado (por nombre o DNI)\n";
    cout << "3. Buscar empleado más cercano\n";
    cout << "4. Mostrar todos los empleados\n";
    cout << "5. Eliminar empleado\n";
    cout << "6. Salir\n";
    cout << "Seleccione una opción: ";
}

int main() {
    KDTree arbol;
    int opcion;
    int idContador = 1;

    do {
        mostrarMenu();
        cin >> opcion;

        if (opcion == 1) {
            system("cls");
            string nombre, dni, area;
            double lat, lon;
            cout << "=== Registro de Empleado ===\n";
            cin.ignore(); // Limpiar buffer
            cout << "Nombre: "; getline(cin, nombre);
            cout << "DNI: "; cin >> dni;
            cout << "Área: "; cin >> area;
            cout << "Latitud: "; cin >> lat;
            cout << "Longitud: "; cin >> lon;

            arbol.insertar(Empleado(idContador++, nombre, dni, area, lat, lon));
            cout << "\n✅ Empleado registrado.\n";
            system("pause");

        } else if (opcion == 2) {
            system("cls");
            int tipoBusqueda;
            cout << "=== Buscar Empleado ===\n";
            cout << "1. Por nombre\n2. Por DNI\nIngrese opción: ";
            cin >> tipoBusqueda;

            if (tipoBusqueda == 1) {
                string patron;
                cin.ignore();
                cout << "Ingrese nombre o parte del nombre: ";
                getline(cin, patron);

                vector<Empleado> resultados = arbol.buscarPorNombre(patron);

                if (!resultados.empty()) {
                    cout << "\n🔍 Resultados encontrados:\n";
                    for (auto& e : resultados) {
                        cout << "ID: " << e.id << "\n";
                        cout << "Nombre: " << e.nombre << "\n";
                        cout << "DNI: " << e.dni << "\n";
                        cout << "Área: " << e.area << "\n";
                        cout << "Ubicación: (" << e.latitud << ", " << e.longitud << ")\n\n";
                    }
                } else {
                    cout << "\n❌ No se encontraron empleados con ese nombre.\n";
                }

            } else if (tipoBusqueda == 2) {
                string patron;
                cin.ignore();
                cout << "Ingrese DNI o parte del DNI: ";
                getline(cin, patron);

                vector<Empleado> resultados = arbol.buscarPorDNI(patron);

                if (!resultados.empty()) {
                    cout << "\n🔍 Resultados encontrados:\n";
                    for (auto& e : resultados) {
                        cout << "ID: " << e.id << "\n";
                        cout << "Nombre: " << e.nombre << "\n";
                        cout << "DNI: " << e.dni << "\n";
                        cout << "Área: " << e.area << "\n";
                        cout << "Ubicación: (" << e.latitud << ", " << e.longitud << ")\n\n";
                    }
                } else {
                    cout << "\n❌ No se encontraron empleados con ese DNI.\n";
                }
            } else {
                cout << "\n❌ Opción no válida.\n";
            }
            system("pause");

        } else if (opcion == 3) {
            system("cls");
            double lat, lon;
            cout << "=== Buscar Empleado Más Cercano ===\n";
            cout << "Ingrese Latitud objetivo: "; cin >> lat;
            cout << "Ingrese Longitud objetivo: "; cin >> lon;

            Empleado target(0, "Target", "", "", lat, lon);
            Empleado cercano = arbol.nearestNeighbor(target);

            cout << "\n🔎 Vecino más cercano:\n";
            cout << "ID: " << cercano.id << "\n";
            cout << "Nombre: " << cercano.nombre << "\n";
            cout << "DNI: " << cercano.dni << "\n";
            cout << "Área: " << cercano.area << "\n";
            cout << "Ubicación: (" << cercano.latitud << ", " << cercano.longitud << ")\n";

            system("pause");

        } else if (opcion == 4) {
            system("cls");
            cout << "=== Todos los Empleados ===\n";
            arbol.mostrarTodos();
            system("pause");

        } else if (opcion == 5) {
            system("cls");
            int id;
            cout << "=== Eliminar Empleado ===\n";
            cout << "Ingrese ID del empleado a eliminar: ";
            cin >> id;
            if (arbol.eliminar(id)) {
                cout << "\n🗑️ Empleado eliminado.\n";
            } else {
                cout << "\n❌ No se encontró al empleado.\n";
            }
            system("pause");
        }

    } while (opcion != 6);

    cout << "\n👋 ¡Hasta luego!\n";
    system("pause");
    return 0;
}