
from fastapi import FastAPI
from socketio import ASGIApp, Server


class SocketIO ():
    sio: Server
    app_sio: ASGIApp

    def __init__(self, app: FastAPI):
        self.initialize_socket_io(app)
        self.register_events()

    def initialize_socket_io(self, app: FastAPI):
        self.sio = Server(cors_allowed_origins="*")
        self.app_sio = ASGIApp(self.sio, app)

    def register_events(self):
        @self.sio.event
        async def connect(sid, environ):
            print('Client Connected: ', sid)

        @self.sio.event
        def disconnect(sid):
            print('Client Disconnected: ', sid)
