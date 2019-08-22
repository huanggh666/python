import os
import collections
import random

# print('♠ ♣ ♦ ♥')
Card = collections.namedtuple("Card",['rank','suit'])
class PMap:
    play_map = [['*']*82]
    play_map.extend([['*']+[' ']*80+['*'] for i in range(20)])
    play_map.extend([['*']*82])
    play_map[2][41] = 'A'
    play_map[11][12] = 'D'
    play_map[11][69] = 'B'
    play_map[19][41] = 'C'
    play_map[11][39:44] = list('GAMES')
    m = play_map.copy()
    
    @classmethod
    def init_map(cls):
        cls.m = cls.play_map.copy()
    
    @classmethod
    def play(cls, player_name, x):
        if x == 'win':
            cls.init_map()
            x = f'The winner is {player_name}'
            cls.m[11][33:48] = list(x)
            cls.print_map()
            return
        l = len(x)
        if l < 10:
            fore = (10-l)//2
            xac = ' '*fore + x + ' '*(10-l-fore)
            xb = ' '*(10-l) + x
            xd = x + ' '*(10-l)
        else:
            xac = xb = xd = x[:10]
        if player_name == 'A':
            cls.m[4][36:46] = list(xac)
        elif player_name == 'C':
            cls.m[17][36:46] = list(xac)
        elif player_name == 'B':
            cls.m[11][57:67] = list(xb)
        elif player_name == 'D':
            cls.m[11][14:24] = list(xd)
        cls.print_map()
    
    @classmethod
    def print_map(cls):
        os.system('cls')
        strls = '\n'.join([''.join(x) for x in cls.m])
        print(strls)

class FrenchDeck:
    ranks = [str(n) for n in range(2,11)] + list('jQKA')
    suits = 'spades clubs diamonds hearts'.split()
    suit_dict = dict(spades='♠',clubs='♣',diamonds='♦',hearts='♥')
    
    def __init__(self):
        self._cards = [Card(rank, suit) for suit in self.suits for rank in self.ranks]
        
    def __len__(self):
        return len(self._cards)
        
    def __getitem__(self, idx):
        return self._cards[idx]
        
    @classmethod
    def compete(cls, card1, card2):
        rank1 = cls.ranks.index(card1.rank)
        rank2 = cls.ranks.index(card2.rank)
        if rank1 < rank2:
            return 2
        elif rank1 > rank2:
            return 1
        elif rank1 == rank2:
            suit1 = cls.suits.index(card1.suit)
            suit2 = cls.suits.index(card2.suit)
            if suit1 < suit2:
                return 2
            else:
                return 1
        
    @classmethod
    def printx(cls, x):
        if isinstance(x, str):
            print(x)
        else:
            print(x.rank, cls.suit_dict[x.suit], sep='')
        
    @classmethod
    def get_print(cls, x):
        if isinstance(x, str):
            return x
        else:
            return f'{x.rank}{cls.suit_dict[x.suit]}'
               
class Player():
    def __init__(self, name='A', cards=[]):
        self.name = name
        self.cards = sorted(cards, key=lambda x:FrenchDeck.ranks.index(x[0]))
        
    def add_card(self, card):
        self.cards.append(card)
        
    def start(self):
        # print(f'Turn:{self.name}, start')
        PMap.play(self.name, ' start  ')
        for i in range(len(self.cards)):
            print(f'{i}:{self.cards[i].rank}'
                  f'{FrenchDeck.suit_dict[self.cards[i].suit]}', end='; ')
        print()
        while True:
            idx = input()
            if idx == '':
                continue
            idx = int(idx)
            if idx <= i:
                card = self.cards.pop(idx)
                if len(self.cards) == 0:
                    return 'win'
                else:
                    return card
        
    def subtract_card(self, fore_card):
        # print(f'Turn:{self.name}, continue')
        PMap.play(self.name, 'continue')
        for i in range(len(self.cards)):
            print(f'{i}:{self.cards[i].rank}'
                  f'{FrenchDeck.suit_dict[self.cards[i].suit]}', end='; ')
        print()
        while True:
            idx = input()
            if idx == '':
                return 'pass'
            idx = int(idx)
            if idx <= i:
                compete = FrenchDeck.compete(fore_card, self.cards[idx])
                if compete == 2:
                    res = self.cards.pop(idx)
                    if len(self.cards) == 0:
                        return 'win'
                    return res
                elif compete == 1:
                    print(f'Can not play ', end='')
                    FrenchDeck.printx(self.cards[idx])
                    continue
                    
class Game():
    def __init__(self):
        fd = FrenchDeck()
        random.shuffle(fd._cards)
        ls_idxs = [fd[i:i+13] for i in range(0,52,13)]
        self.players = [Player(x, ls_idxs[i]) for i,x in enumerate('ABCD')]
        
    def play(self):
        idx = random.randint(0,3)
        card = self.players[idx].start()
        PMap.play(self.players[idx].name, FrenchDeck.get_print(card))
        pass_num = 0
        while True:
            idx += 1
            res = self.players[idx%4].subtract_card(card)
            if res == 'pass':
                PMap.play(self.players[idx%4].name, res)
                pass_num += 1
                if pass_num == 3:
                    idx += 1
                    res = self.players[idx%4].start()
                    pass_num = 0
            else:
                pass_num = 0
            PMap.play(self.players[idx%4].name, FrenchDeck.get_print(res))
            if res == 'win':
                PMap.play(self.players[idx%4].name, res)
                break
            elif res != 'pass':
                card = res


if __name__ == '__main__':
    game = Game()
    game.play()

