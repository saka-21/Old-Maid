import time
import random

from babanuki_dir.views import console


class CreateCard(object):
    def __init__(self):
        suits = ['s', 'h', 'd', 'c']
        sv_list = []
        for i in range(1, 14):
            for j in suits:
                sv_list.append(str(i) + "_" + j)
        sv_list.append("BABA")
        random.shuffle(sv_list)
        self.sv_list = sv_list


class Rules(object):
    def duplication_2_4(self, player_only_num):
        # 偶数枚の場合
        dup_even = []
        for x in set(player_only_num):
            if player_only_num.count(x) == 2 or player_only_num.count(
                    x) == 4:
                dup_even.append(x)
        # 重複しているindexを取得
        index_even = []
        for i, x in enumerate(player_only_num):
            for h in dup_even:
                if x == h:
                    index_even.append(i)
        return index_even

    def duplication_3(self, player_only_num):
        # 3枚ある場合
        dup_3 = []
        for x in set(player_only_num):
            if player_only_num.count(x) == 3:
                dup_3.append(x)
        # ３枚ある数字を抜き出す
        index_3 = []
        for i, x in enumerate(player_only_num):
            for h in dup_3:
                if x == h:
                    index_3.append(i)
        # 重複しているindexを取得
        index_3_t = []
        for i in dup_3:
            t = player_only_num.index(i)
            index_3_t.append(t)
        result_3 = list(filter(lambda x: x not in index_3_t, index_3))
        return result_3

    def index_total(self, player_only_num, player_cards):
        rules = Rules()
        index_2_4 = rules.duplication_2_4(player_only_num)
        index_3 = rules.duplication_3(player_only_num)
        total_index = index_2_4 + index_3
        for i in sorted(total_index, reverse=True):
            player_cards.pop(i)
        return player_cards


class Game(CreateCard):
    def __init__(self):
        super().__init__()

        # ババ抜きを始めます。
        first_message = console.get_template("start_game.txt", "red")
        print(first_message)

        # 何人で遊びますか？
        how_many = console.get_template('how_many.txt', 'green')
        num = int(input(how_many))
        self.num = num

        # 名前を入力してください。
        type_name = console.get_template('type_name.txt', 'green')
        print(type_name)
        player_name = []
        for i in range(num):
            player_name.append(input('Player{} : '.format(i + 1)))
        self.player_names = player_name

    def deal(self):
        deal_cards = console.get_template("deal_cards.txt", "green")
        print(deal_cards)
        time.sleep(.3)
        players_cards = []
        for i in range(self.num):
            players_cards.append([])
        while len(self.sv_list) > 0:
            for player_cards in players_cards:
                player_cards.append(self.sv_list.pop())
                if len(self.sv_list) == 0:
                    break
        self.players_cards = players_cards
        for (name, player) in zip(self.player_names, self.players_cards):
            print(name + " : " + ",  ".join(player))

    def first_discard(self):
        discard_pair = console.get_template('discard_pair.txt', 'green')
        print(discard_pair)
        time.sleep(.3)

        players_only_num = []
        results_list = []
        for i in range(self.num):
            players_only_num.append([])
        for (player_cards, player_only_num) in zip(self.players_cards,
                                                   players_only_num):
            for i in player_cards:
                t = i[:2]
                player_only_num.append(t)

        for (player_only_num, name, player_cards) in zip(
                players_only_num, self.player_names, self.players_cards):

            # 重複削除
            rules = Rules()
            player_card = rules.index_total(player_only_num, player_cards)
            results_list.append(player_card)
            self.results_list = results_list
            print(name + " :  " + ",  ".join(player_card))

    def turn(self):
        # 名前とカードを紐づけるために辞書化
        dict_deck = dict(zip(self.player_names, self.results_list))
        decide_order = console.get_template('decide_order.txt', 'green')
        print(decide_order)
        time.sleep(.5)
        # self.players_order = random.sample(self.player_names, len(self.player_names))
        self.players_order = self.player_names
        self.dict_deck = dict_deck
        print(' → '.join(self.players_order))

    def play_game(self):
        # 途中経過表示
        def print_result():
            for player in self.dict_deck:
                if "Done!" in self.dict_deck[player]:
                    print(player + " : " + ''.join(self.dict_deck[player]))
                else:
                    print(player + " : " + ",  ".join(self.dict_deck[player]))
        self.ranking_list = []

        # 重複削除
        def dup(dict_deck, players_order, n, ranking_list):
            print("\nDiscard if you have a pair: ")
            player_sub = []
            for i in dict_deck[players_order[n]]:
                # 数字のみ取得するため、２文字目までを取得する
                t = i[:2]
                player_sub.append(t)

            rules = Rules()
            player_card = rules.index_total(player_sub,
                                            dict_deck[players_order[n]])

            # 空になった場合
            if not player_card:
                key = [k for k, v in dict_deck.items() if v == []][0]
                dict_deck[key] = 'Done!'
                ranking_list.append(key)
                print_result()

            else:
                print_result()

        # カードを引く
        def pull():
            print(self.players_order[n] + "  pulls  " + self.players_order[m])
            random.shuffle(self.dict_deck[self.players_order[m]])
            self.dict_deck[self.players_order[n]].append(
                self.dict_deck[self.players_order[m]].pop())

        # カード引かれる
        def pulled():
            if not self.dict_deck[self.players_order[m]]:
                key = [k for k, v in self.dict_deck.items() if v == []][
                    0]
                self.dict_deck[key] = "Done!"
                self.ranking_list.append(key)
                print_result()
            else:
                print_result()

        # 各ターンの動き
        turn = 1
        n = -1
        while list(self.dict_deck.values()).count('Done!') < self.num - 1:
            print('\n=== Turn{} =================='.format(turn))
            turn += 1
            n += 1
            if n == self.num:
                n = 0
            if n == self.num - 1:
                n = -1
            m = n + 1

            if self.dict_deck[self.players_order[n]] != 'Done!' and \
                    self.dict_deck[self.players_order[m]] != 'Done!':
                pull()
                pulled()
                dup(self.dict_deck, self.players_order, n, self.ranking_list)

            else:
                while True:
                    if self.dict_deck[self.players_order[n]] != 'Done!':
                        break
                    n += 1
                    if self.dict_deck[self.players_order[n]] != 'Done!':
                        break
                while True:
                    if m == self.num - 1:
                        m = -1
                    m += 1
                    if self.dict_deck[self.players_order[m]] != 'Done!':
                        if m == n:
                            continue
                        if m != n:
                            break
                pull()
                pulled()
                dup(self.dict_deck, self.players_order, n, self.ranking_list)

            if list(self.dict_deck.values()).count('Done!') == self.num - 1:
                break

    def final_result(self):
        print('\n{:=^30}'.format('Final-Result'))
        for i, name in enumerate(self.ranking_list):
            print("{}位: {}".format(i+1, name))
        n = list(filter(lambda x: x not in self.ranking_list, self.players_order))[0]
        print("{}位: {}".format(self.num, n))
