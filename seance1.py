#Question A.2

print("Bonjour le monde!")

Question A.3
nombre_int = 42
nombre_float = 3.14
string = "ceci est une chaîne de caractères"
booleen = True
liste = [1, 2, 3, 4, 5]
dictionnaire = {"clé1": "valeur1", "clé2": "valeur2"}


print(type(nombre_int))  # Affiche <class 'int'>
print(type(nombre_float))  # Affiche <class 'float'>
print(type(string))  # Affiche <class 'str'>
print(type(booleen))  # Affiche <class 'bool'>
print(type(liste))  # Affiche <class 'list'>
print(type(dictionnaire))  # Affiche <class 'dict'>


#Question A.4 

a = 10
b = 3


print("Addition (+) :", a + b)          
print("Soustraction (-) :", a - b)      
print("Multiplication (*) :", a * b)    
print("Division (/ ) :", a / b)         
print("Division entière (//) :", a // b)
print("Modulo / Reste (%) :", a % b)    
print("Puissance (**) :", a ** b)       
print()


texte1 = "Bonjour"
texte2 = "tout le monde"


fusion = texte1 + " " + texte2
print("Concaténation :", fusion)


print("Mise en majuscules (.upper()) :", fusion.upper())
print("Découpage en liste (.split()) :", fusion.split())
print()


taux_change = [1.08, 1.09, 1.05]
print("Liste initiale :", taux_change)


taux_change.append(1.12)
print("Après ajout de 1.12 :", taux_change)


print("Longueur de la liste (len()) :", len(taux_change))


print("Premier élément [0] :", taux_change[0])
print("Dernier élément [-1] :", taux_change[-1])
print()


donnees_bce = {"base": "EUR", "devise": "USD", "taux": 1.09}
print("Dictionnaire initial :", donnees_bce)


print("Accès au taux :", donnees_bce["taux"])


donnees_bce["date"] = "2026-09-02"
print("Après ajout de la clé 'date' :", donnees_bce)
print()


x = 5
y = 10


print("Égalité (==) :", x == y)         
print("Différence (!=) :", x != y)      
print("Strictement inférieur (<) :", x < y)  
print("Strictement supérieur (>) :", x > y)  
print("Inférieur ou égal (<=) :", x <= 5)    
print("Supérieur ou égal (>=) :", y >= 12)   
print()


est_ouvert = True
est_ferie = False


print("ET logique (and) :", est_ouvert and not est_ferie) 
print("OU logique (or) :", est_ouvert or est_ferie)       
print("Inversion (not) :", not est_ouvert)

A.5
taux = 1.08


if taux > 1:
   print("au-dessus de 1")
elif taux == 1:
   print("égal à 1")
else:
   print("en-dessous de 1")

# Question A.6 

taux_liste = [1.5, 1.75, 2, 2.25]


somme_for = 0


for taux in taux_liste:
   print("Taux :", taux)
   somme_for += taux  # Équivalent à : somme_for = somme_for + taux


print("Somme totale (for) :", somme_for)
print()


somme_while = 0 
index = 0       


while index < len(taux_liste):
   taux = taux_liste[index] 
   somme_while += taux      
   index = index + 1               


print("Somme totale (while) :", somme_while)

1. Accéder aux valeurs
reponse = {
   "amount": 1.0,
   "base": "EUR",
   "date": "2024-01-02",
   "rates": {"USD": 1.0956},
}


print(reponse["date"])           # 2024-01-02
print(reponse["rates"]["USD"])   # 1.0956
Pour un dictionnaire imbriqué, on enchaîne simplement les crochets : rates est lui-même un dictionnaire, donc reponse["rates"]["USD"] va chercher la clé "USD" à l'intérieur.
2. Écraser une clé existante
reponse["date"] = "2099-01-01"
print(reponse)
# {'amount': 1.0, 'base': 'EUR', 'date': '2099-01-01', 'rates': {'USD': 1.0956}}




Rien n'est "ajouté" : quand la clé existe déjà, l'affectation remplace l'ancienne valeur par la nouvelle. Un dictionnaire ne peut pas avoir deux fois la même clé — c'est le principe même d'un dict (association clé → valeur unique).
3. Copie simple (.copy()) : le piège de la copie superficielle
opie = reponse.copy()
copie["base"] = "USD"


print(reponse["base"])  # EUR  -> l'original n'a PAS changé
print(copie["base"])    # USD



Jusque-là tout va bien : modifier une clé de premier niveau sur la copie ne touche pas l'original.
Mais maintenant, modifions la partie imbriquée rates :


copie["rates"]["USD"] = 999
print(reponse["rates"])  # {'USD': 999}  -> l'original A CHANGÉ !
print(copie["rates"])    # {'USD': 999}

Constat : .copy() fait une copie superficielle (shallow copy). Elle crée un nouveau dictionnaire "conteneur", mais les valeurs qui sont elles-mêmes des objets mutables (comme le sous-dictionnaire rates) ne sont pas dupliquées — copie["rates"] et reponse["rates"] pointent vers le même objet en mémoire. Modifier l'un modifie donc l'autre.
4. Copie profonde (deepcopy)
import copy


reponse = {
   "amount": 1.0,
   "base": "EUR",
   "date": "2024-01-02",
   "rates": {"USD": 1.0956},
}


copie_profonde = copy.deepcopy(reponse)
copie_profonde["rates"]["USD"] = 999


print(reponse["rates"])        # {'USD': 1.0956}  -> inchangé !
print(copie_profonde["rates"]) # {'USD': 999}



Avec copy.deepcopy(), Python duplique récursivement toute la structure : le sous-dictionnaire rates de la copie est un objet totalement distinct de celui de l'original. Les deux dictionnaires sont désormais complètement indépendants, à tous les niveaux d'imbrication.
