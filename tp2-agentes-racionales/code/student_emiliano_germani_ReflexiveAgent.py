import sys
import os
from typing import Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent

class ReflexiveAgent(BaseAgent):
    """
    Agente reflexivo: limpia si la celda está sucia, de lo contrario se mueve
    en un patrón tipo 'serpiente' por la grilla. Se detiene cuando el entorno
    indica que la simulación ha terminado.
    """

    def __init__(self, server_url: str = "http://localhost:5000",
                 enable_ui: bool = False,
                 record_game: bool = False,
                 replay_file: Optional[str] = None,
                 cell_size: int = 60,
                 fps: int = 10,
                 auto_exit_on_finish: bool = True,
                 live_stats: bool = False):
        super().__init__(server_url, "ReflexiveAgent", enable_ui, record_game,
                         replay_file, cell_size, fps, auto_exit_on_finish, live_stats)

        # Secuencia de movimiento tipo serpiente
        self.direction = "right"

    def get_strategy_description(self) -> str:
        return "Clean if dirty, otherwise sweep grid in snake pattern"

    def think(self):
        if not self.is_connected():
            return False

        perception = self.get_perception()
        if not perception:
            return False

        # 🚨 Detener ejecución si el entorno indica fin
        if perception.get("is_finished", False):
            return False

        x, y = perception.get('position', (0, 0))
        is_dirty = perception.get('is_dirty', False)
        grid = self.get_environment_state().get('grid', [])

        # ✅ Si la celda está sucia, limpiar
        if is_dirty:
            return self.suck()

        # ✅ Movimiento tipo serpiente
        width = len(grid[0])
        height = len(grid)

        if y % 2 == 0:  # fila par: mover a la derecha
            if x < width - 1:
                return self.right()
            elif y < height - 1:
                return self.down()
            else:
                return False  # fin de recorrido
        else:  # fila impar: mover a la izquierda
            if x > 0:
                return self.left()
            elif y < height - 1:
                return self.down()
            else:
                return False  # fin de recorrido


# 🔹 Ejecución individual de prueba
def run_reflexive_agent_simulation(size_x: int = 8, size_y: int = 8,
                                   dirt_rate: float = 0.3,
                                   server_url: str = "http://localhost:5000",
                                   verbose: bool = True) -> int:
    agent = ReflexiveAgent(server_url)
    try:
        if not agent.connect_to_environment(size_x, size_y, dirt_rate):
            return 0
        performance = agent.run_simulation(verbose)
        return performance
    finally:
        agent.disconnect()


if __name__ == "__main__":
    print("Reflexive Agent – Snake Pattern Strategy")
    print("Running test simulation...\n")
    performance = run_reflexive_agent_simulation(verbose=True)
    print(f"\nFinal performance: {performance}")
