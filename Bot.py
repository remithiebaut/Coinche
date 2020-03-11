# -*- coding: utf-8 -*-
"""
Created on Wed Mar 27 22:34:33 2019

@author: rthie
"""
import coinche_constant as const
from Card import Card

class Bot:
  """
  AI Prototype which count cards each round
  """
  def __init__(self, cards, level="beginner"):
    self.hand={}
    self.betStrength={}
    self.level=level
    self.counter={}
    for color in const.liste_couleur[:4] :
      self.counter[color]=0
      self.hand[color]={}
      for number in const.liste_numero :
         self.hand[color][number] = False
    for card in cards:
        self.hand[card.color][card.number] = True
        self.counter[card.color] += 1
    for color in const.liste_couleur :
        self.betStrength[color] = 0
    self.updateBetStrength()


  def count(self, card):
    """
    call after each card is played
    """
    self.counter[card.color]+=1

  def reinitialize(self):
    """
    reinitialize for a new round
    """
    for color in self.counter:
      self.counter[color]=0

  def bet(self):
    """
    determine which trump to bet on
    """
    maxBet = 0
    betColor = ''
    # find highest bet above 80
    for color in self.betStrength :
      if self.betStrength[color] > maxBet and self.betStrength[color] > 80 :
        maxBet = self.betStrength[color]
        betColor = color

    if betColor == '' : #announce nothing
      return ([None,None])

    else: #announce something

      if maxBet%10==5: #if its between two announces
        maxBet-=5 #round to the inferior

      if maxBet>160:

        maxBet="capot" # TODO: add generale and take trump into account

      maxBet=str(maxBet) #convert to string

      return([maxBet,betColor]) #retourne none ???



  def updateBetStrength(self):
    """
    evaluate the strength of each bet
    """
    for trump in const.liste_couleur[:4] :
      #belote and number of trumps
      self.betStrength[trump] = 10 * self.counter[trump] + 20 * (self.hand[trump]['R'] and self.hand[trump]['D'])
      #search valet and 9
      if self.hand[trump]['V'] :
        if self.hand[trump]['9'] :
          self.betStrength[trump] += 60
        else :
          self.betStrength[trump] += 40
      elif self.hand[trump]['9'] :
        self.betStrength[trump] += 30
      #search for as and 10
      for color in const.liste_couleur[:4] :
        #as and 10
        if color != trump :
          if self.hand[color]['As'] :
            self.betStrength[trump] += 10 + 5 * self.hand[color]['10']
          elif self.hand[color]['10'] :
            #dry 10
            if self.counter[color] == 1 :
              self.betStrength[trump] -= 15
            else :
              self.betStrength[trump] += 5

    #sans atout
    for color in const.liste_couleur[:4] :
      if self.hand[color]['As'] :
        self.betStrength['sans atout'] += 25 + 15 * self.hand[color]['10'] + 5 * self.hand[color]['R']
      elif self.hand[color]['10'] :
        #dry 10
        if self.counter[color] == 1 :
          self.betStrength[trump] -= 10
        else :
          self.betStrength[trump] += 10


def test_update_bet_strength(): #random test
    testCards = [Card("D","carreau"), Card("As","trefle"), Card("V","coeur"), Card("9","coeur"),
                 Card("As","pique"), Card("10","pique"), Card("7","trefle"), Card("D","trefle")]

    testCards2 = [Card("8","coeur"), Card("7","coeur"), Card("R","coeur"), Card("9","coeur"),
                 Card("D","carreau"), Card("10","pique"), Card("7","trefle"), Card("D","trefle")]

    testCards3 = [Card("8","coeur"), Card("D","coeur"), Card("R","coeur"), Card("As","coeur"),
                 Card("D","carreau"), Card("As","pique"), Card("7","trefle"), Card("D","trefle")]

    testCards4 = [Card("As","coeur"), Card("D","coeur"), Card("10","coeur"), Card("As","trefle"),
                 Card("10","trefle"), Card("As","pique"), Card("7","trefle"), Card("D","trefle")]

    bot = Bot(testCards)
    print(bot.bet())
    print(bot.betStrength)


    bot = Bot(testCards2)
    print(bot.bet())
    print(bot.betStrength)

    bot = Bot(testCards3)
    print(bot.bet())
    print(bot.betStrength)

    bot = Bot(testCards4)
    print(bot.bet())
    print(bot.betStrength)


class AdvancedBot(Bot):
  """
  AI Prototype who keep track of previous games
  """
  def __init__(self, level="beginner"):
    Bot.__init__(self,level)
    self.previouscounter={} #keep track of the last round

  def reinitialize(self):
    """
    reinitialize for a new round
    """
    for color in self.counter:
      self.previouscounter[color]=self.counter[color]
    Bot.reinitialize(self)

  def findBestStreak(self, color) :
      #result=[longestStreak,highestStreakCard]
      result = [0,0]
      longestStreak = 0
      highestStreakCard = 0
      for card in self.hand[color] :
          if self.hand[color][card] :
              longestStreak += 1
              highestStreakCard = const.liste_numero.index(card)
          else :
              if highestStreakCard > result[1] :
                  result[0] = longestStreak
                  result[1] = highestStreakCard
              longestStreak = 0
              highestStreakCard = 0
      if highestStreakCard > result[1] :
                  result[0] = longestStreak
                  result[1] = highestStreakCard
      return result


if __name__=="__main__" :
  """
  card={}
  for color in const.liste_couleur[:4] :
    card[color]=Card("As",color)
  bob = Bot([Card("As",'trefle')])
  bob.count(card[const.liste_couleur[3]])
  assert(bob.counter[const.liste_couleur[3]]==1)

  bill = AdvancedBot()
  bill.counter
  bill.count(card[const.liste_couleur[2]])
  bill.count(card[const.liste_couleur[1]])
  assert(bill.counter[const.liste_couleur[2]]==1)
  assert(bill.counter[const.liste_couleur[1]]==1)
  bill.reinitialize()
  assert(bill.previouscounter[const.liste_couleur[2]]==1)
  assert(bill.previouscounter[const.liste_couleur[1]]==1)
  bill.count(card[const.liste_couleur[0]])
  assert(bill.counter[const.liste_couleur[0]]==1)
  assert(bill.previouscounter[const.liste_couleur[0]]==0)
  """
  print("Test OK")
  test_update_bet_strength()

