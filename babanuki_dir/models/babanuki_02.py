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
        type_name = console.get_template('type_name.txt', 'blue')
        print(type_name)
        player_name = []
        for i in range(num):
            player_name.append(input('Player{}: '.format(i+1)))
        self.player_names = player_name

    def deal(self):
        deal_cards = console.get_template("deal_cards.txt", "blue")
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
            print(name + ":  " + ",  ".join(player))

    def first_discard(self):
        discard_pair = console.get_template('discard_pair.txt', 'blue')
        print(discard_pair)
        time.sleep(.3)

        players_only_num = []
        for i in range(self.num):
            players_only_num.append([])
        for (player_cards, player_only_num) in zip(self.players_cards, players_only_num):
            for i in player_cards:
                t = i[:2]
                player_only_num.append(t)
        for (player_only_num, name, player_cards) in zip(
                players_only_num, self.player_names, self.players_cards):
            # 偶数枚の場合
            dup_even = []
            for x in set(player_only_num):
                if player_only_num.count(x) == 2 or player_only_num.count(x) == 4:
                    dup_even.append(x)

            # まず偶数枚の数字を抜き出す
            result_even = list(filter(lambda x: x in dup_even, player_only_num))

            # 重複しているindexを取得
            index_even = []
            for i, x in enumerate(player_only_num):
                for h in result_even:
                    if x == h:
                        index_even.append(i)
            index_even = list(set(index_even))

            # 3枚ある場合
            dup_3 = []
            for x in set(player_only_num):
                if player_only_num.count(x) == 3:
                    dup_3.append(x)

            # ３枚ある数字を抜き出す
            result_3 = list(filter(lambda x: x in dup_3, player_only_num))
            c_index_3 = []
            for i, x in enumerate(player_only_num):
                for h in result_3:
                    if x == h:
                        c_index_3.append(i)
            c_index_3 = list(set(c_index_3))

            # 重複しているindexを取得
            result_3_t = list(set(result_3))
            c_index_3_t = []
            for i in result_3_t:
                t = player_only_num.index(i)
                c_index_3_t.append(t)
            result_3 = list(filter(lambda x: x not in c_index_3_t, c_index_3))

            # （２枚、４枚）と（３枚）のインデックスのリストを足し合わせる
            last_index = index_even + result_3

            for i in sorted(last_index, reverse=True):
                player_cards.pop(i)
            self.results_list = []
            self.results_list.append(player_cards)

            print(name + " :  " + ",  ".join(player_cards))

    def turn(self):
        # 名前とカードを紐づけるために辞書化
        n_r_dict = dict(zip(self.player_names, self.results_list))
        decide_order = console.get_template('decide_order.txt', 'blue')
        print(decide_order)
        time.sleep(.5)
        random.shuffle(self.player_names)
        print(' → '.join(self.player_names))

        self.n_r_dict = n_r_dict

    def play_game(self):
        def print_result():
            print(self.name1 + " :  " + ", ".join(self.n_r_dict[self.name1]))
            print(self.name2 + " :  " + ", ".join(self.n_r_dict[self.name2]))
            print(self.name3 + " :  " + ", ".join(self.n_r_dict[self.name3]))

        while ["BABA"] not in list(self.n_r_dict.values()):
            for i in range(0,3):
                n = (i + 3) % 3
                m = (i + 4) % 3
                if "①" not in list(self.n_r_dict.values()):
                    # y = input("\n" + self.player_names[n] + "さんが" + self.player_names[m]
                    #           + "さんのカードをひいてください。(y/n): ")
                    print("\n" + self.player_names[n] + "さんが" + self.player_names[m] + "さんのカードをひいてください。(y/n): ")
                    # if y == "y":
                    time.sleep(.5)
                    random.shuffle(self.n_r_dict[self.player_names[m]])
                    self.n_r_dict[self.player_names[n]].append(self.n_r_dict[self.player_names[m]].pop())
                    if self.n_r_dict[self.player_names[m]] == []:
                        key = [k for k, v in self.n_r_dict.items() if v == []][0]
                        print(key)
                        self.n_r_dict[key] = "①"
                        print_result()
                    else:
                        print_result()
                    # y = input("\nDiscard if you have a pair (y/n): ")
                    print("\nDiscard if you have a pair (y/n): ")
                    # if y == "y":
                    time.sleep(.5)
                        #####################################################################
                    player_sub = []
                    for i in self.n_r_dict[self.player_names[n]]:
                        t = i[:2]  # 数字のみ取得するため、２文字目までを取得する
                        player_sub.append(t)
                    # print("player_sub; ", player_sub)
                    # 偶数枚の場合
                    dup_2_4 = []
                    for x in set(player_sub):
                        if player_sub.count(x) == 2:
                            dup_2_4.append(x)
                    # print("dup_2_4: ", dup_2_4)

                    # まず偶数枚の数字を抜き出す
                    result_2_4 = list(filter(lambda x: x in dup_2_4, player_sub))
                    # print("result_2_4; ", result_2_4)

                    # 重複しているindexを取得
                    c_index_2_4 = []
                    for i, x in enumerate(player_sub):
                        for h in result_2_4:
                            if x == h:
                                c_index_2_4.append(i)
                    c_index_2_4 = list(set(c_index_2_4))
                    # print("c_index_2_4; ", c_index_2_4)

                    for i in sorted(c_index_2_4, reverse=True):
                        self.n_r_dict[self.player_names[n]].pop(i)
                    # print("self.n_r_dict[self.player_names[n]]; ", self.n_r_dict[self.player_names[n]])
                    ########################################################################
                    if self.n_r_dict[self.player_names[n]] == []:
                        key = [k for k,v in self.n_r_dict.items() if v == []][0]
                        #print(key)
                        self.n_r_dict[key] = "①"
                        print_result()

                    else:
                        print_result()

                elif self.n_r_dict[self.player_names[n]] == "①":
                    n = (i + 4) % 3
                    m = (i + 5) % 3

                    while '②' not in list(self.n_r_dict.values()):
                        for a, b in [[n, m], [m, n]]:
                            # y = input("\n" + self.player_names[a] + "さんが" + self.player_names[b] + "さんのカードをひいてください。(y/n): ")
                            print("\n" + self.player_names[a] + "さんが" + self.player_names[b] + "さんのカードをひいてください。(y/n): ")
                            # if y == "y":
                            time.sleep(.5)
                            random.shuffle(self.n_r_dict[self.player_names[b]])
                            self.n_r_dict[self.player_names[a]].append(self.n_r_dict[self.player_names[b]].pop(0))
                            if self.n_r_dict[self.player_names[b]] == []:
                                key = [k for k, v in self.n_r_dict.items() if v == []][0]
                                print(key)
                                self.n_r_dict[key] = "②"
                                print_result()
                            else:
                                print_result()
                            # y = input("\nペアができれば捨ててください。(y/n): ")
                            print("\nペアができれば捨ててください。(y/n): ")
                            # if y == "y":
                            time.sleep(.5)
                            player_sub = []
                            for i in self.n_r_dict[self.player_names[a]]:
                                t = i[:2]  # 数字のみ取得するため、２文字目までを取得する
                                player_sub.append(t)
                            # print("player_sub; ", player_sub)
                            # 偶数枚の場合
                            dup_2_4 = []
                            for x in set(player_sub):
                                if player_sub.count(x) == 2:
                                    dup_2_4.append(x)
                            # print("dup_2_4: ", dup_2_4)

                            # まず偶数枚の数字を抜き出す
                            result_2_4 = list(filter(lambda x: x in dup_2_4, player_sub))
                            # print("result_2_4; ", result_2_4)

                            # 重複しているindexを取得
                            c_index_2_4 = []
                            for i, x in enumerate(player_sub):
                                for h in result_2_4:
                                    if x == h:
                                        c_index_2_4.append(i)
                            c_index_2_4 = list(set(c_index_2_4))
                            # print("c_index_2_4; ", c_index_2_4)

                            for i in sorted(c_index_2_4, reverse=True):
                                self.n_r_dict[self.player_names[a]].pop(i)
                            # print("self.n_r_dict[self.player_names[n]]; ", self.n_r_dict[self.player_names[n]])
                            ########################################################################
                            if self.n_r_dict[self.player_names[a]] == []:
                                key = [k for k, v in self.n_r_dict.items() if v == []][0]
                                #print(key)
                                self.n_r_dict[key] = "②"
                                print_result()
                                break

                            else:
                                print_result()


                elif self.n_r_dict[self.player_names[(n + 2) % 3]] == "①":
                    n = (i + 3) % 3
                    m = (i + 4) % 3
                    while '②' not in list(self.n_r_dict.values()):
                        for a, b in [[n, m], [m, n]]:
                            # y = input("\n" + self.player_names[a] + "さんが" + self.player_names[b] + "さんのカードをひいてください。(y/n): ")
                            print("\n" + self.player_names[a] + "さんが" + self.player_names[b] + "さんのカードをひいてください。(y/n): ")
                            # if y == "y":
                            time.sleep(.5)
                            self.n_r_dict[self.player_names[a]].append(self.n_r_dict[self.player_names[b]].pop(0))
                            if self.n_r_dict[self.player_names[b]] == []:
                                key = [k for k, v in self.n_r_dict.items() if v == []][0]
                                self.n_r_dict[key] = "②"
                                print_result()
                            else:
                                print_result()
                            # y = input("\nペアができれば捨ててください。(y/n): ")
                            print("\nペアができれば捨ててください。(y/n): ")
                            # if y == "y":
                            time.sleep(.5)
                            player_sub = []
                            for i in self.n_r_dict[self.player_names[a]]:
                                t = i[:2]  # 数字のみ取得するため、２文字目までを取得する
                                player_sub.append(t)
                            # print("player_sub; ", player_sub)
                            # 偶数枚の場合
                            dup_2_4 = []
                            for x in set(player_sub):
                                if player_sub.count(x) == 2:
                                    dup_2_4.append(x)
                            # print("dup_2_4: ", dup_2_4)

                            # まず偶数枚の数字を抜き出す
                            result_2_4 = list(filter(lambda x: x in dup_2_4, player_sub))
                            # print("result_2_4; ", result_2_4)

                            # 重複しているindexを取得
                            c_index_2_4 = []
                            for i, x in enumerate(player_sub):
                                for h in result_2_4:
                                    if x == h:
                                        c_index_2_4.append(i)
                            c_index_2_4 = list(set(c_index_2_4))
                            # print("c_index_2_4; ", c_index_2_4)

                            for i in sorted(c_index_2_4, reverse=True):
                                self.n_r_dict[self.player_names[a]].pop(i)
                            if self.n_r_dict[self.player_names[a]] == []:
                                key = [k for k, v in self.n_r_dict.items() if v == []][0]
                                self.n_r_dict[key] = "②"
                                print_result()
                                break

                            else:
                                print_result()

    def final_result(self):
        key_1 = [k for k, v in self.n_r_dict.items() if v == "①"][0]
        key_2 = [k for k, v in self.n_r_dict.items() if v == "②"][0]
        key_3 = [k for k, v in self.n_r_dict.items() if v == ["BABA"]][0]

        print("\n=====最終結果=====\n")
        print("1位: {} さん".format(key_1))
        print("2位: {} さん".format(key_2))
        print("3位: {} さん".format(key_3))




