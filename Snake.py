import msvcrt as ms
import multiprocessing as mp
import time, random


class Snake:
    def __init__(self, board_width, board_height) -> None:
        """Spawn the snake in the center of the board with an initial length of two pointing to the right and with no initial direction"""
        self.board_width = board_width
        self.board_height = board_height # the point 0, 0 is the top left corner

        self.length = 2
        self.x = (board_width-1)//2     # -1 to account for beginning at 0
        self.y = (board_width-1)//2
        self.head = (self.x, self.y)

        self.body = []      # each element is a x, y pair , the first element is the head and the last is the tail
        self.tail = (self.x-1, self.y)
        self.body.append(self.head)
        self.body.append(self.tail)
        self.direction = None

    def get_direction(self):
        return self.direction

    def change_direction(self, new_direction):
        self.direction = new_direction

    def get_body(self):
        return self.body

    def get_board_dimensions(self):
        return (self.board_width, self.board_height)

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


def print_board(snake: Snake, food: Food):
    snake_body = snake.get_body()
    snake_set = set(snake_body)     # will only need to test membership in the snake, so turn it into a set
    width, height = snake.get_board_dimensions()

    print('\n'*30)  # clear the screen so it looks like the same board updating

    print('#='+'-='*width+'#')

    for line in range(height):
        print('|', end=' ')

        for column in range(width):
            if (column, line) in snake_set:
                if (column, line) == snake_body[0]:
                    print('@', end=' ')  # snake's head
                else:
                    print('#', end=' ')  # snake's body

            elif (column, line) == food.get_position():
                print('*', end=' ')      # food

            else:
                print(' ', end=' ')      # no snake

        print('|')

    print('#='+'-='*width+'#')


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
        elif q.qsize() == 2:    # arrow key adds 2 items
            q.get()             # get the first one out
            return q.get()      # return the arrow key
        else:
            return None


def main(board_width, board_height):
    snake = Snake(board_width, board_height)
    food = Food()
    delay = 2

    while True:
        move = get_move(delay)
        if move is not None:
            snake.change_direction(move)
            

if __name__ == '__main__':
    mp.set_start_method('spawn')
    # agora eu entendi o porque do name == main
    # é pra nenhum dos processos executar o codigo que é só do processo principal
    # então tudo fora desse if tambem seria executado pelo processo
    main(9, 9)
    



# maybe dont need self.length in snake
# TODO multiplayer snake? wasd and arrows?