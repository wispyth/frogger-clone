from game import Game
from rendering import load_assets

if __name__ == "__main__":
    print("Loading assets...")
    load_assets()
    print("Assets loaded. Starting game.")
    Game().run()
