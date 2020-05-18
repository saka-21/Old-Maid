from babanuki_dir.models import babanuki
from babanuki_dir.models import babanuki
from babanuki_dir.models import babanuki_03


def main():
    game = babanuki_03.Game()
    game.deal()
    game.first_discard()
    game.turn()
    game.play_game()
    game.final_result()


if __name__ == "__main__":
    main()
