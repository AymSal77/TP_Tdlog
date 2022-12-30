from DAO.DAO import GameDao
from model.player import Player
from model.vessel import Vessel
from model.battlefield import Battlefield
from model.game import Game
class GameService:
    def __init__(self):
        self.game_dao = GameDao()

    def create_game(self, player_name: str, min_x: int, max_x: int, min_y: int, max_y: int, min_z: int,
                        max_z: int) -> int:
        game = Game()
        battle_field = Battlefield(min_x, max_x, min_y, max_y, min_z, max_z)
        game.add_player(Player(player_name, battle_field))
        return self.game_dao.create_game(game)

    def join_game(self, game_id: int, player_name: str) -> bool:
        self.game = GameDao.find_game(game_id)
        self.game.add_player(Player(player_name), Battlefield=None)
        return True

    def add_vessel(self, game_id: int, player_name: str, vessel_type: str, x: int, y: int, z: int) -> bool:
        game = self.game_dao.find_game(game_id)
        if not game:
            return False

        player = next((p for p in game.players if p.name == player_name), None)
        if not player:
            return False

        vessel = Vessel(vessel_type, x, y, z)
        player.add_vessel(vessel)
        self.game_dao.update_player(player)

        return True

    def shoot_at(self, game_id: int, shooter_name: str, vessel_id: int, x: int, y: int, z: int) -> bool:
        game = self.game_dao.find_game(game_id)
        if not game:
            return False

        shooter = next((p for p in game.players if p.name == shooter_name), None)
        if not shooter:
            return False

        vessel = next((v for v in shooter.vessels if v.id == vessel_id), None)
        if not vessel:
            return False
        success = vessel.shoot_at(x, y, z)
        self.game_dao.update_player(shooter)
        return success

    def get_game_status(self, game_id: int, shooter_name: str) -> str:
        game = self.game_dao.find_game(game_id)
        for player in game.players:
            if player.name == shooter_name:
                if player.has_lost():
                    return "PERDU"
                else:
                    return "GAGNE"
        return "ENCOURS"


