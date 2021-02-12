students = ["Jafet","Asaf","Carlos","Emanuel"]

print(students)
print(students[0])

#Incorrecto
# students[3] = "Pablo"

students.append("Pablo")
students.append("Luis")
students.append("Luis")

#Toma la ultima posicion, ELIMINA EL ELEMENTO CON COINCIDENCIA
students.remove("Luis")

#ELIMINA EL INDEX
students.pop()

print(students)