import io as io
import json
import re
import string
import math
from Util import extraer_datos_covit

##########################################################
## Metodo que lee el archivo de norvig y devuelve       ##
## un diccionario con lo que lee del archivo            ##
##########################################################
def extraer_datos_count(path):
    #path = ".\dir\count_1w.txt"

    frequency = {}

    with open( path, 'rb' ) as fh:
        lines = fh.readlines()

        for line in lines:
            apartados = line.split()
            frequency[str(apartados[0])[2:-1]] = int(apartados[1])

    return frequency


##########################################################
## Metodo que es la implementacion propia en python  de ##
## la implementacion en php que se dio en el enunciado  ##
##########################################################

def rootLogLikelihoodRatio(frenqA, frenqB, totalA, totalB):
    # $E1=$c*($a+$b)/($c+$d);
    E1 = totalA * (frenqA + frenqB) / (totalA + totalB)

    # $E2=$d*($a+$b)/($c+$d);
    E2 = totalB * (frenqA + frenqB) / (totalA + totalB)

    # $result=2*($a*log($a/$E1+($a==0?1:0))+$b*log($b/$E2+($b==0?1:0)));
    result = 2 * (frenqA * math.log( frenqA / E1 + (1 if frenqA == 0 else 0) ) + frenqB * math.log(
        frenqB / E2 + (1 if frenqB == 0 else 0) ))

    # $result=sqrt($result);
    result = math.sqrt( result )

    # if (($a/$c)<($b/$d)) $result=-$result;
    if ((frenqA / totalA) < (frenqB / totalB)):
        result = result * -1

    return result


base_path = "D://document_parses/pdf_json/"
ficheros_path = "./dir/ficheros.txt"
path_result = "./dir/resultado.txt"

extraer_datos_covit(base_path, ficheros_path, path_result)


dict_covit = extraer_datos_count(path_result)
print( "Fichero covit leido " )


path_norvig = "./dir/count_1w.txt"

dict_norvig = extraer_datos_count(path_norvig)
print( "Fichero norvig leido ")


dict_covit_list = dict_covit.keys()

total_covit = 0

for words in dict_covit_list:
    total_covit += int(dict_covit[words])
print( "Total covit calculado ")


dict_norvig_list = dict_norvig.keys()

total_norvig = 0

for words in dict_norvig_list:
    total_norvig += int(dict_norvig[words])

print("Total norvig calculado " )


print("Fichero analizado ")

path_result_Root = "./dir/resultadoRoot.txt"


finalFrequency = {}


for words in dict_covit_list:
    if words in dict_norvig_list:
        finalFrequency[words] = rootLogLikelihoodRatio(dict_covit[words], dict_norvig[words], total_covit, total_norvig)

print("Diccionario formado ")

finalFrequencySorted = [(k, finalFrequency[k]) for k in sorted(finalFrequency, key=finalFrequency.get, reverse=True)]

print("Diccionario ordenado ")

with open(path_result_Root, 'w') as rh:

    for words in finalFrequencySorted:
        rh.write( "{0} {1}\n".format(words[0], words[1]))


