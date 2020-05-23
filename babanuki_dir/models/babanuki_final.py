import random


class Card:
    SUITS = ['S', 'D', 'H', 'C']
    RANKS = [str(x+1) for x in range(13)]

    def __init__(self, suit, rank=""):
        self.suit = suit
        self.rank = rank
        self.number = rank and Card.RANKS.index(rank) + 1 or 0
        self.label = self.suit + self.rank

    def __repr__(self):
        return self.label


class Player:

    def __init__(self, index, dealer):
        self.name = dealer.player_names[index]
        self.cards = []

    def append(self, card):
        self.cards.append(card)

    def release(self, card):
        self.cards.remove(card)

    def drop_pairs(self):
        dropped_cards = []
        cards = sorted(self.cards, key=lambda card: card.number)
        for i in range(len(cards) - 1):
            if cards[i] and cards[i].rank == cards[i + 1].rank:
                dropped_cards += [cards[i], cards[i + 1]]
                cards[i] = cards[i + 1] = None
        self.cards = [card for card in self.cards if card not in dropped_cards]
        return dropped_cards

    def play(self, next_player):
        card = random.choice(next_player.cards)
        next_player.release(card)
        self.append(card)
        return card, self.drop_pairs()

    def win(self):
        return not self.cards


class Dealer:
    # ババ抜きを始めます。
    @staticmethod
    def start():
        print("\n=== Let's start Old Maid! ===")

    # 何人で遊びますか？
    def how_many(self):
        num = int(input('How many people?\n'))
        self.num = num

    # 名前を入力してください。
    def what_is_your_name(self):
        print("\n=== Please type in your name. ===")
        player_name = []
        for i in range(self.num):
            player_name.append(input('Player{} : '.format(i + 1)))
        self.player_names = player_name

    # カードを配ります。
    @staticmethod
    def deal(players):
        cards = []
        for suit in Card.SUITS:
            for rank in Card.RANKS:
                cards.append(Card(suit, rank))
        cards += [Card("Joker")]
        random.shuffle(cards)
        # print('cards: ', cards)
        for i, card in enumerate(cards):
            players[i % len(players)].append(card)


class Game:
    def play(self):
        dealer = Dealer()
        dealer.start()
        dealer.how_many()
        dealer.what_is_your_name()
        self.players = [Player(i, dealer) for i in range(dealer.num)]
        self.ranking = []

        Dealer.deal(self.players)
        self._show_result()
        self._drop_pairs()
        self._show_result()

        print("\n===== Game Start =====")
        turn = 1
        while len(self.players) > 1:
            print(f"\n[ Turn {turn} ]")
            self._turn()
            turn += 1

        self._show_ranking()

    def _show_result(self):
        print("-- Players Hand -------------")
        for player in self.players:
            print(f"{player.name} : {player.cards}")
        print("-----------------------------")

    def _drop_pairs(self):
        print("\n! Drop Pairs !")
        for player in self.players:
            player.drop_pairs()

    def _pair_players(self):
        players = self.players[:]
        for i, player in enumerate(players):
            if player.win():
                continue
            for next_player in players[i+1:] + players[:i]:
                if not next_player.win():
                    yield player, next_player
                    break

    def _turn(self):
        for player, next_player in self._pair_players():
            self._show_result()
            pulled_card, dropped_cards = player.play(next_player)
            print(f"\n{player.name} pulled {pulled_card} from {next_player.name}")
            self._show_result()
            if dropped_cards:
                print(f"{player.name} dropped {dropped_cards}")
            if next_player.win():
                print(f"{next_player.name} Done!")
                self.players.remove(next_player)
                self.ranking.append(next_player)

            if player.win():
                print(f"{player.name} Done！")
                self.players.remove(player)
                self.ranking.append(player)

    def _show_ranking(self):
        print('\n====== Final-Result ======')
        for i, player in enumerate(self.ranking + self.players, 1):
            print(f'{i} place : {player.name}')


if __name__ == "__main__":
    Game().play()