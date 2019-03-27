# coding=utf-8

a = str(input("a = "))
b = str(input("b = "))
print(a, '+', b, '=')

alen = len(a)
blen = len(b)

longer = alen if alen > blen else blen
longer_str = a if alen > blen else b
shorter = alen if alen < blen else blen
i = 0
carry = 0
result = ''

print(result)
