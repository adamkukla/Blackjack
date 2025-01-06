import art
import random

def ace(score, cards):
    '''decides if ACE is counted as 1 or 11 and returns the score more favourable for either player or dealer'''
    if "A" in cards:
        score -= 11
        if (score + 11) > 21:
            score += 1
        else:
            score += 11
    return score

def total(cards):
    '''calculates the total of the cards'''
    current_total = 0
    for card in cards:
        current_total += deck_values[card]
    return current_total

def player_decision():
    '''returns T/F answer if the player wants to draw another card = to HIT or to end the turn = to STAND.'''
    player_choice = False
    while not player_choice:
        player_choice = input('Would you like to HIT ( + 1 card) or STAND ? ').lower()
        if player_choice == 'hit':
            return 'hit'
        elif player_choice == 'stand':
            return 'stand'
        else:
            print('Make a proper choice.')
            player_choice = False

def game_status(p_total, p_cards, d_total, d_cards):
    '''gives information about current cards and scores in the game based on the card dictionary'''
    print('Your cards: ')
    for card in p_cards:
        print(card)
    print(f'Your total: {p_total}')
    print('\nDealer cards: ')
    for card in d_cards:
        print(card)
    print(f'Dealer total: {d_total}')


def game_over(p_total, p_cards, d_total, d_cards, bank, stake):
    '''protocol executed when it is time to end the game. Also calculates the bank balance and restarts the game. returns bank balance.'''
    if p_total > 21:
        print('You lose.')

    if p_total > d_total and p_total <= 21:
        if p_total == 21:
            print('Blackjack!')
        print('You won!')
        bank += 2 * stake

    if p_total < d_total and d_total <= 21:
        if d_total == 21:
            print('Dealer Blackjack!')
        print('Dealer won!')
        print('You lose.')

    if p_total == d_total and d_total <= 21:
        if d_total == 21:
            print('Both Blackjack!')
        print('Draw!')
        bank += stake

    if d_total > 21:
        print('You won!')
        bank += 2 * stake

    print(f'Your bank balance is {bank}.')

    again_choice = True
    while again_choice:
        again = input("Would you like to play again? 'y' / 'n' ").lower()
        if again == 'y':
            again_choice = False
            return int(bank)
        if again == 'n':
            bank = 0
            again_choice = False
            return int(bank)
        else:
            print('Make a proper choice.')
            again_choice = True



def dealer_sequence(p_total, p_cards, d_total, d_cards):
    '''function executing the role of the dealer. decides whether the dealer draws another card. Returns final dealer cards.'''
    game_status(p_total, p_cards, d_total, d_cards)
    if d_total > 21 and "A" in d_cards:
        d_total = ace(d_total, d_cards)
        dealer_sequence(p_total, p_cards, d_total, d_cards)
    if d_total >= 17:
        return d_cards
    if d_total < 17:
        d_cards.insert(len(d_cards) + 1, deck_of_cards[random.randint(0, len(deck_of_cards) - 1)])
        d_total = total(d_cards)
        dealer_sequence(p_total, p_cards, d_total, d_cards)
    return d_cards

initial_bank_balance = 1000

bank_balance = initial_bank_balance

deck_of_cards = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K'] #card deck
deck_values = { #dictionary with the card values ACE's value is 11 but if it is more favourable to be 1 function ace() decides
    'A': 11,
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    '10': 10,
    'J': 10,
    'Q': 10,
    'K': 10
}

while bank_balance > 0:
    player_cards = []               #resetting the values
    dealer_cards = []
    player_total = 0
    dealer_total = 0
    revealed_dealer_cards = []
    revealed_player_total = 0
    bet = 0
    player_hit = False

    print(art.logo)


    while bet ==0:                  #loop will not let the player continue unless he/she bets, also used to ensure the proper amount
        bet = int(input(f'Your bank balance is {bank_balance}. What is your bet? '))
        if bet <= bank_balance:
            bank_balance -= bet
        else:
            print('Sorry, you do not have enough money.')
            bet = 0

    print(f'Your bet {bet} was accepted. Your current balance is {bank_balance}')

    player_cards = [deck_of_cards[random.randint(0, len(deck_of_cards) - 1)], deck_of_cards[random.randint(0, len(deck_of_cards) - 1)]] #player is dealt both cards
    dealer_cards = [deck_of_cards[random.randint(0, len(deck_of_cards) - 1)], deck_of_cards[random.randint(0, len(deck_of_cards) - 1)]] #dealer is dealt both cards
    player_total = total(player_cards)   #values are found and added for player and dealer
    dealer_total = total(dealer_cards)
    revealed_dealer_cards = [dealer_cards[0], '█']          #dealer only reveals one card in the beginning of the game
    revealed_dealer_total = deck_values[dealer_cards[0]]    #value is calculated only from the revealed card

    game_status(player_total, player_cards, revealed_dealer_total, revealed_dealer_cards)   #prints player's and dealer's cards and values

    player_hit = player_decision()          #player decides to HIT +1card (True) or to STAND (False)

    while player_hit == 'hit':
        if player_hit:                          #if player decides to hit
            player_cards.insert(len(player_cards) + 1, deck_of_cards[random.randint(0, len(deck_of_cards) - 1)]) #1 more card is drawn
            player_total = total(player_cards)                                                                      #total is calculated again
            game_status(player_total, player_cards, revealed_dealer_total, revealed_dealer_cards)                   #new game status generated to make a better next choise
            if player_total >= 21:                                   #bust case
                player_total = ace(player_total, player_cards)      #ACE value 1 insted of 11 consideration
                if player_total >= 21:                               #if still bust
                    bank_balance = game_over(player_total, player_cards, revealed_dealer_total, revealed_dealer_cards, bank_balance, bet) #starts game over sequence for Blackjack! or bust
                    player_hit = 'bust' #ends while loop
                else:
                    player_hit = player_decision()  #lets the player decide HIT/STAND again if ACE value 1 changes the total
            else:
                player_hit = player_decision()      #lets the player decide HIT/STAND again if the score is below 21

    if player_hit == 'stand':               #if player decides to stand
        dealer_cards = dealer_sequence(player_total, player_cards, dealer_total, dealer_cards)   #starts dealer sequence - dealer automated decision making
        dealer_total = total(dealer_cards)                             #dealer total score calculated after the dealer sequence is finished
        bank_balance = game_over(player_total, player_cards, dealer_total, dealer_cards, bank_balance, bet) #starts game over sequence to conclude the game