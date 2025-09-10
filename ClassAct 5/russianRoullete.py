import random
gun = 6
chambers = [0] * gun
chambers[random.randint(0, gun - 1)] = 1

def checkIfPlayerGotHit(player1, player2) -> int:
    turn = 0
    while True:
        current_player = player1 if turn % 2 == 0 else player2
        input(f"{current_player}'s turn. Press Enter to pull the trigger...")
        if chambers[turn % gun] == 1:
            print(f"Bang! {current_player} is out!")
            return current_player 
        print("Click! You're safe.")
        turn += 1

def game() -> None:
    player1 = input("Enter Player 1 name: ")
    player2 = input("Enter Player 2 name: ")
    while True:
        loser = checkIfPlayerGotHit(player1, player2)
        print(f"Game over! {loser} lost.")
        break

if __name__ == "__main__":
    random.shuffle(chambers)
    print("Welcome to Russian Roulette!")
    while True:
        game()
        play_again = input("Play again? (y/n): ").lower()
        if play_again != 'y':
            break
        print("Thanks for playing!")