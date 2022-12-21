import msvcrt as ms
import time as time
import multiprocessing as mp

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