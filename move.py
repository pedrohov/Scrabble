# Projeto e Analise de Algoritmos (PAA)
# 2o sem/2018 - IFMG - Campus Formiga
# Pedro Henrique Oliveira Veloso (0002346)
# Saulo Ricardo Dias Fernandes   (0021581)

class Move():
    """ Representacao de uma jogada. """
    def __init__(self, word, pos, direction):
        self.word   = word;      # Palavra formada.
        self.pos    = pos;       # Comeco da palavra no tabuleiro (lin, col).
        self.dir    = direction; # Direcao em que a palavra foi formada (esq -> dir, ou cima -> baixo).
        self.value  = 0;         # Valor total da jogada.
        self._value = 0;         # Valor da palavra colocada.

        self.crosswords = [];    # Palavras a mais formadas pela jogada.

        self.brancos = {};       # Informacao das pecas em branco utilizadas na jogada.

    def getWords(self):
        res = self.word + '(' + str(self._value) +')';

        if(len(self.crosswords) > 0):
            for crossword in self.crosswords:
                res += ' ' + crossword[0] + '(' + str(crossword[1]) + ')';

            res = '[' + ", ".join(res.split(' ')) + ']';
            
        return res;

    def parseBrancos(self, brancos):
        """ [IA] Adiciona conjunto de pecas em branco
            utilizadas para formar a jogada.
        """
        for (letra, posicao) in brancos:
            self.brancos[posicao] = letra;
        return;

    def __str__(self):
        return self.word + " (" + str(self.value) + ")" + " [" + str(self.pos[0]) + ", " + str(self.pos[1]) + "]" + " - dir: " + self.dir;