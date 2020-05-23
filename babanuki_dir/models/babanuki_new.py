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
        self.ranking_list = []
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


ranking_list = []


class Player(Dealer):
    def __init__(self, index, dealer):
        self.name = dealer.player_names[index]
        self.cards = []
        self.after_dict = {}
        player_dict = {}
        for i in dealer.dict_deck[self.name]:
            player_dict[i] = dealer.all_dict[i]
            self.player_dict = player_dict

    def append(self, card):
        dealer = Dealer()
        self.cards.append(card)
        self.after_dict[card] = dealer.all_dict[card]

    def release(self, card):
        self.cards.remove(card)
        if not self.cards:
            ranking_list.append(self.name)
            self.cards = 'Done!'

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

        # ３枚あるカードは一枚だけ取得
        key_list_02 = []
        for i in key_list:
            if i:
                key_list_02.append(i.pop())

        # 削除した後のカードの辞書
        d = {}
        for i in key_list_02:
            d[i] = dealer.all_dict[i]

        self.after_dict = d
        self.cards = key_list_02
        if not self.cards:
            ranking_list.append(self.name)
            self.cards = 'Done!'
        else:
            return self.cards


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

        # ゲームスタート
        turn = 1
        n = -1
        self.card_list = []
        # while self.card_list.count('Done!') != dealer.num - 1:
        while self.card_list.count('Done!') != dealer.num - 2:

            print('\n== Turn-{} =='.format(turn))
            n += 1
            if n == dealer.num:
                n = 0
            if n == dealer.num - 1:
                n = -1
            m = n + 1

            # 通常のループ
            if self.players[n].cards != 'Done!' and self.players[m].cards != 'Done!':
                self._turn(n, m, dealer)

            # 誰かが上がった時のループ
            else:
                while True:
                    if self.players[n].cards != 'Done!':
                        break
                    n += 1
                    if self.players[n].cards != 'Done!':
                        break
                while True:
                    if m == dealer.num - 1:
                        m = -1
                    m += 1
                    if self.players[m].cards != 'Done!':
                        if m == n:
                            continue
                        if m != n:
                            break
                self._turn(n, m, dealer)

            self.card_list = []
            for player in self.players:
                self.card_list.append(player.cards)
            turn += 1
        self._show_final_result(dealer)

    def _turn(self, n, m, dealer):
        pulled_card = self.players[n].play(self.players[m])
        print('{} pulled {} of {}'.format(self.players[n].name,
                                          pulled_card, self.players[m].name))
        self._show_result()
        self.players[n].delete_dup(dealer, self.players[n].cards)
        dealer.delete_pair()
        self._show_result()

    def _show_result(self):
        for player in self.players:
            if 'Done!' in player.cards:
                print(player.name + " : " + ''.join(player.cards))
            else:
                print(player.name + " : " + ',  '.join(player.cards))

    def _show_final_result(self, dealer):
        print('\n======Finel-Result======')
        for i, name in enumerate(ranking_list):
            print("{}位: {}".format(i+1, name))
        n = self.players[self.card_list.index(['BABA'])].name
        print("{}位: {}".format(dealer.num, n))


if __name__ == '__main__':
    game = Game()
    game.play()
