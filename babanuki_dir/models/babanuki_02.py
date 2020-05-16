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


class Game(CreateCard):
    def __init__(self):
        # 親クラスの継承
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

            rules = Rules()
            index_even = rules.duplication_2_4(player_only_num)
            result_3 = rules.duplication_3(player_only_num)

            # （２枚、４枚）と（３枚）のインデックスのリストを足し合わせる
            last_index = index_even + result_3

            for i in sorted(last_index, reverse=True):
                player_cards.pop(i)
            results_list.append(player_cards)
            self.results_list = results_list

            print(name + " :  " + ",  ".join(player_cards))

    def turn(self):
        # 名前とカードを紐づけるために辞書化
        dict_deck = dict(zip(self.player_names, self.results_list))
        decide_order = console.get_template('decide_order.txt', 'green')
        print(decide_order)
        time.sleep(.5)
        self.players_order = random.sample(self.player_names, len(self.player_names))
        print(' → '.join(self.players_order))
        self.dict_deck = dict_deck

    def play_game(self):
        def print_result():
            for (name, player) in zip(self.player_names, self.dict_deck):
                print(name + " : " + ",  ".join(self.dict_deck[name]))

        while ["BABA"] not in list(self.dict_deck.values()):
            for i in range(self.num):
                n = (i + self.num) % self.num
                m = (i + self.num + 1) % self.num
                
                if "①" not in list(self.dict_deck.values()):
                    print(
                        "\n" + self.players_order[n] + " pulls " + self.players_order[
                            m] + "'s cards")
                    time.sleep(.5)
                    random.shuffle(self.dict_deck[self.players_order[m]])
                    self.dict_deck[self.players_order[n]].append(
                        self.dict_deck[self.players_order[m]].pop())
                    if self.dict_deck[self.players_order[m]] == []:
                        key = [k for k, v in self.dict_deck.items() if v == []][
                            0]
                        print(key)
                        self.dict_deck[key] = "①"
                        print_result()
                    else:
                        print_result()

                    print("\nDiscard if you have a pair: ")
                    time.sleep(.5)

                    # 重複削除
                    player_sub = []
                    for i in self.dict_deck[self.players_order[n]]:
                        t = i[:2]  # 数字のみ取得するため、２文字目までを取得する
                        player_sub.append(t)

                    rules = Rules()
                    index_even = rules.duplication_2_4(player_sub)

                    for i in sorted(index_even, reverse=True):
                        self.dict_deck[self.players_order[n]].pop(i)

                    # 空になった場合
                    if self.dict_deck[self.players_order[n]] == []:
                        key = [k for k, v in self.dict_deck.items() if v == []][
                            0]
                        self.dict_deck[key] = "①"
                        print_result()

                    else:
                        print_result()

                elif self.dict_deck[self.players_order[n]] == "①":
                    n = (i + 4) % 3
                    m = (i + 5) % 3

                    while '②' not in list(self.dict_deck.values()):
                        for a, b in [[n, m], [m, n]]:
                            print("\n" + self.players_order[a] + "さんが" +
                                  self.players_order[
                                      b] + "さんのカードをひいてください。(y/n): ")
                            time.sleep(.5)
                            random.shuffle(self.dict_deck[self.players_order[b]])
                            self.dict_deck[self.players_order[a]].append(
                                self.dict_deck[self.players_order[b]].pop(0))
                            if self.dict_deck[self.players_order[b]] == []:
                                key = [k for k, v in self.dict_deck.items() if
                                       v == []][0]
                                print(key)
                                self.dict_deck[key] = "②"
                                print_result()
                            else:
                                print_result()
                            print("\nペアができれば捨ててください。(y/n): ")
                            time.sleep(.5)

                            # 重複削除
                            player_sub = []
                            for i in self.dict_deck[self.players_order[n]]:
                                t = i[:2]  # 数字のみ取得するため、２文字目までを取得する
                                player_sub.append(t)

                            rules = Rules()
                            index_even = rules.duplication_2_4(player_sub)

                            for i in sorted(index_even, reverse=True):
                                self.dict_deck[self.players_order[a]].pop(i)

                            # 空になった場合
                            if self.dict_deck[self.players_order[a]] == []:
                                key = [k for k, v in self.dict_deck.items() if
                                       v == []][0]
                                # print(key)
                                self.dict_deck[key] = "②"
                                print_result()
                                break

                            else:
                                print_result()


                elif self.dict_deck[self.players_order[(n + 2) % 3]] == "①":
                    n = (i + 3) % 3
                    m = (i + 4) % 3
                    while '②' not in list(self.dict_deck.values()):
                        for a, b in [[n, m], [m, n]]:
                            print("\n" + self.players_order[a] + "さんが" +
                                  self.players_order[
                                      b] + "さんのカードをひいてください。(y/n): ")
                            time.sleep(.5)
                            self.dict_deck[self.players_order[a]].append(
                                self.dict_deck[self.players_order[b]].pop(0))
                            if self.dict_deck[self.players_order[b]] == []:
                                key = [k for k, v in self.dict_deck.items() if
                                       v == []][0]
                                self.dict_deck[key] = "②"
                                print_result()
                            else:
                                print_result()
                            print("\nペアができれば捨ててください。(y/n): ")
                            time.sleep(.5)

                            # 重複削除
                            player_sub = []
                            for i in self.dict_deck[self.players_order[n]]:
                                t = i[:2]  # 数字のみ取得するため、２文字目までを取得する
                                player_sub.append(t)

                            rules = Rules()
                            index_even = rules.duplication_2_4(player_sub)

                            for i in sorted(index_even, reverse=True):
                                self.dict_deck[self.players_order[a]].pop(i)
                            if self.dict_deck[self.players_order[a]] == []:
                                key = [k for k, v in self.dict_deck.items() if
                                       v == []][0]
                                self.dict_deck[key] = "②"
                                print_result()
                                break

                            else:
                                print_result()

    def final_result(self):
        key_1 = [k for k, v in self.dict_deck.items() if v == "①"][0]
        key_2 = [k for k, v in self.dict_deck.items() if v == "②"][0]
        key_3 = [k for k, v in self.dict_deck.items() if v == ["BABA"]][0]

        print("\n=====最終結果=====\n")
        print("1位: {} さん".format(key_1))
        print("2位: {} さん".format(key_2))
        print("3位: {} さん".format(key_3))
