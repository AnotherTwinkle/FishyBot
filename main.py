from bot import FishyBot
from dotenv import load_dotenv

def main():
    load_dotenv()
    client = FishyBot("!")
    client.set_up()
    client.run_bot()


if __name__ == "__main__":
    main()
