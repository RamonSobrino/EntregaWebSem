import json
import re

from os import listdir
from os.path import isfile, isdir


##########################################################
## Metodo que lee el archivo de reddit y devuelve       ##
## un diccionario con las palabras usadas y el numero   ##
## de veces que se usan                                 ##
##########################################################
def extraer_datos_fichero(base_path, nombreFichero, frequency):
    path = base_path+nombreFichero

    with open( path, 'rb' ) as json_file:

        counter = 0

        formatted = json.load( json_file )

        text_string = formatted['metadata']['title'].lower()

        counter = contar_palabras(counter, frequency, text_string)

        for par in formatted['abstract']:
            text_abstract = par['text']
            counter = contar_palabras(counter, frequency, text_abstract)

        for par in formatted['body_text']:
            text_abstract = par['text']
            counter = contar_palabras(counter, frequency, text_abstract)

        print( "Contador palabras: ", counter )

    return frequency


def contar_palabras(counter, frequency, text_string):
    match_pattern = re.findall( r'\b[a-z\']{3,15}\b', text_string )
    for word in match_pattern:
        counter = counter + 1
        count = frequency.get( word, 0 )
        frequency[word] = count + 1
    return counter


def escribir_resultados(path_result, frequency):
    with open( path_result, 'a' ) as rh:
        frequency_list = frequency.keys()

        for words in frequency_list:
            rh.write( str( words ) + " " + str( frequency[words] ) + "\n" )


def ls1(path):
    return [obj for obj in listdir(path) if isfile(path + obj)]


def extraer_ficheros_carpeta_sin(base_path, frequency, numero_maximo, ficheros_path):
    files = ls1(base_path)

    contador_ficheros = 0

    ficheros = []

    for file in files:
        contador_ficheros = contador_ficheros + 1
        ficheros.append(str(file))
        extraer_datos_fichero(base_path, file, frequency)
        print("Analizando fichero numero: ", contador_ficheros)
        if (contador_ficheros > numero_maximo):
            break

    with open( ficheros_path, 'w') as rh:
        for fichero in ficheros:
            rh.write(fichero + "\n")

def extraer_ficheros_carpeta_con(base_path, frequency, numero_maximo, ficheros_path):

    contador_ficheros = 0

    ficheros = []

    with open( ficheros_path, 'rb' ) as fh:
        lines = fh.readlines()
        for line in lines:
            ficheros.append(str(line)[2:-1].replace('\\r', '')
                            .replace('\\n', '').replace('\\', '').replace('\'', ''))

    for file in ficheros:
        if (contador_ficheros > numero_maximo):
            break
        contador_ficheros = contador_ficheros + 1
        extraer_datos_fichero(base_path, file, frequency)
        print("Analizando fichero numero: ", contador_ficheros)



def extraer_datos_covit(base_path, ficheros_path, path_result):
    frequency = {}

    extraer_ficheros_carpeta_con( base_path, frequency, 20000, ficheros_path)

    print( "Fichero analizado " )
    escribir_resultados( path_result, frequency )



