from time import sleep
from nameko.rpc import rpc
from random import randint

class GreetingService:
    name = 'greeting_service'

    @rpc
    def hello(self, name):
        sleep( randint(1,10) )
        return f'Hello {name}'
    

    