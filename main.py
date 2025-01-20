from src.Manager import Manager
from src.CLI import CLI

def main():
    parser = CLI()
    args = parser.parse_input()
    manager = Manager(args.command, args.language)

    manager.execute_command(args.command)

if __name__ == "__main__":
    main()
