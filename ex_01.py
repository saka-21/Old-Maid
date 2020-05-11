import random


class AutoOldmaid:
    # カードの分配
    def preparation(self, playerNum):

        stock = [("Spade_A", 1), ("Spade_2", 2), ("Spade_3", 3), ("Spade_4", 4),
                 ("Spade_5", 5), ("Spade_6", 6), ("Spade_7", 7), ("Spade_8", 8),
                 ("Spade_9", 9), ("Spade_10", 10), ("Spade_J", 11),
                 ("Spade_Q", 12), ("Spade_K", 13),
                 ("Club_A", 1), ("Club_2", 2), ("Club_3", 3), ("Club_4", 4),
                 ("Club_5", 5), ("Club_6", 6), ("Club_7", 7), ("Club_8", 8),
                 ("Club_9", 9), ("Club_10", 10), ("Club_J", 11), ("Club_Q", 12),
                 ("Club_K", 13),
                 ("Diamond_A", 1), ("Diamond_2", 2), ("Diamond_3", 3),
                 ("Diamond_4", 4), ("Diamond_5", 5), ("Diamond_6", 6),
                 ("Diamond_7", 7), ("Diamond_8", 8), ("Diamond_9", 9),
                 ("Diamond_10", 10), ("Diamond_J", 11), ("Diamond_Q", 12),
                 ("Diamond_K", 13),
                 ("Heart_A", 1), ("Heart_2", 2), ("Heart_3", 3), ("Heart_4", 4),
                 ("Heart_5", 5), ("Heart_6", 6), ("Heart_7", 7), ("Heart_8", 8),
                 ("Heart_9", 9), ("Heart_10", 10), ("Heart_J", 11),
                 ("Heart_Q", 12), ("Heart_K", 13),
                 ("Joker", 0)]

        # 山札の準備
        random.shuffle(stock)

        # (playerNum)人のプレイヤーにカードを分配
        playerHand = [["Player{}".format(i)] for i in range(playerNum)]

        # この配り方のほうがリアルっぽい！
        while len(stock) != 0:
            for i in range(playerNum):
                # 各プレイヤーに同数のカードが配られない場合に必要。
                if len(stock) != 0:
                    playerHand[i].append(stock[0])
                    stock.pop(0)

                    # 手札の表示
        print("====== Preparation ======")
        self.showHands(playerNum, playerHand)
        self.deleteDuplicates(playerNum, playerHand)

    # 重複した手札の削除
    def deleteDuplicates(self, playerNum, playerHand):

        # iはプレイヤーの数(プレイヤーごとに手札を削除していく)
        for i in range(playerNum):
            # ｊは各プレイヤーの手札の枚数
            for j in range(len(playerHand[i])):
                val = playerHand[i][j][0]
                num = playerHand[i][j][1]

                for k in range(len(playerHand[i])):
                    if val != playerHand[i][k][0] and num == playerHand[i][k][
                        1]:
                        playerHand[i][j] = "Delete"
                        playerHand[i][k] = "Delete"
                        break

                        # filterにより重複していたものを削除
            playerHand[i] = list(filter(lambda x: x != "Delete", playerHand[i]))

        print("====== Delete Duplicates ======")
        self.showHands(playerNum, playerHand)
        self.mainGame(playerNum, playerHand)
        # 最初から上がっていた場合の処理を追加

    # メインゲーム
    def mainGame(self, playerNum, playerHand):

        rank = []
        game_loop = True
        turn = 1

        print("====== Game Start======")
        while game_loop:

            print("===== Turn {} ======".format(turn))

            # Gameの終了フラグ
            if playerNum == 1:
                print("====== Game Over ======")
                print("====== Ranking ======")
                rank.append(playerHand[0][0])
                self.ranking(rank)
                game_loop = False
                break

            # 各プレイヤーが手札を引いていく
            for i in range(playerNum):

                if i == playerNum - 1:
                    i = -1

                # 通常のループ
                if len(playerHand[i]) != 1 and len(playerHand[i + 1]) != 1:
                    player_choice_card = playerHand[i + 1][
                        random.randrange(1, len(playerHand[i + 1]))]
                    playerHand[i].insert(1, player_choice_card)
                    playerHand[i + 1].remove(player_choice_card)
                    print("{} Pull {}".format(playerHand[i][0],
                                              player_choice_card))

                    # ｊは各プレイヤーの手札の枚数
                    # 一枚ずつ調べ、重複するカードを削除。
                    for j in range(len(playerHand[i])):

                        val = player_choice_card[0]
                        num = player_choice_card[1]

                        if val != playerHand[i][j][0] and num == \
                                playerHand[i][j][1]:
                            print("====== Duplication ======")
                            print(playerHand[i][1])
                            print(playerHand[i][j])
                            playerHand[i][j] = "Delete"
                            playerHand[i][1] = "Delete"
                            break

                            # 重複したものを削除
                    playerHand[i] = list(
                        filter(lambda x: x != "Delete", playerHand[i]))

                    print("====== PlayerHand ======")
                    self.showHands(playerNum, playerHand)
                    print("========================")

                # あがった時の処理
                # 引いたヒト上がり
                if len(playerHand[i]) == 1 and len(playerHand[i + 1]) != 1:
                    rank.append(playerHand[i][0])
                    playerHand.pop(i)
                    subPlayerhand = playerHand[:]
                    playerHand.clear()
                    playerNum -= 1

                    for s in range(playerNum):
                        if i + s < playerNum:
                            playerHand.append(subPlayerhand[i + s])

                        elif i + s >= playerNum:
                            z = playerNum - i
                            playerHand.append(subPlayerhand[s - z])

                    print("引いた人上がり")
                    break

                # 引かれたヒト上がり
                elif len(playerHand[i]) != 1 and len(playerHand[i + 1]) == 1:
                    rank.append(playerHand[i + 1][0])
                    playerHand.pop(i + 1)
                    subPlayerhand = playerHand[:]
                    playerHand.clear()
                    playerNum -= 1

                    for s in range(playerNum):
                        if i + s < playerNum - 1:
                            playerHand.append(subPlayerhand[i + s + 1])

                        elif i + s >= playerNum - 1:
                            z = playerNum - i
                            playerHand.append(subPlayerhand[s - z + 1])

                    print("引かれた人上がり")
                    break

                # 2人同時上がり
                elif len(playerHand[i]) == 1 and len(playerHand[i + 1]) == 1:
                    rank.append(playerHand[i + 1][0])
                    rank.append(playerHand[i][0])
                    playerHand.pop(i + 1)
                    playerHand.pop(i)
                    subPlayerhand = playerHand[:]
                    playerHand.clear()
                    playerNum -= 2

                    for s in range(playerNum):

                        if i + s <= playerNum - 1:
                            playerHand.append(subPlayerhand[i + s])

                        elif i + s > playerNum - 1:
                            z = playerNum - i
                            playerHand.append(subPlayerhand[s - z])

                    print("二人同時上がり")
                    break

            print("====== Turn{} Finish ======".format(turn))
            print("Playing {}player".format(playerNum))
            turn += 1
            self.showHands(playerNum, playerHand)

    def ranking(self, ranking):
        for i in range(len(ranking)):
            print(ranking[i])

    def showHands(self, playerNum, playerHand):
        for i in range(playerNum):
            print(playerHand[i])


if __name__ == "__main__":
    playerNum = 5
    a = AutoOldmaid()
    a.preparation(playerNum)