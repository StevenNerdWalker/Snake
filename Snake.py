import msvcrt as ms
import timeit as timeit
import time as time


class Timer:
    def __init__(self) -> None:
        self.start = time.perf_counter()

    def get_time(self):
        self.now = time.perf_counter()
        self.time = self.now - self.start
        return self.time

t = Timer()
while t.get_time() < 5:
    a = ms.getch()
    print('pau')

print(a)








#print('cu')
#answer = ms.getch()#.decode('ASCII')
#new_answer = ms.getch()
#print(answer, 'pau', new_answer)


# big brain time
# getch returns b'\x00' if its a special character, such as the arrow keys
# so i can call it once (for wasd), and if returns this, then call it again to get the first ones actual key (for the arrows)