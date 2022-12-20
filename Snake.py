import msvcrt as ms

print('cu')
answer = ms.getch()#.decode('ASCII')
new_answer = ms.getch()
print(answer, 'pau', new_answer)


# big brain time
# getch returns b'\x00' if its a special character, such as the arrow keys
# so i can call it once (for wasd), and if returns this, then call it again to get the first ones actual key (for the arrows)