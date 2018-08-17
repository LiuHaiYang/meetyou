from flask_script import Manager, Server,Shell
from flask_migrate import Migrate, MigrateCommand
import main
import meetyou

manager = Manager(meetyou.app)
migrate = Migrate(meetyou.app, main.db)
manager.add_command('db', MigrateCommand)
@manager.shell
def make_shell_context():
    return dict(app=meetyou.app,db = main.db)
if __name__ == '__main__':
    manager.run()
