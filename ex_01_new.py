import random
from itertools import count


class Card:
    SUITS = "♣♦♥♠"
    RANKS = "A23456789TJQK"

    def __init__(self, suit, rank=""):
        self.suit = suit
        self.rank = rank.replace("T", "10")
        self.number = rank and Card.RANKS.index(rank) + 1 or 0
        self.label = self.suit + self.rank

    def __repr__(self):
        return self.label


class Player:

    def __init__(self, name):
        self.name = name
        self.cards = []

    def hold(self, card):
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
        self.hold(card)
        return card, self.drop_pairs()

    def win(self):
        return not self.cards


class Dealer:

    @staticmethod
    def deal(players):
        cards = [Card(suit, rank) for suit in Card.SUITS for rank in Card.RANKS]
        cards += [Card("Joker")]
        random.shuffle(cards)
        for i, card in enumerate(cards):
            players[i % len(players)].hold(card)


class AutoOldmaid:

    def play(self, player_num):
        self.players = [Player(f"Player#{i+1}") for i in range(player_num)]
        self.ranking = []

        print("###### Preparation ######")
        Dealer.deal(self.players)
        self._show_hands()
        self._drop_pairs()
        self._show_hands()

        print("###### Game Start ######")
        self._show_heavenly_winner()
        turn = count(1)
        while len(self.players) > 1:
            print(f"===== Turn {next(turn)} ======")
            print(f"Playing {len(self.players)} players")
            self._turn()
            self._show_hands()

        print("###### Game Over ######")
        self._show_ranking()

    def _show_hands(self):
        print("------ Players Hand ------")
        for player in self.players:
            print(f"{player.name} holds {player.cards}")

    def _drop_pairs(self):
        print("------ Drop Pairs ------")
        for player in self.players:
            dropped_cards = player.drop_pairs()
            if dropped_cards:
                print(f"{player.name} dropped {dropped_cards}")

    def _show_heavenly_winner(self):
        for player in self.players[:]:
            if player.win():
                print(f"{player.name} いきなり上がり！")
                self.players.remove(player)
                self.ranking.append(player)

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
            pulled_card, dropped_cards = player.play(next_player)
            print(f"{player.name} pulled {pulled_card} from {next_player.name}")
            if next_player.win():
                print(f"{next_player.name} 引かれて上がり！")
                self.players.remove(next_player)
                self.ranking.append(next_player)
            if dropped_cards:
                print(f"{player.name} dropped {dropped_cards}")
            if player.win():
                print(f"{player.name} 引いて上がり！")
                self.players.remove(player)
                self.ranking.append(player)

    def _show_ranking(self):
        print("------ Ranking ------")
        for player in self.ranking + self.players:
            print(player.name)


if __name__ == "__main__":
    AutoOldmaid().play(player_num=4)