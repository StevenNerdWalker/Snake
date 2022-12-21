import msvcrt as ms
import multiprocessing as mp
import time, random


class Snake:
    def __init__(self, board_width, board_height) -> None:
        """Spawn the snake in the center of the board with an initial length of two pointing to the right and with no initial direction"""
        self.board_width = board_width
        self.board_height = board_height

        self.length = 2
        self.x = board_width//2
        self.y = board_height//2
        self.head = (self.x, self.y)

        self.body = [] # each element is a x, y pair , the first element is the head and the last is the tail
        self.body.append(self.head)
        self.tail = (self.x-1, self.y)
        self.body.append(self.tail)
        self.direction = None

    def get_direction(self):
        return self.direction

    def change_direction(self, new_direction):
        self.direction = new_direction

    def move(self):
        pass

    def check_collision(self):
        pass


class Food:
    def __init__(self) -> None:
        pass

    def spawn_food(self):
        pass

    def get_position(self):
        pass



def getch_move(q):
    # getch returns b'\x00' if its a special character, such as the arrow keys
    # so i can call it once (wasd), and if it returns that, then call it again to get the actual key (the arrows)
    a = ms.getch()
    q.put(a)
    if a == b'\x00':
        b = ms.getch()
        q.put(b)
    return


def get_move(stop):
        q = mp.Queue()
        p = mp.Process(target=getch_move, name='Getch', args=(q, ))
        p.start()
        time.sleep(stop)
        p.terminate()
        # diference between .join() and .terminate()
        # join holds the main thread and waits until the completion of the child (p)
        # terminate kills the process immediatly (exactly what i need)

        # queue works in first in first out
        if q.qsize() == 1:      # wasd only adds 1 item to the queue
            return q.get()
        elif q.qsize() == 2:    # arrow keys add 2 items
            q.get()             # get the first one out
            return q.get()      # return the arrow key
        else:
            return None

            

if __name__ == '__main__':
    # agora eu entendi o porque do name == main
    # é pra nenhum dos processos executar o codigo que é só do processo principal
    # então tudo fora desse if tambem seria executado pelo processo
    mp.set_start_method('spawn')
    print(get_move(3))



# TODO multiplayer snake? wasd and arrows?