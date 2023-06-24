from threading import Thread


class Game:

    def run_game(self):
        Thread(target=self.start_game)
        while True:
            self.loop()

    def start_game(self):
        raise NotImplementedError()

    def loop(self):
        raise NotImplementedError()
