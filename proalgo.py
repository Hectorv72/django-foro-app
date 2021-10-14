#for i in range(4):

#    nom = input('ingresar: ')#

#    permitidas = ['txt', 'doc', 'docx']
#    extension = nom.split('.')[-1]
#    
#    if extension in permitidas:
#        print('correcto')

"""
texto = ' aaa a          '

print ( texto.strip() )"""


"""
characters = ['p','y','t','h','o','n']
word = "".join(characters)
print(word)"""



""" mensaje con muchos espacios sin perder espacios

word = "Este       mensaje es para @Hector que se mamo"
word = "Este       mensaje es para @Hector que se mamo"

separado = word.split(' ')

print(separado)

print( " ".join(separado) )"""

usuarios = ['Hector','Gomez','Lopez','Perez','Diaz']

word = "Este       mensaje es para @Hector que es un kpo @Hector anasdsd @Hector @Hector"

"""for i in usuarios:
    if word.find('@'+i):
        print(i)
        print('lel')"""



separado = word.split()
print(separado)

for i in usuarios:
    #print(i)
    if '@' + i in separado:
        print('hay')



