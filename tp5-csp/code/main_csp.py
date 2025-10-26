from nqueens_csp_backtracking import backtracking_csp
from nqueens_csp_fc import nqueens_forward_checking

def main():
    print("===== COMPARACIÓN DE ALGORITMOS CSP - N REINAS =====\n")
    n = 8  # tamaño del tablero

    print(">>> BACKTRACKING CLÁSICO")
    result_bt = backtracking_csp(n)
    print(f"Solución: {result_bt['solution']}")
    print(f"Estados explorados: {result_bt['states']}")
    print(f"Tiempo: {result_bt['time']:.6f} segundos")
    print("------------------------------------------\n")

    print(">>> FORWARD CHECKING")
    result_fc = nqueens_forward_checking(n)
    print(f"Solución: {result_fc['solution']}")
    print(f"Estados explorados: {result_fc['states']}")
    print(f"Tiempo: {result_fc['time']:.6f} segundos")
    print("------------------------------------------\n")

    # Comparación general
    print("===== COMPARATIVA GENERAL =====")
    if result_bt["time"] < result_fc["time"]:
        print("Backtracking fue más rápido.")
    else:
        print("Forward Checking fue más rápido.")

    if result_bt["states"] < result_fc["states"]:
        print("Backtracking exploró menos estados.")
    else:
        print("Forward Checking exploró menos estados.")

if __name__ == "__main__":
    main()
