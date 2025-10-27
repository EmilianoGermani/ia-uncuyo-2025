import sys
import os
import random
from typing import Optional
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from base_agent import BaseAgent


class RandomAgent(BaseAgent):
    def __init__(self, server_url: str = "http://localhost:5000", 
                 enable_ui: bool = False,
                 record_game: bool = False, 
                 replay_file: Optional[str] = None,
                 cell_size: int = 60,
                 fps: int = 10,
                 auto_exit_on_finish: bool = True,
                 live_stats: bool = False):
        super().__init__(server_url, "RandomAgent", enable_ui, record_game, 
                        replay_file, cell_size, fps, auto_exit_on_finish, live_stats)

    def get_strategy_description(self) -> str:
        return "Clean if dirty, move in circular pattern when clean"

    def think(self):
        if not self.is_connected():
            return False

        perception = self.get_perception()
        if not perception or perception.get('is_finished', True):
            return False

        # Lista de acciones posibles
        possible_actions = [
            self.up,
            self.down,
            self.left,
            self.right,
            self.suck
        ]

        # Elegir una acción al azar
        action = random.choice(possible_actions)
        return action()


def run_random_agent_simulation(size_x: int = 8, size_y: int = 8, 
                                dirt_rate: float = 0.3, 
                                server_url: str = "http://localhost:5000",
                                verbose: bool = True) -> int:
    """
    Función auxiliar para ejecutar una simulación rápida del RandomAgent.
    """
    agent = RandomAgent(server_url)
    
    try:
        if not agent.connect_to_environment(size_x, size_y, dirt_rate):
            return 0
        
        performance = agent.run_simulation(verbose)
        return performance
    
    finally:
        agent.disconnect()


if __name__ == "__main__":
    print("Random Agent")
    print("Make sure the environment server is running on localhost:5000")
    print("Strategy: Clean if dirty, move in circular pattern when clean")
    performance = run_random_agent_simulation(verbose=True)
    print(f"\nDesempeño final: {performance}")
