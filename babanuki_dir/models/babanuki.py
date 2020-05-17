import time
import random

from babanuki_dir.views import console


class CreateCard(object):
    def __init__(self):
        suits = ["s", "h", "d", "c"]
        sv_list = []
        for i in range(1, 14):
            for j in suits:
                sv_list.append(str(i) + "_" + j)
        sv_list.append("BABA")
        random.shuffle(sv_list)
        self.sv_list = sv_list


class Game(CreateCard):
    def __init__(self):
        super().__init__()
        first_message = console.get_template("start_game.txt", "red")
        print(first_message)
        self.name1 = "A"
        self.name2 = "B"
        self.name3 = "C"
        print("Player1: A")
        print("Player2: B")
        print("Player3: C")
        self.names = [self.name1, self.name2, self.name3]

    def deal(self):
        self.player1 = []
        self.player2 = []
        self.player3 = []
        self.players = [self.player1, self.player2, self.player3]
        print("\nカードを配ります(y/n) : ")
        time.sleep(.3)
        while len(self.sv_list) > 0:
            for player in self.players:
                player.append(self.sv_list.pop())
                if len(self.sv_list) == 0:
                    break

        for (name, player) in zip(self.names, self.players):
            print(name + ":  " + ",  ".join(player))
            # print("player; ", player)

    def first_discard(self):
        # y = input("\nDiscard if you have a pair : ")
        print("\nDiscard if you have a pair : ")
        player1_num = []
        player2_num = []
        player3_num = []
        players_num = [player1_num, player2_num, player3_num]
        # if y == "y":
        time.sleep(.3)
        for (player, player_num) in zip(self.players, players_num):
            for i in player:
                t = i[:2]
                player_num.append(t)
        self.results_list = []
        for (player_num, name, player) in zip(
                players_num, self.names, self.players):
            # 偶数枚の場合
            dup_2_4 = []
            for x in set(player_num):
                if player_num.count(x) == 2 or player_num.count(x) == 4:
                    dup_2_4.append(x)

            # まず偶数枚の数字を抜き出す
            result_2_4 = list(filter(lambda x: x in dup_2_4, player_num))

            # 重複しているindexを取得
            c_index_2_4 = []
            for i, x in enumerate(player_num):
                for h in result_2_4:
                    if x == h:
                        c_index_2_4.append(i)
            c_index_2_4 = list(set(c_index_2_4))

            # 3枚ある場合
            dup_3 = []
            for x in set(player_num):
                if player_num.count(x) == 3:
                    dup_3.append(x)

            # ３枚ある数字を抜き出す
            result_3 = list(filter(lambda x: x in dup_3, player_num))
            c_index_3 = []
            for i, x in enumerate(player_num):
                for h in result_3:
                    if x == h:
                        c_index_3.append(i)
            c_index_3 = list(set(c_index_3))

            # 重複しているindexを取得
            result_3_t = list(set(result_3))
            c_index_3_t = []
            for i in result_3_t:
                t = player_num.index(i)
                c_index_3_t.append(t)
            result_3 = list(filter(lambda x: x not in c_index_3_t, c_index_3))

            # （２枚、４枚）と（３枚）のインデックスのリストを足し合わせる
            last_index = c_index_2_4 + result_3

            for i in sorted(last_index, reverse=True):
                player.pop(i)

            self.results_list.append(player)

            print(name + "さん" + " :  " + ",  ".join(player))

    def turn(self):
        # 名前とカードを紐づけるために辞書化
        self.n_r_dict = dict(zip(self.names, self.results_list))
        # y = input("\nランダムで順番を決めます(y/n) : ")
        print("\nランダムで順番を決めます(y/n) : ")
        # if y == "y":
        time.sleep(.5)
        random.shuffle(self.names)
        print("{0[0]} →→ {0[1]} →→ {0[2]}".format(self.names))

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
                    # y = input("\n" + self.names[n] + "さんが" + self.names[m]
                    #           + "さんのカードをひいてください。(y/n): ")
                    print("\n" + self.names[n] + "さんが" + self.names[m] + "さんのカードをひいてください。(y/n): ")
                    # if y == "y":
                    time.sleep(.5)
                    random.shuffle(self.n_r_dict[self.names[m]])
                    self.n_r_dict[self.names[n]].append(self.n_r_dict[self.names[m]].pop())
                    if self.n_r_dict[self.names[m]] == []:
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
                    for i in self.n_r_dict[self.names[n]]:
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
                        self.n_r_dict[self.names[n]].pop(i)
                    # print("self.n_r_dict[self.names[n]]; ", self.n_r_dict[self.names[n]])
                    ########################################################################
                    if self.n_r_dict[self.names[n]] == []:
                        key = [k for k,v in self.n_r_dict.items() if v == []][0]
                        #print(key)
                        self.n_r_dict[key] = "①"
                        print_result()

                    else:
                        print_result()

                elif self.n_r_dict[self.names[n]] == "①":
                    n = (i + 4) % 3
                    m = (i + 5) % 3

                    while '②' not in list(self.n_r_dict.values()):
                        for a, b in [[n, m], [m, n]]:
                            # y = input("\n" + self.names[a] + "さんが" + self.names[b] + "さんのカードをひいてください。(y/n): ")
                            print("\n" + self.names[a] + "さんが" + self.names[b] + "さんのカードをひいてください。(y/n): ")
                            # if y == "y":
                            time.sleep(.5)
                            random.shuffle(self.n_r_dict[self.names[b]])
                            self.n_r_dict[self.names[a]].append(self.n_r_dict[self.names[b]].pop(0))
                            if self.n_r_dict[self.names[b]] == []:
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
                            for i in self.n_r_dict[self.names[a]]:
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
                                self.n_r_dict[self.names[a]].pop(i)
                            # print("self.n_r_dict[self.names[n]]; ", self.n_r_dict[self.names[n]])
                            ########################################################################
                            if self.n_r_dict[self.names[a]] == []:
                                key = [k for k, v in self.n_r_dict.items() if v == []][0]
                                #print(key)
                                self.n_r_dict[key] = "②"
                                print_result()
                                break

                            else:
                                print_result()


                elif self.n_r_dict[self.names[(n + 2) % 3]] == "①":
                    n = (i + 3) % 3
                    m = (i + 4) % 3
                    while '②' not in list(self.n_r_dict.values()):
                        for a, b in [[n, m], [m, n]]:
                            # y = input("\n" + self.names[a] + "さんが" + self.names[b] + "さんのカードをひいてください。(y/n): ")
                            print("\n" + self.names[a] + "さんが" + self.names[b] + "さんのカードをひいてください。(y/n): ")
                            # if y == "y":
                            time.sleep(.5)
                            self.n_r_dict[self.names[a]].append(self.n_r_dict[self.names[b]].pop(0))
                            if self.n_r_dict[self.names[b]] == []:
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
                            for i in self.n_r_dict[self.names[a]]:
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
                                self.n_r_dict[self.names[a]].pop(i)
                            if self.n_r_dict[self.names[a]] == []:
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

        print('{:^30}'.format('Final-Result'))
        print("1位: {} さん".format(key_1))
        print("2位: {} さん".format(key_2))
        print("3位: {} さん".format(key_3))




