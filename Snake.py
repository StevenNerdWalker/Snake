import msvcrt as ms
import timeit as timeit
import time as time
import multiprocessing as mp

def getch_move(q):
    print('getch_move is run by ', mp.current_process().name)
    a = ms.getch()
    q.put(a)
    return


def get_move(stop):
        q = mp.Queue()
        q.put(None)
        p = mp.Process(target=getch_move, name='Getch', args=(q, ))
        p.start()

        start = time.perf_counter()
        while time.perf_counter() - start < stop:
            pass
        #print(q.get())
        if q.qsize() != 0:
            print(q.get())
        p.terminate()
        p.join()

        print('get_move is run by ', mp.current_process().name)
            

if __name__ == '__main__':
    # caralho agora eu entendi o porque do name == main
    # é pra nenhum dos processos executar o codigo que é só do processo principal
    # então tudo fora desse if tambem seria executado pelo processo
    # por isso tava printando mais de uma vez
    # passei o dia todo tentando resolver isso e agora eu entendi
    mp.set_start_method('spawn')
    get_move(3)
    #print('bazinga')
    #get_move(3)
    print('main is run by ', mp.current_process().name)




























#
#class Timer:
#    def __init__(self) -> None:
#        self.start = time.perf_counter()
#
#    def get_time(self):
#        self.now = time.perf_counter()
#        self.time = self.now - self.start
#        return self.time
#
#t = Timer()
#while t.get_time() < 5:
#    a = ms.getch()
#    print('pau')
#
#print(a)
#
##print('cu')
##answer = ms.getch()#.decode('ASCII')
#new_answer = ms.getch()
#print(answer, 'pau', new_answer)


# big brain time
# getch returns b'\x00' if its a special character, such as the arrow keys
# so i can call it once (for wasd), and if returns this, then call it again to get the first ones actual key (for the arrows)