import random
import math

players_hand = []
dealers_hand = []
bankroll = 500
bet = 0
shoe = []
sorted_decks = []
playing = False
round_over = True
spade = '\9824'
for x in range(0,4): #Create sorted stack of 4 decks
    for suit in ["\u2660","\u2666","\u2663","\u2665"]:
        for face_value in range(2,12):
            sorted_decks.append({"suit":suit,"number":face_value})
        for face_value in range(0,3):
            sorted_decks.append({"suit":suit,"number":10})

for card in sorted_decks:
    print(card["suit"]+str(card["number"]))

def shuffle_up():
    print("SHUFFLE UP!")
#    temp_deck = sorted_decks.copy()
#    for x in range(0, len(sorted_decks)):
#        selected_card = random.choice(temp_deck)
#        shoe.append(selected_card)
#        temp_deck.remove(selected_card)
    global shoe 
    shoe = sorted_decks.copy()
    random.shuffle(shoe)

def display_cards(hand):
    output = ""
    for card in hand:
        temp = "{}{} "
        output += temp.format(str(card["suit"]), str(card["number"]))
    print(output)
    print("Total: "+str(calc_hand(hand)))

def deal_out():
    #simulate real deal out, I know it's unnecessary
    global shoe, round_over
    round_over = False
    players_hand.append(shoe.pop())
    dealers_hand.append(shoe.pop())
    players_hand.append(shoe.pop())
    #print(calc_hand(players_hand))
    print("You have:")
    display_cards(players_hand)
    print("================================================================") #ugly divider :(
    print("Dealer has:")
    display_cards(dealers_hand)

    if calc_hand(players_hand) == 21:
        lucky_lucky() 
        if calc_hand(dealers_hand, True) == 10 or calc_hand(dealers_hand, True) == 11:
            draw(dealers_hand)
            print("Dealer has:")
            display_cards(dealers_hand)
            game_over()
        else: 
            game_over()

#Lucky Lucky Play
def lucky_lucky(): 
    global players_hand, dealers_hand, bankroll, lucky_bet

    calc_both_hands = calc_hand(players_hand) + calc_hand(dealers_hand, True)
    
    #Aces 
    if calc_both_hands > 21: 
        if players_hand[0]["number"] == 11 or players_hand[1]["number"] == 11 or dealers_hand[0]["number"] == 11: 
            calc_both_hands = calc_both_hands - 10
    
    #Suited Lucky
    suited_lucky = False 
    try: 
        if players_hand[0]["suit"] == players_hand[1]["suit"] and players_hand[1]["suit"] == dealers_hand[0]["suit"]:
            suited_lucky = True 
    except IndexError: 
        print(players_hand)
        print(dealers_hand)
    
    #Lucky 678 
    lucky_678 = False 
    if calc_both_hands == 21: 
        for card in players_hand: 
            if card["number"] == 6: 
                for card in players_hand: 
                    if card["number"] == 7:
                        lucky_678 = True 
        for card in players_hand: 
            if card["number"] == 7: 
                for card in players_hand: 
                    if card["number"] == 8:
                        lucky_678 = True
        for card in players_hand: 
            if card["number"] == 8: 
                for card in players_hand: 
                    if card["number"] == 6:
                        lucky_678 = True
                        
    #Lucky 777
    lucky_777 = False
    if players_hand[0]["number"] == 7 and players_hand[1]["number"] == 7 and dealers_hand[0]["number"] == 7: 
        lucky_777 = True

    if lucky_bet > 0: 
        if calc_both_hands == 19 or calc_both_hands == 20:
            bankroll += int(lucky_bet*2)+lucky_bet
            print("Lucky Lucky " + str(calc_both_hands) + " pays 2 to 1.")
        elif lucky_678 and suited_lucky: 
            bankroll += int(lucky_bet*100)+lucky_bet
            print("Lucky Lucky Suited 678 pays 100 to 1.")
        elif lucky_678: 
            bankroll += int(lucky_bet*30)+lucky_bet
            print("Lucky Lucky 678 pays 30 to 1.")
        elif lucky_777 and suited_lucky: 
            bankroll += int(lucky_bet*200)+lucky_bet
            print("Lucky Lucky Suited 777 pays 200 to 1.")
        elif lucky_777: 
            bankroll += int(lucky_bet*50)+lucky_bet
            print("Lucky Lucky 777 pays 50 to 1.")
        elif calc_both_hands == 21 and suited_lucky: 
            bankroll += int(lucky_bet*15)+lucky_bet
            print("Lucky Lucky Suited 21 pays 15 to 1.")
        elif calc_both_hands == 21: 
            bankroll += int(lucky_bet*3)+lucky_bet
            print("Lucky Lucky 21 pays 3 to 1.")
        else:
            print("No Lucky Lucky.")

    else: 
      return

