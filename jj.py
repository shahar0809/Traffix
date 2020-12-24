def main():
    """
    list_1 = [["hi", "bye", "hello"], ["k", "t", "h"], ["n", "me", "my"]]
    l = 0
    m = 0
    for x in list_1:
        for k in list_1:
            print(list_1[l][m], list_1[l][m + 1], list_1[l][m + 2])
            l += 1
        if l == 3:
            break
    """
    m = 1
    n = 0
    hours = [i for i in range(1, 25)]
    for i in range(1, 8):
        while n < 24:
            print(m, hours[n])
            n += 1
        m += 1
        n = 0



if __name__ == '__main__':
    main()
