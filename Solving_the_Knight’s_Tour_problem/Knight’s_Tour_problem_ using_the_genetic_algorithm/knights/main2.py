# main.py
from knight_v2 import run_backtracking
from src.animation import animate

if __name__ == "__main__":
    print("The horse ride issue is being resolved (Knight's Tour)...")
    path = run_backtracking()
    print(f"The solution has been found! Number of steps: {len(path)}")
    animate(path)
    