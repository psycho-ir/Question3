__author__ = 'soroosh'
import logging
from actions import HelloWorldAction, PicAction, ClientAction, TimeAction, DirAction, MyAction
from engine import WebServer

logging.basicConfig(level=logging.INFO)

s = WebServer(8181)
s.register_action(HelloWorldAction())
s.register_action(PicAction())
s.register_action(ClientAction(s.get_info))
s.register_action(TimeAction())
s.register_action(DirAction())
s.register_action(MyAction())
s.start()

