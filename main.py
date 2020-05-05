import babanuki_apply

def main():
    game = babanuki_apply.Game()
    game.deal()
    game.first_discard()
    game.turn()
    game.play_game()
    game.final_result()


if __name__ == "__main__":
    main()