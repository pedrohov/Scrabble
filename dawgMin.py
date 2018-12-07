# Projeto e Analise de Algoritmos (PAA)
# 2o sem/2018 - IFMG - Campus Formiga
# Pedro Henrique Oliveira Veloso (0002346)
# Saulo Ricardo Dias Fernandes   (0021581)

# Adaptado de: Steve Hanov, 2011. Released to the public domain.

import sys;
import time;
import pickle;

class DawgNode:
    NextId = 0
    
    def __init__(self):
    	# Id para auxiliar na minimizacao:
        self.id = DawgNode.NextId;
        DawgNode.NextId += 1;

        # Determina se o no e uma palavra:
        self.final = False;

        # Dicionario de nos:
        self.edges = {};

        # Numero de nos alcancados por este no:
        self.count = 0

    def __str__(self):        
        arr = [];
        if self.final: 
            arr.append("1")
        else:
            arr.append("0")

        for (label, node) in self.edges.items():
            arr.append(label);
            arr.append(str(node.id));

        return "_".join(arr)

    def __hash__(self):
        return self.__str__().__hash__();

    def __eq__(self, other):
        return self.__str__() == other.__str__();

    def numReachable(self):
        # Se o no ja possui uma contagem, retorna ela:
        if self.count:
            return self.count;

        # Conta o numero de nos finais alcancaveis a partir deste,
        # incluindo ele mesmo:
        count = 0;
        if self.final:
            count += 1;
        for label, node in self.edges.items():
            count += node.numReachable();

        self.count = count;
        return count;

    def lookup(self, word):
        """ Consulta a partir deste no se a palavra 'word' existe. """
        node = self;
        for letter in word:
            if letter not in node.edges:
                return False
            node = node.edges[letter];

        return node.final; 

class DawgMin:
    def __init__(self):

        # Raiz do DAWG:
        self.root = DawgNode();

        # Checa se as palavras estao em ordem alfabetica:
        self.previousWord = "";
        
        # Nos nao checados por duplicacao:
        self.uncheckedNodes = [];

        # Nos unicos. Checados por duplicacao:
        self.minimizedNodes = {};

    def insert(self, word):
        """ Adiciona uma nova palavra ao DAWG. """

        if(word < self.previousWord):
            raise Exception("Erro: As palavras devem ser fornecidas em ordem alfabetica.");

        # Acha um prefixo em comum com a palavra atual e previousWord:
        commonPrefix = 0;
        for i in range(min(len(word), len(self.previousWord))):
            if word[i] != self.previousWord[i]:
                break;
            commonPrefix += 1;

        # Checa por nos redundantes
        # Check the uncheckedNodes for redundant nodes, proceeding from last
        # one down to the common prefix size. Then truncate the list at that
        # point.
        self.minimize(commonPrefix);

        # Adiciona o sufixo, comencando pelo no intermediario do grafo:
        if(len(self.uncheckedNodes) == 0):
            node = self.root;
        else:
            node = self.uncheckedNodes[-1][2];

        for letter in word[commonPrefix:]:
            nextNode = DawgNode();
            node.edges[letter] = nextNode;
            self.uncheckedNodes.append((node, letter, nextNode));
            node = nextNode;

        node.final = True;
        self.previousWord = word;

    def finish(self):
        # Minimiza todos os nos nao checados:
        self.minimize(0);

    def minimize(self, downTo):
        # Procede da raiz ate o ponto especificado por downTo:
        for i in range(len(self.uncheckedNodes) - 1, downTo - 1, -1):
            (parent, letter, child) = self.uncheckedNodes[i];
            if child in self.minimizedNodes:
                # Troca o nodo filho com o ja existente:
                parent.edges[letter] = self.minimizedNodes[child];
            else:
                # Adiciona o estado aos nos ja minimizados:
                self.minimizedNodes[child] = child;
            self.uncheckedNodes.pop();

    def lookup(self, word):
        node = self.root;
        for letter in word:
            if letter not in node.edges:
                return False
            node = node.edges[letter];

        return node.final;    

    def nodeCount(self):
        return len(self.minimizedNodes);

    def edgeCount(self):
        count = 0;
        for node in self.minimizedNodes:
            count += len(node.edges);
        return count;

    def create(self, local):
        WordCount = 0;
        words = open(local, "rt", encoding="latin1").read().split();
        words.sort();
        start = time.time(); 
        for word in words:
            WordCount += 1;
            dawg.insert(word);
            if ((WordCount % 100) == 0):
                print("%d" % WordCount);
        dawg.finish();
        print("A criacao do DAWG demorou %g s" % (time.time()-start));

        EdgeCount = dawg.edgeCount();
        print("Foram lidas %d palavras em %d nos e %d arestas" % (WordCount, dawg.nodeCount(), EdgeCount));

    def save(self, local):
        file = open(local, "wb");
        pickle.dump(self, file);
        file.close();

def load(local):
    file = open(local, "rb");
    dawg = pickle.load(file);
    file.close();
    return dawg;

if __name__ == "__main__":
    # Criar dawg:
    dawg = DawgMin();
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