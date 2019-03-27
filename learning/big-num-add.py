# coding=utf-8


def add(a, b):
    alen = len(a)
    blen = len(b)

    longer = alen if alen > blen else blen
    longer_str = a if alen > blen else b
    shorter = alen if alen < blen else blen
    i = 0
    carry = 0
    result = ''

    while i < longer:
        if i < shorter:
            summ = int(a[alen - 1 - i]) + int(b[blen - 1 - i]) + carry
            carry = 1 if summ >= 10 else 0
            result = str(summ % 10) + result
        else:
            summ = int(longer_str[longer - 1 - i]) + carry
            carry = 1 if summ >= 10 else 0
            result = str(summ % 10) + result
        i += 1
    if carry == 1:
        result = '1' + result

    return result


if __name__ == "__main__":
    import sys
    if len(sys.argv) == 1:
        a = str(input("a = "))
        b = str(input("b = "))
        print(a, '+', b, '=')
        r = add(a, b)
        print(r)
    elif len(sys.argv) == 3:
        print(add(str(sys.argv[1]), str(sys.argv[2])))
    else:
        print('Please input 2 numbers.')
