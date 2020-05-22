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
        # print(self.all_dict)
        self.all_list = list(all_cards)
        # print(self.all_list)

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

    # ペアがあれば捨ててくださ園主問題
    @staticmethod
    def delete_pair():
        print('\n=== Discard if you have pairs. ===')


class Player(Dealer):
    def __init__(self, index, dealer):
        self.name = dealer.player_names[index]
        self.cards = dealer.dict_deck[self.name]
        print(self.name, ':', self.cards)
        player_dict = {}
        for i in self.cards:
            player_dict[i] = dealer.all_dict[i]
            self.player_dict = player_dict
        print('self.player_dict: ', self.player_dict)


    # def pull(self, next_player):
    #     self.cards.append(next_player.cards.pop())


    def delete_dup(self, dealer):
        # 2, 4枚の場合
        only_num_list = []
        for t in self.cards:
            only_num_list.append(dealer.all_dict[t])
        l = []
        for x in set(only_num_list):
            if only_num_list.count(x) == 2 or only_num_list.count(x) == 4:
                for a in only_num_list:
                    if a == x:
                        l.append(a)
        print('l:', l)
        k = []
        for i in set(l):
            k.append([k for k, v in self.player_dict.items() if v == i])
        print('k:', k)
        for j in k:
            for u in j:
                del self.player_dict[u]
        print('self.player_dict: ', self.player_dict)
        print('set(only_num_list): ', set(only_num_list))

        # 3枚の場合
        ju = []
        for j in set(only_num_list):
            ju.append([k for k, v in self.player_dict.items() if v == j])
        print('ju: ', ju)
        je = []
        for i in ju:
            if i:
                je.append(i.pop())
        print('je: ', je)




        only_num_list = set(only_num_list)
        only_num_list = list(only_num_list)
        return only_num_list





class Game(CreateCard):
    def play(self):
        dealer = Dealer()
        dealer.start()
        dealer.how_many()
        dealer.what_is_your_name()
        dealer.deal()
        dealer.delete_pair()
        for i in range(dealer.num):
            l = []
            player = Player(i, dealer)
            only_num = player.delete_dup(dealer)
            print('only_num: ', only_num)
            for j in only_num:
                l.append([k for k, v in player.player_dict.items() if v == j])
            print(l)

    #         for k in a:
    #             self.all_dict[]
    #         self._show_result(dealer, i, a)
    #
    # def _show_result(self, dealer, i, contents):
    #     print(dealer.player_names[i], ':', contents)



if __name__ == '__main__':
    game = Game()
    game.play()
