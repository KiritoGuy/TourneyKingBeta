import os
from dotenv import load_dotenv

load_dotenv()


class Emojis:
    def __init__(self):
        self.staff = '<:Discord:858675155941064714>'
        self.yes = '<a:DD_yes:873108459044880444>'
        self.no = '<a:no:873108921273974804>'
        self.loading = '<a:EpicLoading5:873107947977310248>'


class Logs:
    def __init__(self):
        self.cmds: int = 895171174126977024
        self.cmd_errs: int = 895163964361674752
        self.event_errs: int = 895163964361674752
        self.add_remove: int = 895163962587496458


class Config:
    def __init__(self):
        self.emojis = Emojis()
        self.logs = Logs()
        self.prefixes = ['sq!', 'sq!']
        self.status = 'Squid Game'
        self.owners = [692333430045671425, 753247226880589982]
        self.client_secret = os.environ.get('CLIENT_SECRET')
        self.bot_lists = [733135548566470726, 333949691962195969]
