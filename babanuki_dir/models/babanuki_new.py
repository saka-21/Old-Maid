import random


class CreateCard(object):
    def __init__(self):
        suits = ['s', 'h', 'd', 'c']
        all_cards = {}
        for i, k in enumerate(range(1, 14), 1):
            for j in suits:
                key = str(k) + "_" + j
                all_cards[key] = i
        all_cards['BABA'] = 0
        self.all_dict = all_cards
        self.all_list = list(all_cards)

class Dealer(CreateCard):
    def __init__(self):
        super().__init__()

    # ババ抜きを始めます。
    def start(self):
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
    def deal(self):
        print('\n=== Here are some cards. ===')
        players_cards = []
        random.shuffle(self.all_list)
        for i in range(self.num):
            players_cards.append([])
        while len(self.all_list) > 0:
            for player_cards in players_cards:
                player_cards.append(self.all_list.pop())
                if len(self.all_list) == 0:
                    break

        self.players_cards = players_cards
        for (name, player) in zip(self.player_names, self.players_cards):
            print(name + " : " + ",  ".join(player))
        self.dict_deck = dict(zip(self.player_names, self.players_cards))

    # ペアがあれば捨ててください
    @staticmethod
    def delete_pair():
        print('\n=== Discard if you have pairs. ===')


class Player(Dealer):
    def __init__(self, index, dealer):
        self.name = dealer.player_names[index]
        self.cards = []
        self.after_dict = {}
        # print(self.name, ':', self.cards)
        player_dict = {}
        for i in dealer.dict_deck[self.name]:
            player_dict[i] = dealer.all_dict[i]
            self.player_dict = player_dict
        # print('self.player_dict: ', self.player_dict)

    def append(self, card):
        dealer = Dealer()
        self.cards.append(card)
        self.after_dict[card] = dealer.all_dict[card]

    def release(self, card):
        self.cards.remove(card)
        # if not self.cards:


    def play(self, next_player):
        card = random.choice(next_player.cards)
        next_player.release(card)
        self.append(card)
        return card

    def delete_dup(self, dealer, card):
        # 自分自身のカードの数字だけ取得
        only_num_list = []
        for t in card:
            only_num_list.append(dealer.all_dict[t])
        a = only_num_list

        # ２枚、４枚ではないカードの数字を取得
        for x in set(only_num_list):
            if only_num_list.count(x) == 2 or only_num_list.count(x) == 4:
                only_num_list = [a for a in only_num_list if a != x]
        if only_num_list == a:
            self.cards = card
            return card

        # ２枚、４枚ではないカードのマークを取得
        key_list = []
        for i in set(only_num_list):
            if self.after_dict:
                key_list.append([k for k, v in self.after_dict.items() if v == i])
            else:
                key_list.append([k for k, v in self.player_dict.items() if v == i])
        print('key_list: ', key_list)

        # ３枚あるカードは一枚だけ取得
        key_list_02 = []
        for i in key_list:
            if i:
                key_list_02.append(i.pop())
        print('key_list_02: ', key_list_02)

        # 削除した後のカードの辞書
        d = {}
        for i in key_list_02:
            d[i] = dealer.all_dict[i]

        only_num_list = set(only_num_list)
        after_num_list = list(only_num_list)
        self.after_dict = d
        self.cards = key_list_02
        self.only_num_list = after_num_list
        return key_list_02


class Game(CreateCard):

    def play(self):
        # 準備
        dealer = Dealer()
        dealer.start()
        dealer.how_many()
        dealer.what_is_your_name()
        dealer.deal()
        dealer.delete_pair()
        self.players = [Player(i, dealer) for i in range(dealer.num)]
        for player in self.players:
            player.delete_dup(dealer, dealer.dict_deck[player.name])
        self._show_result()

        # GameStart
        turn = 1
        n = -1
        for i in range(20):
            n += 1
            if n == dealer.num:
                n = 0
            if n == dealer.num - 1:
                n = -1
            print('\n== Turn-{} =='.format(turn))
            self._turn(n, dealer)
            turn += 1

    def _turn(self, i, dealer):
        pulled_card = self.players[i].play(self.players[i+1])
        print('{} pulled {}'.format(self.players[i].name, pulled_card))
        self._show_result()
        # print('self.players[i].cards: ', self.players[i].cards)
        self.players[i].delete_dup(dealer, self.players[i].cards)
        dealer.delete_pair()
        self._show_result()

    def _show_result(self):
        for player in self.players:
            print(player.name + " : " + ',  '.join(player.cards))


if __name__ == '__main__':
    game = Game()
    game.play()
