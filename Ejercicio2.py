import networkx as nx
from scipy.stats import spearmanr
import Constant
from Util import *


# START FUNCTION DEFINITION
def generate_relations(graph, window, paragraphs):
    for words in paragraphs:
        counter = 0
        while counter < len(words):

            current_word = counter

            window_limit = current_word
            if window_limit + window > len(words):
                window_limit = len(words)
            else:
                window_limit = window_limit + window

            for x in range(current_word, window_limit):
                for y in range(x, window_limit):
                    if x != y:
                        graph.add_edge(words[x], words[y])
                        print('Creando relacion', words[x], '->', words[y])
            counter = counter + 1

    return graph


def calculate(clean_covid_words, clean_covid_paragraphs_words, window, file):
    G = nx.Graph()
    for word in clean_covid_words:
        G.add_node(word)

    graph = generate_relations(G, window, clean_covid_paragraphs_words)
    rank = nx.pagerank(graph, 0.85)

    ordered_words = [(k, rank[k]) for k in sorted(rank, key=rank.get, reverse=True)]

    with open(file, 'w') as rh:
        for words in ordered_words:
            rh.write("{0} {1}\n".format(words[0], words[1]))

    return ordered_words


def comparate_spearman_rank(word_list1, word_list2, number_of_elements):
    cor, pvalue = spearmanr(word_list1[:number_of_elements], word_list2[:number_of_elements], axis=None)
    with open(Constant.CORRELATIONS_FILE, 'a') as rh:
        rh.write('Correlation:' + str(cor) + "\n")
        rh.write('pvalue:' + str(pvalue) + "\n")


def comparate_words(words1, words2):
    word_list1 = []
    word_list2 = []
    for word in words2:
        word_list2.append(word[0])
    for word in words1:
        word_list1.append(word[0])

    max_value = len(word_list1)
    if len(word_list1) > len(word_list2):
        max_value = len(word_list2)
    comparator = 10
    while comparator < max_value:
        comparate_spearman_rank(word_list1, word_list2, comparator)
        comparator = comparator * 10

    comparate_spearman_rank(word_list1, word_list2, max_value)


# END FUNCTION DEFINITION

# START MAIN
def main():
    ejercicio1_words = file_to_dictionary(Constant.PATH_RESULT_ROOT)

    empty_words = read_stop_words(Constant.STOP_WORDS_DIR)

    covid_paragraphs = []
    covid_words = []
    counter = 0
    for file in get_file_list(Constant.FILE_PATH):
        counter += 1
        covid_paragraphs += read_paragrahp(Constant.BASE_PATH, file)
        covid_words += list(extraer_datos_fichero(Constant.BASE_PATH, file, {}).keys())

    clean_covid_paragraphs_words = clean_paragraphs(covid_paragraphs, empty_words)
    clean_covid_words = clean_words(covid_words, empty_words)

    # Prueba con ventana 4
    ordered_words = calculate(clean_covid_words, clean_covid_paragraphs_words, 4, Constant.PAGE_RANK4_FILE)
    with open(Constant.CORRELATIONS_FILE, 'a') as rh:
        rh.write("Ventana 4 \n")
    comparate_words(ejercicio1_words, ordered_words)

    # Prueba con ventana 5
    ordered_words = calculate(clean_covid_words, clean_covid_paragraphs_words, 5, Constant.PAGE_RANK5_FILE)
    with open(Constant.CORRELATIONS_FILE, 'a') as rh:
        rh.write("Ventana 5 \n")
    comparate_words(ejercicio1_words, ordered_words)

    # Prueba con ventana 8
    ordered_words = calculate(clean_covid_words, clean_covid_paragraphs_words, 8, Constant.PAGE_RANK8_FILE)
    with open(Constant.CORRELATIONS_FILE, 'a') as rh:
        rh.write("Ventana 8 \n")
    comparate_words(ejercicio1_words, ordered_words)


# END MAIN

if __name__ == "__main__":
    main()
