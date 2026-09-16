#Question C.1
def factorielle(n) :
    if n == 0 :
        return 1
    else :
        return n * factorielle(n-1)

def somme_liste (liste) :
    if len(liste) == 0 :
        return 0
    else :
        return liste[0] + somme_liste(liste[1:])

# Question C.2
def fibonnaci(n):
    if n == 0 :
        return 0
    if n == 1 :
        return 1
    else :
        return fibonnaci (n-1) + fibonnaci (n-2)

import time
for n in range (10,36,5) :
    debut = time.perf_counter()
    resultat = fibonnaci (n)
    fin = time.perf_counter()
    print (f"fibonnaci({n}) = {resultat} - temps : {fin - debut:.4f} secondes")

import time
from functools import lru_cache
@lru_cache(maxsize=None)
def fibonnaci_memo(n):
    if n == 0 :
        return 0
    if n == 1 :
        return 1
    else :
        return fibonnaci_memo (n-1) + fibonnaci_memo (n-2)

def fibonnaci_iteratif(n) :
    a, b = 0,1
    for _ in range(n) :
        a, b = b, a + b
    return a

import sys
print(sys.getrecursionlimit())
try :
    fibonnaci_memo(2000)
except RecursionError as e:
    print(f"Erreur : {e}")

#Question C.3
def somme(liste) :
    total = 0
    for element in liste :
        total += element
    return total

def paires (liste) :
    resultat = []
    for i in liste:
        for j in liste:
            resultat.append((i,j))
    return resultat

def fibonnaci (n) :
    if n<=1 :
        return n
    return fibonnaci(n-1) + fibonnaci(n-2)

def factorielle_iterative (n) :
    resultat = 1
    for i in range (1, n+1):
        resultat *= i
    return resultat

from functools import lru_cache
@lru_cache(maxsize=None)
def fibonnaci_memo(n) :
    if n<=1 :
        return n
    return fibonnaci_memo(n-1) + fibonnaci_memo(n-2)


import time
import sys
import tracemalloc
from functools import lru_cache

# Version 1 : récursive naïve
def fib_naif(n):
    if n <= 1:
        return n
    return fib_naif(n - 1) + fib_naif(n - 2)

# Version 2 : récursive avec mémoïsation
@lru_cache(maxsize=None)
def fib_memo(n):
    if n <= 1:
        return n
    return fib_memo(n - 1) + fib_memo(n - 2)

# Version 3 : itérative
def fib_iteratif(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a
