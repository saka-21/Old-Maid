from babanuki_dir.models import babanuki



def main():
    game = babanuki.Game()
    game.deal()
    game.first_discard()
    game.turn()
    game.play_game()
    game.final_result()


if __name__ == "__main__":
    main()