def calc_hand(hand, is_dealer = False):
    total = 0
    index_of_aces = []
    for card in hand:
        card_value = card.get("number")
        total+=card_value
        if card_value == 11:
            index_of_aces.append(hand.index(card))
  
    if is_dealer and total > 11 and total < 18 and len(index_of_aces) > 0: #Dealer hits on soft 17 and less, so calculate as lesser value
        hand[index_of_aces.pop()]["number"] = 1
        total = total - 10
    elif total > 21 and len(index_of_aces) > 0: #Player can hit on any soft value
        hand[index_of_aces.pop()]["number"] = 1
        total = total - 10

    return total

def game_over():
    global playing, round_over, players_hand, dealers_hand, bankroll, bet,lucky_bet
    player_total = calc_hand(players_hand)
    dealer_total = calc_hand(dealers_hand)
    round_over = True

    if player_total == 21 and len(players_hand) == 2 and dealer_total == 21 and len(dealers_hand) == 2:
        print("You and the dealer have blackjack! Your bet pushes.")
        bankroll += bet
    elif player_total == 21 and len(players_hand) == 2:
        print("You have blackjack, you win!")
        bankroll += int(bet*1.5)+bet
    elif dealer_total == 21 and len(dealers_hand) == 2:
        print("The dealer has blackjack, you lose!")
    elif player_total == dealer_total:
        print("You and the dealer have "+str(player_total)+". A tie! Your bet pushes.")
        bankroll += bet 
    elif player_total > 21:
        print("You busted. You lose!")
    elif dealer_total > 21:
        print("The dealer busted. You win!")
        bankroll += 2*bet
    elif player_total > dealer_total:
        print("You have "+str(player_total)+" while the dealer has "+str(dealer_total)+". You win!")
        bankroll += 2*bet
    elif dealer_total > player_total:
        print("You have "+str(player_total)+" while the dealer has "+str(dealer_total)+". You lose!")
    
    players_hand = []
    dealers_hand = []
    print("================================================================")
    if bankroll == 0: 
        answer = input("You've run out of money! Type 'y' if you'd like to buy in for another $500. ")
        if answer.lower() == 'y': 
            bankroll += 500 
        else:
            playing = False
            return
    response = input("Would you like to play again? Press any button to continue or 'n' to leave.")
    if response.lower() == 'n':
        playing = False
    else:
        bet = make_bet()
        lucky_bet = make_lucky_bet()

def make_bet():
    global bankroll, playing
    bet = 0
    print("You have $"+str(bankroll)+".")

    while bet == 0:
        response = input("Please place a bet or press 'n' to leave.\n")

        if response.lower() == 'n':
            playing = False
            return
        else:
            bet = parse_bet(response)
    if bet > bankroll: 
        print("You don't have enough. ")
        response = input("Please place a bet or press 'n' to leave.\n")

        if response.lower() == 'n':
            playing = False
            return
        else:
            bet = parse_bet(response)
    bankroll = bankroll-bet
    return bet

def make_lucky_bet():
    #Lucky Lucky Bet
    global bankroll
    lucky_bet = 0 
    print("You have $"+str(bankroll)+".")
    while lucky_bet == 0: 
        lucky_response = input("Please place a bet for Lucky Lucky or press 'n' to continue. \n")
        if lucky_response.lower() == 'n': 
            break
        else: 
            lucky_bet = int(lucky_response)
    bankroll = bankroll-lucky_bet
    return lucky_bet

    
def parse_bet(user_input):
    global playing
    try:
        value = int(user_input)
        playing = True
        return value
    except ValueError:
        return 0

def draw(hand):
    global shoe
    card = shoe.pop()
    hand.append(card)

#Main        
print("Welcome to Blackjack!")
bet = make_bet()
lucky_bet = make_lucky_bet()
while playing:
    if len(shoe) < 20:
        shuffle_up()
        
    deal_out()
    lucky_lucky()
    while not round_over:
        print("================================================================")
        
        if calc_hand(players_hand) == 21:
            draw(dealers_hand)
            while calc_hand(dealers_hand, True) < 17:
                draw(dealers_hand)
            print("Dealer has:")
            display_cards(dealers_hand)
            game_over()
            break

        response = input("Press any key to HIT, press 'n' to STAY.\n")
        if response.lower() == 'n':
            draw(dealers_hand)
            while calc_hand(dealers_hand, True) < 17:
                draw(dealers_hand)
            print("Dealer has:")
            display_cards(dealers_hand)
            game_over()
        else:
            draw(players_hand)
            print("You have:")
            display_cards(players_hand)
            if calc_hand(players_hand) > 21:
                game_over()

print("Goodbye.") 
