import msvcrt as ms
import multiprocessing as mp
import time, random


class Snake:
    def __init__(self, board_width, board_height) -> None:
        """Spawn the snake in the center of the board with an initial length of two pointing to the right and with no initial direction"""
        if board_width < 3 or board_height < 3:
            raise Exception        
        
        self.board_width = board_width
        self.board_height = board_height # the point 0, 0 is the top left corner

        self.length = 2
        self.x = (board_width-1)//2     # -1 to account for beginning at 0
        self.y = (board_width-1)//2
        self.head = (self.x, self.y)

        self.body = []      # each element is a x, y pair , the first element is the head and the last is the tail
        self.body.append(self.head)
        self.body.append((self.x-1, self.y))    # tail
        self.direction = None


    def get_head_position(self):
        return self.head


    def get_direction(self):
        return self.direction


    def change_direction(self, move):
        # hkpm are the arrows representations in bytes
        # checks if the move wont go backwards (eg press w when going down)
        new_direction = self.direction # initialize the variable just in case the move isnt valid and doesnt enter any of the ifs

        if move == 'w' or move == 'H':
            if self.direction != 'down':
                new_direction = 'up'
        elif move == 'a' or move == 'K':
            if self.direction != 'right':
                new_direction = 'left'
        elif move == 's' or move == 'P':
            if self.direction != 'up':
                new_direction = 'down'
        elif move == 'd' or move == 'M':
            if self.direction != 'left':
                new_direction = 'right'

        self.direction = new_direction


    def get_body(self):
        return self.body


    def get_board_dimensions(self):
        return (self.board_width, self.board_height)


    def move(self):
        direction = self.direction
        length = self.length

        if direction == 'up':
            self.y -= 1     # move it up
        elif direction == 'down':
            self.y += 1     # move it down
        elif direction == 'left':
            self.x -= 1     # move it left
        elif direction == 'right':
            self.x += 1     # move it right

        if direction is not None:   # check this in case the snake hasnt begun moving yet
            self.head = (self.x, self.y)    # update the head
            self.body.insert(0, self.head)  # insert the new head at the beginning of the list
            if len(self.body) > length:     # if the snake has grown, dont delete, else, do
                del self.body[-1]       # delete the last part of the tail


    def check_collision(self):
        body = self.body
        head = body[0]
        x = head[0]
        y = head[1]
        body_minus_head = set(body[1:])

        if head in body_minus_head:     # the head is intersecting some part of the body (aka sharing the same coordinates)
            return True

        if x < 0 or x > self.board_width-1:   # the head hit the left or right wall
            return True

        if y < 0 or y > self.board_height-1:    # the head hit the top or bottom wall
            return True

        return False


    def check_food(self, food):
        if food.get_position() == self.get_head_position():
            return True
        return False


    def grow(self):
        self.length += 1


class Food:
    def __init__(self, snake: Snake) -> None:
        snake_body = snake.get_body()
        self.width, self.height = snake.get_board_dimensions()

        # every coordinate that isnt part of the snakes body
        empty_space = [(x, y) for x in range(self.width) for y in range(self.height) if (x, y) not in set(snake_body)]
        
        self.position = random.choice(empty_space)


    def move_food(self, snake: Snake):
        snake_body = snake.get_body()
        empty_space = [(x, y) for x in range(self.width) for y in range(self.height) if (x, y) not in set(snake_body)]
        self.position = random.choice(empty_space)


    def get_position(self):
        return self.position


def print_board(snake: Snake, food: Food):
    snake_body = snake.get_body()
    snake_set = set(snake_body)     # will only need to test membership in the snake, so turn it into a set
    width, height = snake.get_board_dimensions()

    print('\n'*27)  # clear the screen so it looks like the same board updating

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
            return q.get().decode(encoding='ASCII')
        elif q.qsize() == 2:    # arrow key adds 2 items
            q.get()             # get the first one out
            return q.get().decode(encoding='ASCII')      # return the arrow key
        else:
            return None


def main(board_width, board_height, initial_delay, delay_reduction_factor):
    snake = Snake(board_width, board_height)
    food = Food(snake)
    delay = initial_delay
    score = 0

    while True:
        print_board(snake, food)

        move = get_move(delay)
        if move is not None:
            snake.change_direction(move)
        snake.move()

        if snake.check_food(food):
            snake.grow()
            food.move_food(snake)
            delay = delay/delay_reduction_factor
            score += 1

        if snake.check_collision():
            break

    print_board(snake, food)
    print('\nGAME OVER')
    print(f'SCORE: {score}')
            

if __name__ == '__main__':
    mp.set_start_method('spawn')
    # agora eu entendi o porque do name == main
    # é pra nenhum dos processos executar o codigo que é só do processo principal
    # então tudo fora desse if tambem seria executado pelo processo
    main(10, 10, 1, 1)
    



# TODO multiplayer snake? wasd and arrows?