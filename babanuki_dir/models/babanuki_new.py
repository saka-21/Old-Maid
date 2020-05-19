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

    # ペアがあれば捨ててください
    def delete_pair(self):
        print('\n=== Discard if you have pairs. ===')

# class Player(object):
#      def pull(self):





class Game(CreateCard):

    dealer = Dealer()
    dealer.start()
    dealer.how_many()
    dealer.what_is_your_name()
    dealer.deal()
    dealer.delete_pair()

Game()

