"""
Rules:
    + When you call a function, push the return addr on the stack
    + When you return, pop the return address off the stack (and store it in the PC)
Stack:

699:  a =  ?? |
698:  b = ??  |  main's stack frame
697:  [addr1] |

696:  x = 2   |
695:  y = 7   | mult2's stack frame
694:  z = ??  |
693:  [addr2] |
"""

def mult2(x, y):
    z = x * y
    return z

def main():
    a = 2
    b = mult2(a, 7)
    print(b)

    return

main()

print("Done")
