from math import pi


pi = pi
str_pi = str(pi)
str_pi = str_pi.replace('.', '')
list_str_pi = list(str_pi)
print(sum(map(int, list_str_pi)))