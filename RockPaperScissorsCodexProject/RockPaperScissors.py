import random
#Created a dictionary to map the choices because its easier for the logic and possobilities 
#instead of using multiple if-else statements
winnings = {
    'rock': 'scissors',
    'scissors': 'paper',
    'paper': 'rock'
}

#Function to get computer's random choice
def get_computer_choice():
    return random.choice(list(winnings.keys()))

#Function to determine the winner
def determine_winner(user_choice, computer_choice):
    if user_choice == computer_choice:
        return 'tie'
    elif winnings[user_choice] == computer_choice:
        return 'user'
    else:
        return 'computer'

#Main game loop    
while True:
    player_choice = input("Enter rock, paper, or scissors (or 'quit' to exit): ").lower()
    if player_choice == 'quit':
        break
    if player_choice not in winnings:
        print("Invalid choice. Please try again.")
        continue
    
    computer_choice = get_computer_choice()
    print(f"Computer chose: {computer_choice}")
    
    winner = determine_winner(player_choice, computer_choice)
    if winner == 'tie':
        print("It's a tie!")
    elif winner == 'user':
        print("You win!")
    else:
        print("Computer wins!") 