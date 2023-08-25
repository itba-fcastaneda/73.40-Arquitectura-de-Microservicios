from nameko.standalone.rpc import ClusterRpcProxy
from os import environ

CONFIG = {
    'AMQP_URI': f'amqp://{environ["RABBIT_USER"]}:{environ["RABBIT_PASSWORD"]}@{environ["RABBIT_HOST"]}:{environ["RABBIT_PORT"]}/'
}

class Consumer:
    name = 'consumer_service'

    def __init__(self, rpc):
        self.response=[]
        self.rpc = rpc
    
    def say_hello(self, name):
        self.response.append( self.rpc.greeting_service.hello.call_async( name=name ) )

    def get_response(self):
        return [ resp.result() for resp in self.response ]

def main():

    with ClusterRpcProxy(CONFIG) as cluster_rpc:
        c = Consumer(cluster_rpc)
        for i in range(5):
            c.say_hello( name=f'user_{i}' ) 

        for r in c.get_response():
            print(r)

if __name__=='__main__':
    main()