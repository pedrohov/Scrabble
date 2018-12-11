# Projeto e Analise de Algoritmos (PAA)
# 2o sem/2018 - IFMG - Campus Formiga
# Pedro Henrique Oliveira Veloso (0002346)
# Saulo Ricardo Dias Fernandes   (0021581)

import random;
from piece import *;
from copy import deepcopy;

class BNode():
    """ Uma posicao do tabuleiro. """
    def __init__(self, multLabel, multiplier, lin, col):
        self.value = ' ';                 # Caractere colocado no tabuleiro.
        self.multiplier = multiplier;     # Multiplier de (letras, palavras).
        self.multiplierLabel = multLabel; # Label exibida no tabuleiro.
        self.pos = (lin, col);

    def isEmpty(self):
        if self.value == ' ':
            return True;
        return False;

    def place(self, letter):
        self.value = letter;

    def remove(self):
        self.value = ' ';

    def __str__(self):
        return "Value: " + str(self.value) + ". Mult: " + self.multiplierLabel + ". (" + str(self.pos[0]) + ", " + str(self.pos[1]) + ").";

class Board():
    """ Mantem o estado atual do tabuleiro.
        Valida e adiciona novas palavras ao tabuleiro.
    """
    def __init__(self, boardFile, root):
        self.matrix = [];                     # Estado atual do tabuleiro.
        self.boardFile = boardFile;           # Arquivo de origem do tabuleiro.
        self.dict = root;                     # Dicionario.
        self.loadBoardFile(boardFile);        # Carregar tabuleiro.

    def loadBoardFile(self, local):
        i = 0;
        j = 0;
        with open(local) as file:
            for line in file:
                lineList = line.split();      # Divide a string em uma lista.
                nodeList = [];                # Linha de nodes.
                for mult in lineList:         # Cria um node para cada coluna.
                    multiplier = (1, 1);
                    multLabel = "1";
                    if(mult == "DL"):         # DL: Dobra pontuacao da letra.
                        multLabel  = "-";
                        multiplier = (2, 1);
                    elif(mult == "TL"):       # TL: Triplica pontuacao da letra.
                        multLabel = "+";
                        multiplier = (3, 1);
                    elif(mult == "DP"):       # DP: Dobra pontuacao da palavra.
                        multLabel = "*";
                        multiplier = (1, 2);
                    elif(mult == "TP"):       # TP: Triplica pontuacao da palavra.
                        multLabel = "@";
                        multiplier = (1, 3);
                    elif(mult == "*"):        #  *: Pontuacao inicial.
                        multLabel = "$"
                        multiplier = (1, 2);

                    nodeList.append(BNode(multLabel, multiplier, i, j));
                    j += 1;
                j = 0;
                i += 1;
                self.matrix.append(nodeList);       # Adiciona linha ao tabuleiro.

    def isValid(self, move, player):
        """ Checa se uma nova pedra colocada no tabuleiro
            gera palavras cruzadas validas.

            1o) Checa se a palavra existe no dicionario.
            2o) Checa se a palavra utiliza um ponto ancora.
            3o) Checa se gera outras palavras cruzadas validas.
        """

        # 1o) Se a palavra nao existir no dicionario
        # ou possuir menos do que dois caracteres
        # a jogada eh invalida:
        if((self.dict.lookup(move.word) == False) or (len(move.word) < 2)):
            return False;

        # 2o) A nova jogada deve utilizar uma peca do tabuleiro:
        lin = move.pos[0];
        col = move.pos[1];
        utilizaAncora = False;

        for l in move.word:
            if(self.get(lin, col) == l):
                utilizaAncora = True;
                break;

            # Determina proxima posicao:
            if(move.dir == 'H'):
                col += 1;
            elif(move.dir == 'V'):
                lin += 1;

        # Nao utiliza ancora e nao eh a primeira jogada:
        if(utilizaAncora == False) and (self.get(7, 7) != ' '):
            return False;

        # 3o) A nova jogada nao deve criar outras palavras invalidas:
        lin = move.pos[0];
        col = move.pos[1];

        for l in move.word:

            crossword = "";
            empty = False;

            if(move.dir == "H"):
                if(self.get(lin, col) == ' '):
                    # Coloca a letra atual no tabuleiro:
                    self.getSquare(lin, col).place(l);

                    # Procura o inicio da palavra:
                    _lin = lin;
                    pedra = self.get(_lin, col);
                    while(pedra != ' '):
                        _lin -= 1;
                        pedra = self.get(_lin, col);

                    # Concatena as pedras da palavra:
                    _lin += 1;
                    pedra = self.get(_lin, col);
                    while(pedra != ' '):
                        _lin += 1;
                        crossword += pedra;
                        pedra = self.get(_lin, col);

                    # Retira a letra atual do tabuleiro:
                    self.getSquare(lin, col).remove();

                # Checa a proxima posicao:
                col += 1;
            elif(move.dir == "V"):
                if(self.get(lin, col) == ' '):
                    # Coloca a letra atual no tabuleiro:
                    self.getSquare(lin, col).place(l);

                    # Procura o inicio da palavra:
                    _col = col;
                    pedra = self.get(lin, _col);
                    while(pedra != ' '):
                        _col -= 1;
                        pedra = self.get(lin, _col);

                    # Concatena as pedras da palavra:
                    _col += 1;
                    pedra = self.get(lin, _col);
                    while(pedra != ' '):
                        _col += 1;
                        crossword += pedra;
                        pedra = self.get(lin, _col);

                    # Retira a letra atual do tabuleiro:
                    self.getSquare(lin, col).remove();

                # Checa a proxima posicao:
                lin += 1;

            # Crossword formada nao esta no dicionario:
            # Ignora palavras de tamanho 2.
            if(len(crossword) > 2):
                if (self.dict.lookup(crossword)):
                    move.crosswords.append((crossword, 0));
                else:
                    return False;

        return True;

    def insertWord(self, move, player):
        """ Insere uma jogada valida no tabuleiro. """
        lin = move.pos[0];
        col = move.pos[1];

        index = 0;
        for l in move.word:
            if(self.getSquare(lin, col).isEmpty()):
                # Checa se uma pedra em branco foi utilizada:
                if(index in move.brancos):
                    player.hand['#'].quantity -= 1;
                else:
                    player.hand[l].quantity -= 1;

            index += 1;

            # Coloca a letra na posicao:
            self.getSquare(lin, col).place(l);

            # Posicao para a proxima peca:
            if(move.dir == "H"):
                col += 1;
            elif(move.dir == "V"):
                lin += 1;

        return;

    def addWordCrosscheck(self, move):
        """ Adiciona a palavra no tabuleiro para auxiliar a checagem de palavras cruzadas. """
        lin = move.pos[0];
        col = move.pos[1];

        for l in move.word:
    
            # Coloca a letra na posicao:
            self.getSquare(lin, col).place(l);

            # Posicao para a proxima peca:
            if(move.dir == "H"):
                col += 1;
            elif(move.dir == "V"):
                lin += 1;


    def remWordCrosscheck(self, move):
        """ Remove a palavra do tabuleiro para auxiliar a checagem de palavras cruzadas. """
        lin = move.pos[0];
        col = move.pos[1];

        for l in move.word:
    
            # Remove a letra da posicao:
            self.getSquare(lin, col).remove();

            # Posicao para a proxima peca:
            if(move.dir == "H"):
                col += 1;
            elif(move.dir == "V"):
                lin += 1;

    def calcMovePoints(self, move):
        lin = move.pos[0];
        col = move.pos[1];	
        pts = 0;
        multWord = 1;
        index = 0;

        # Calcula pontuacao da palavra:
        for l in move.word:
            # Pega dados da pedra:
            if(index in move.brancos):
                pt = Piece.getLetterData('#', l)[0];
            else:
                pt = Piece.getLetterData(Piece, l)[0];

            square = self.getSquare(lin, col);
            multWord = multWord * square.multiplier[1];
            pts = pts + pt * square.multiplier[0];

            if(move.dir == 'H'):
                col += 1;
            elif(move.dir == 'V'):
                lin += 1;

            index += 1;

        pts = pts * multWord;
        move._value = pts;

        # Calcula pontuacao das demais:
        lin = move.pos[0];
        col = move.pos[1];
        index = 0; # Index dos coringas utilizados na palavra.
        extra = 0; # Index das palavras a mais formadas pela jogada.
        for l in move.word:

            crossword = "";
            empty = False;

            # Pega dados da pedra:
            if(index in move.brancos):
                _pt = Piece.getLetterData('#', l)[0];
            else:
                _pt = Piece.getLetterData(Piece, l)[0];

            index += 1;     # Incrementa o index dos coringas.
            _multWord = 1;  # Multiplicador de palavras das palavras adicionais.
            _pts = 0;       # Pontuacao das palavras adicionais.

            if(move.dir == "H"):
                if(self.get(lin, col) == ' '):
                    # Coloca a letra atual no tabuleiro:
                    self.getSquare(lin, col).place(l);

                    # Procura o inicio da palavra:
                    _lin = lin;
                    pedra = self.get(_lin, col);
                    while(pedra != ' '):
                        _lin -= 1;
                        pedra = self.get(_lin, col);

                    # Concatena as pedras da palavra e calcula a pontuacao:
                    _lin += 1;
                    square = self.getSquare(_lin, col);
                    while(square is not None) and (square.value != ' '):
                        _lin += 1;
                        crossword += square.value;
                        
                        _multWord = _multWord * square.multiplier[1];
                        _pts = _pts + _pt * square.multiplier[0];

                        square = self.getSquare(_lin, col);

                    # Retira a letra atual do tabuleiro:
                    self.getSquare(lin, col).remove();
                    _pts = _pts * _multWord;

                # Checa a proxima posicao:
                col += 1;
            elif(move.dir == "V"):
                if(self.get(lin, col) == ' '):
                    # Coloca a letra atual no tabuleiro:
                    self.getSquare(lin, col).place(l);

                    # Procura o inicio da palavra:
                    _col = col;
                    pedra = self.get(lin, _col);
                    while(pedra != ' '):
                        _col -= 1;
                        pedra = self.get(lin, _col);

                    # Concatena as pedras da palavra e calcula a pontuacao:
                    _col += 1;
                    square = self.getSquare(lin, _col);
                    while(square is not None) and (square.value != ' '):
                        _col += 1;
                        crossword += square.value;

                        _multWord = _multWord * square.multiplier[1];
                        _pts = _pts + _pt * square.multiplier[0];

                        square = self.getSquare(lin, _col);

                    # Retira a letra atual do tabuleiro:
                    self.getSquare(lin, col).remove();
                    _pts = _pts * _multWord;

                # Checa a proxima posicao:
                lin += 1;

            # Crossword formada nao esta no dicionario:
            # Ignora palavras de tamanho 2.
            if(len(crossword) > 2) and (self.dict.lookup(crossword)):
                # Se existir atualiza a pontuacao das crosswords:
                move.crosswords[extra] = (move.crosswords[extra][0], _pts);
                extra += 1;

                # Da pontuacao total:
                pts = pts + _pts;

        return pts;

    def get(self, lin, col):
        # Garante que recebeu linha e coluna validos:
        if((lin < 0) or (lin > 14) or (col < 0) or (col > 14)):
            return ' ';
        return self.matrix[lin][col].value;

    def getSquare(self, lin, col):
        # Garante que recebeu linha e coluna validos:
        if((lin < 0) or (lin > 14) or (col < 0) or (col > 14)):
            return None;
        return self.matrix[lin][col];

    def show(self, p1, p2):
        palavrasP1 = deepcopy(p1.words);
        palavrasP2 = deepcopy(p2.words);
        maxchar = 35;

        board = "    0 1 2 3 4 5 6 7 8 9 A B C D E\n";
        board = board + "    - - - - - - - - - - - - - - -\n";
        for i in range(len(self.matrix) - 1):

            lineIndex = str(i);

            # Exibe index da linha:
            if(i == 10):
                lineIndex = "A";
            elif(i == 11):
                lineIndex = "B";
            elif(i == 12):
                lineIndex = "C";
            elif(i == 13):
                lineIndex = "D";
            elif(i == 14):
                lineIndex = "E";

            board = board + lineIndex + "| ";

            for j in range(len(self.matrix[0]) - 1):
                node = self.matrix[i][j];
                if(node.value == ' ') and (node.multiplierLabel != '1'):
                    board = board + " " + node.multiplierLabel;
                else:
                    board = board + " " + node.value.upper();
            
            # Exibe index da linha:
            board = board + " |" + lineIndex;

            # Coloca dados das palavras dos jogadores:
            if(i > 8):
                
                nchars = 0;
                res = "";

                if(len(palavrasP2) > 0):
                    word = palavrasP2.pop();
                    res += word + " ";
                    nchars = len(word);

                while(nchars <= maxchar) and (len(palavrasP2) > 0):
                    nchars += len(palavrasP2[len(palavrasP2) - 1]);
                    if(nchars > maxchar):
                        break;

                    word = palavrasP2.pop();
                    res += word + " ";
                    
                board += "\t" + res;

            elif(i == 8):
                board += "\tPalavras do " + p2.name + ":";
            elif(i > 0):
                nchars = 0;
                res = "";

                if(len(palavrasP1) > 0):
                    word = palavrasP1.pop();
                    res += word + " ";
                    nchars = len(word);

                while(nchars <= maxchar) and (len(palavrasP1) > 0):
                    nchars += len(palavrasP1[len(palavrasP1) - 1]);
                    if(nchars > maxchar):
                        break;

                    word = palavrasP1.pop();
                    res += word + " ";
                    
                board += "\t" + res;
            else:
                board += "\tPalavras do " + p1.name + ":";

            board += "\n";

        board = board + "    - - - - - - - - - - - - - - -\n";
        board = board + "    0 1 2 3 4 5 6 7 8 9 A B C D E\n";
            
        print(board);


if __name__ == "__main__":
    board = Board("board.txt");
    print(board);