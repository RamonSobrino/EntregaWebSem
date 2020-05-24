

from Util import leer_resultados

import Constant

import requests
'''
    Entidades de medicamentos:
    Q11173 : chemical compound
    Q35456 : essential medicine
    Q12140 : medication
'''

id_medicamentos = ['Q11173', 'Q35456', 'Q12140']


def ejercicio3(max_terminos):

    resultado =[]

    lista_palabras = leer_resultados(Constant.PATH_RESULT_ROOT)

    lista_palabras.keys()

    palabras = []
    contador =0
    for palabra in lista_palabras:
        contador = contador +1
        if(contador>max_terminos):
            break
        palabras.append(palabra)

    print("Numero de palabras: ", len(palabras))

    contador = 1
    for palabra in palabras:

        contador = contador +1

        r = requests.get( 'https://www.wikidata.org/w/api.php',
                     params={'search': palabra, 'action':'wbsearchentities', 'language':'en', 'format': 'json'})

        contenido = r.json()

        print("Analizada palabra ", contador)

        for search_result in contenido['search']:
            id_entidad_WD = search_result['id']

            r2= requests.get( 'https://www.wikidata.org/w/api.php',
                            params={'ids': id_entidad_WD, 'action': 'wbgetentities', 'languages': 'en',
                                    'format': 'json'} )

            contenido2 = r2.json()

            #print(contenido2)

            for entity in contenido2['entities'].keys():
                entidad = contenido2['entities'][entity]
                for claim in entidad['claims'].keys():
                    actual = contenido2['entities'][entity]['claims'][claim]
                    for act in actual:
                        if act['mainsnak']['property'] == 'P31':
                            id_instance_of = act['mainsnak']['datavalue']['value']['id']
                            if id_instance_of in id_medicamentos:
                                print("Palabra que casa ", palabra)
                                if palabra not in resultado:
                                    resultado.append(palabra)

    return resultado

print("Inicio Ejercicio 3")
resultado = ejercicio3(3000)

print("Diccionario ordenado ")

with open(Constant.PATH_RESULT_EJ3, 'w') as rh:
    for word in resultado:
        rh.write( "{0}\n".format(word))
