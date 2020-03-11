# -*- coding: utf-8 -*-
"""
Created on Wed Mar 11 16:22:11 2020

@author: rthie
"""
import coinche_constant as const
from Card import Card
from Bot import Bot
from generical_function import test

class AdvancedBot(Bot):
  """
  AI Prototype who keep track of previous games
  """
  def __init__(self,cards, level="advanced",name="j1",allyName="j3",ennemyNames=["j2","j4"]):

    Bot.__init__(self,cards=cards,level=level,name=name,allyName=allyName,ennemyNames=ennemyNames)
    self.previouscounter={} #keep track of the last round
    self.announcetracker={}
    for color in const.liste_couleur :
      self.announcetracker[color]=False


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

  def adaptBetStrength(self,PartnerBet,BetColor):
    """
    adapt its bet strength according to his partner announce
    """

    #Assert that our partner announce something
    if PartnerBet != None :

      #update strength only if the bot hasnt already said something in this color
      if not self.announcetracker[BetColor] :

        if PartnerBet!="generale" and PartnerBet!="capot" : # TODO : adapt this method to the capot and generale cases
          self.betStrength[BetColor]+=int(PartnerBet)

  def coinche(self,AdversaryBet,BetColor):
    """
    Coinche if its strength in this color is higher than 160 minus the adversary bet
    """

    #Assert that our adversary announce something
    assert( AdversaryBet != None)

    if AdversaryBet!="generale" and AdversaryBet!="capot" : # TODO : adapt this method to the capot and generale cases

      #Strong enough to Coinche
      if self.betStrength[BetColor]>160-int(AdversaryBet) : # TODO : adapt this method to the belote case
        return True

      #Too weak to Coinche
      return False

    return False # TODO : adapt this method to the capot and generale cases

def test_adaptBetStrength(): #random test
  testCards1 = [Card("D","carreau"), Card("As","trefle"), Card("V","coeur"), Card("9","coeur"),
               Card("As","pique"), Card("10","pique"), Card("7","trefle"), Card("D","trefle")]

  testCards2 = [Card("8","coeur"), Card("7","coeur"), Card("R","coeur"), Card("9","coeur"),
               Card("D","carreau"), Card("10","pique"), Card("7","trefle"), Card("D","trefle")]

  testCards3 = [Card("8","coeur"), Card("D","coeur"), Card("R","coeur"), Card("As","coeur"),
               Card("D","carreau"), Card("As","pique"), Card("7","trefle"), Card("D","trefle")]

  testCards4 = [Card("As","coeur"), Card("D","coeur"), Card("10","coeur"), Card("As","trefle"),
               Card("10","trefle"), Card("As","pique"), Card("7","trefle"), Card("D","trefle")]

  bots =[AdvancedBot(testCards1),AdvancedBot(testCards2),AdvancedBot(testCards3),AdvancedBot(testCards4)]

  print("Bets before partner : ", end="\n"*2)

  bets_before=[]
  i=0
  for bot in bots :
    print("Bet of bot {} :".format(i))
    bets_before.append(bot.bet())
    print(bot.bet())
    print(bot.betStrength, end="\n"*2)
    i+=1

  print("Bets after partner : ", end="\n"*2)

  i=0
  for bot in bots :
    # (2 - i + 2* (i%2)) tricks to get the number of our friend
    bot.adaptBetStrength(bets_before[2 - i + 2* (i%2)][0],bets_before[2 - i + 2* (i%2)][1])
    print("Bet of bot {} :".format(i))
    print(bot.bet())
    print(bot.betStrength, end="\n"*2)
    i+=1

def test_coinche(): #random test
  testCards1 = [Card("D","carreau"), Card("As","trefle"), Card("V","coeur"), Card("9","coeur"),
               Card("As","pique"), Card("10","pique"), Card("7","trefle"), Card("D","trefle")]

  testCards2 = [Card("8","coeur"), Card("7","coeur"), Card("R","coeur"), Card("9","coeur"),
               Card("D","carreau"), Card("10","pique"), Card("7","trefle"), Card("D","trefle")]

  testCards3 = [Card("8","coeur"), Card("D","coeur"), Card("R","coeur"), Card("As","coeur"),
               Card("D","carreau"), Card("As","pique"), Card("7","trefle"), Card("D","trefle")]

  testCards4 = [Card("As","coeur"), Card("D","coeur"), Card("10","coeur"), Card("As","trefle"),
               Card("10","trefle"), Card("As","pique"), Card("7","trefle"), Card("D","trefle")]

  bots =[AdvancedBot(testCards1),AdvancedBot(testCards2),AdvancedBot(testCards3),AdvancedBot(testCards4)]

  print("Bets : ", end="\n"*2)

  bets_before=[]
  i=0
  for bot in bots :
    print("Bet of bot {} :".format(i))
    bets_before.append(bot.bet())
    print(bot.bet())
    print(bot.betStrength, end="\n"*2)
    i+=1

  print("Bets after partner : ", end="\n"*2)

  i=0
  for bot in bots :
    # (i+2)%4 tricks to get the number of our friend
    bot.adaptBetStrength(bets_before[(i+2)%4][0],bets_before[(i+2)%4][1])
    print("Bet of bot {} :".format(i))
    bet,betcolor=bot.bet()
    print(bet,betcolor)
    print(bot.betStrength, end="\n"*2)

    print("Coinche ", end="\n"*2)

    # (i+1)%4 or (i+3)%4  tricks to get the number of our friend

    for adversary in [1,3] :

      print(bots[(i+adversary)%4].betStrength)
      print("bot {} coinche : ".format((i+adversary)%4), bots[(i+adversary)%4].coinche(bet,betcolor), end="\n"*2)

    i+=1


if __name__=="__main__" :

  test("coinche",test_adaptBetStrength)

  test("coinche",test_coinche)
