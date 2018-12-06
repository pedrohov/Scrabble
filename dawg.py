# Projeto e Analise de Algoritmos (PAA)
# 2o sem/2018 - IFMG - Campus Formiga
# Pedro Henrique Oliveira Veloso (0002346)
# Saulo Ricardo Dias Fernandes   (0021581)

import sys;
import time;
import pickle;

class DawgNode:
    NextId = 0
    
    def __init__(self):
        # Dicionario de nos:
        self.edges = {};    	

        # Determina se o no e uma palavra:
        self.final = False;

    def lookup(self, word):
        """ Consulta a partir deste no se a palavra 'word' existe. """
        node = self;
        for letter in word:
            if letter not in node.edges:
                return False
            node = node.edges[letter];

        return node.final; 

class Dawg:
    def __init__(self):
        # Raiz do DAWG:
        self.root = DawgNode();

        # Nos criados:
        self.nodes = [];

    def insert(self, word):
        """ Adiciona uma nova palavra ao DAWG. """

        node = self.root;
        for letter in word:
            if(letter in node.edges):
                node = node.edges[letter];
            else:
                nextNode = DawgNode();
                node.edges[letter] = nextNode;
                node = nextNode;
                self.nodes.append(nextNode);

        node.final = True;

    def lookup(self, word):
        node = self.root;
        for letter in word:
            if letter not in node.edges:
                return False
            node = node.edges[letter];

        return node.final;    

    def nodeCount(self):
        return len(self.nodes);

    def edgeCount(self):
        count = 0;
        for node in self.nodes:
            count += len(node.edges);
        return count;

    def create(self, local):
        WordCount = 0;
        words = open(local, "rt").read().split();
        words.sort();
        start = time.time(); 
        for word in words:
            WordCount += 1;
            dawg.insert(word);
            if ((WordCount % 100) == 0):
                print("%d" % WordCount);
        print("A criacao do DAWG demorou %g s" % (time.time()-start));

        EdgeCount = dawg.edgeCount();
        print("Foram lidas %d palavras em %d nos e %d arestas" % (WordCount, dawg.nodeCount(), EdgeCount));

    def save(self, local):
        file = open(local, "wb");
        pickle.dump(self, file);
        file.close();

def load(local):
    file = open(local, "rb")
    dawg = pickle.load(file);
    file.close();
    return dawg;

if __name__ == "__main__":
    # Criar dawg:
    dawg = Dawg();
    dawg.create("dict.txt");
    dawg.save("dict.dawg");

    # Carregar arq binario:
    #dawg = load("dict.dawg");

    # Pesquisa por palavras passadas por parametro:
    QUERY = sys.argv[1:];
    for word in QUERY:
        if not dawg.lookup( word ):
            print( "%s NAO esta no dicionario." % word)
        else:
            print ("%s esta no dicionario." % word)