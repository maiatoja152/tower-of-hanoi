"""Command-line Tower of Hanoi game"""
import argparse
import random
from typing import List
from typing import Dict
import sys
from collections import OrderedDict


Towers = Dict[str, List[int]]


def get_arguments() -> argparse.Namespace:
    """Get the command-line arguments"""
    parser = argparse.ArgumentParser(
        description="Command-line Tower of Hanoi game"
    )
    parser.add_argument(
        "-n",
        "--number-of-disks",
        type=int,
        choices=range(3, 20),
        default=5,
        help="The number of disks in the tower",
    )
    return parser.parse_args()


def initialize_towers(number_of_disks: int) -> Towers:
    """Initialize the three towers with a full tower on one random peg"""
    towers: Towers = OrderedDict([("A", []), ("B", []), ("C", [])])
    towers[random.choice("ABC")].extend(range(number_of_disks, 0, -1))
    return towers


def display_towers(towers: Towers, number_of_disks: int) -> None:
    """Print a display of the towers to the console"""
    tower_width: int = number_of_disks * 2 + 2
    letter_spaces = " " * (tower_width - 1)
    lines: List[str] = [
        f"{" " * (tower_width // 2)}A{letter_spaces}B{letter_spaces}C"
    ]
    empty_disk: str = f"{" " * number_of_disks}||{" " * number_of_disks}"
    for i in range(number_of_disks + 1):
        line: str = ""
        for disks in towers.values():
            if i > len(disks) - 1:
                line += empty_disk
            else:
                spaces: str = " " * (number_of_disks - disks[i])
                disk_edge: str = "@" * disks[i]
                disk_number: str = str(disks[i]).rjust(2, "_")
                line += f"{spaces}{disk_edge}{disk_number}{disk_edge}{spaces}"
            
        lines.append(line)

    for line in reversed(lines):
        print(line)


def make_player_move(towers: Towers) -> None:
    while True:
        player_move = input(
            """
Enter the letters of "from" and "to" towers, or QUIT.
(For example, AB moves a disk from tower A to tower B)
"""
        )
        if player_move.lower() == "quit":
            print("Quitting...")
            sys.exit()

        valid_moves = ("AB", "BA", "AC", "CA", "BC", "CB")
        if player_move not in valid_moves:
            print(f"Your input must be one of: {", ".join(valid_moves)}, or QUIT")
            continue

        from_tower = towers[player_move[0]]
        to_tower = towers[player_move[1]]
        if not from_tower:
            print(f"You cannot move a ring from an empty tower!")
            continue
        if to_tower and to_tower[-1] < from_tower[-1]:
            print(f"You cannot place a disk on top of a smaller disk!")
            continue
            
        break

    to_tower.append(from_tower.pop())


def check_win(towers: Towers) -> bool:
    number_of_empty_towers: int = 0
    for tower in towers.values():
        if not tower:
            number_of_empty_towers += 1
        if number_of_empty_towers == 2:
            return True
    return False
                

def main() -> None:
    args: argparse.Namespace = get_arguments()

    towers: Towers = initialize_towers(args.number_of_disks)
    print(
        """Move the tower of disks, one disk at a time, to another tower. 
A disk cannot be moved on top of a smaller disk.
"""
    )
    while True:
        display_towers(towers, args.number_of_disks)
        make_player_move(towers)

        if check_win(towers):
            display_towers(towers, args.number_of_disks)
            print("You solved the puzzle!")
            break


if __name__ == "__main__":
    main()