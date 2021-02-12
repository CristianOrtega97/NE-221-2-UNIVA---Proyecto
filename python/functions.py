def say_hello():
    return "Hello"

print(say_hello())

def say_hello_user(name):
    print("Hello "+name)

name = "Emanuel"
say_hello_user(name)

def user_years_old(actual_year,born_year):
    years_old = actual_year - born_year
    return years_old

print(user_years_old(2021,1997))

#Ejercicio 2 Funciones que reciban 2 parámetros

def area_rectangulo(base,altura):
    return base * altura

def area_triangulo(base,altura):
    return (base*altura)/2

print(area_rectangulo(2,3))
print(area_triangulo(5,6))