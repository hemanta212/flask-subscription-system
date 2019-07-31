import os
import sys
from flask_subscription_system import create_app, db
from flask_subscription_system.models import User

app = create_app()
arg = sys.argv[1:]

if 'sqlite' in arg:
    print('setting sqlite db....')
    with app.app_context():
        db.create_all()
        print('done.')

if 'i' in arg:
    with app.app_context():
        while True:
            inp = input(">> ")
            if inp == 'clear':
                if sys.platform.startswith('win'):
                    os.system('cls')
                else:
                    os.system('clear')
                continue

            try:
                exec('print({0})'.format(inp))
            except Exception as e:
                print(e)


if __name__ == "__main__":
    app.run('0.0.0.0')
