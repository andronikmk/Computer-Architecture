def looper(n):
    if n < 0: return
    print(n)
    looper(n-1)

    return

looper(4)
