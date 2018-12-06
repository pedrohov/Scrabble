# Projeto e Analise de Algoritmos (PAA)
# 2o sem/2018 - IFMG - Campus Formiga
# Pedro Henrique Oliveira Veloso (0002346)
# Saulo Ricardo Dias Fernandes   (0021581)

import random;
from piece import *;
from copy import deepcopy;

class BNode():
    """ Uma posicao do tabuleiro. """
    def __init__(self, multiplier, lin, col):
        self.value = ' ';
        self.empty = True;
        self.multiplier = multiplier;
        self.pos = (lin, col);

    def isEmpty(self):
        return self.empty;

    def place(self, letter):
        self.value = letter;
        self.empty = False;

    def remove(self):
        self.value = ' ';
        self.empty = True;

    def __str__(self):
        return "Value: " + str(self.value) + ". Mult: " + self.multiplier + ". (" + str(self.pos[0]) + ", " + str(self.pos[1]) + ").";

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
                    multiplier = "1";
                    if(mult == "DL"):         # DL: Dobra pontuacao da letra.
                        multiplier = "-";
                    elif(mult == "TL"):       # TL: Triplica pontuacao da letra.
                        multiplier = "+";
                    elif(mult == "DP"):       # DP: Dobra pontuacao da palavra.
                        multiplier = "*";
                    elif(mult == "TP"):       # TP: Triplica pontuacao da palavra.
                        multiplier = "@";
                    elif(mult == "*"):        #  *: Pontuacao inicial.
                        multiplier = "$";

                    nodeList.append(BNode(multiplier, i, j));
                    j += 1;
                j = 0;
                i += 1;
                self.matrix.append(nodeList);       # Adiciona linha ao tabuleiro.

    def isValid(self, move, player):
        """ Checa se uma nova pedra colocada no tabuleiro
            gera palavras cruzadas validas.
        """

        # Se a palavra nao existir no dicionario
        # ou possuir menos do que dois caracteres
        # a jogada eh invalida:
        if((self.dict.lookup(move.word) is False) or (len(move.word) < 2)):
            return False;

        lin = move.pos[0];
        col = move.pos[1];
        utilizaAncora = False;

        for l in move.word:

            _lin = lin;
            _col = col;
            crossWord = "";

            # Nao checa palavras ja existentes (ancora):
            if(self.matrix[lin][col].isEmpty()):

                # Adiciona a letra no tabuleiro para verificacao:
                self.matrix[lin][col].place(l);

                # Direcao horizontal checa por crosswords verticais:
                if(move.dir == 'H'):

                    # Busca o inicio da palavra:
                    pedra = self.get(_lin, _col);
                    while(pedra != ' '):
                        _lin -= 1;
                        pedra = self.get(_lin, _col);

                    # Forma a palavra:
                    _lin += 1;
                    pedra = self.get(_lin, _col);
                    while(pedra != ' '):
                        _lin += 1;
                        crossWord += pedra;
                        pedra = self.get(_lin, _col);

                    #print("> " + move.word + " Vertical: " + crossWord + " (" + str(_lin) + ", " + str(_col) + ")");

                # Direcao vertical checa por crosswords horizontais:
                elif(move.dir == 'V'):

                    # Busca o inicio da palavra:
                    pedra = self.get(_lin, _col);
                    while(pedra != ' '):
                        _col -= 1;
                        pedra = self.get(_lin, _col);

                    # Forma a palavra:
                    _col += 1;
                    pedra = self.get(_lin, _col);
                    while(pedra != ' '):
                        _col += 1;
                        crossWord += pedra;
                        pedra = self.get(_lin, _col);

                    #print("> " + move.word + " Horizontal: " + crossWord + " (" + str(lin) + ", " + str(_col) + ")");

                # Remove a letra do tabuleiro:
                self.matrix[lin][col].remove();

                # Determina se a letra formada eh valida:
                if(len(crossWord) <= 2):
                    continue;
                if(self.dict.lookup(crossWord) is False):
                    #print("NAO valido");
                    return False;

            # Utilizou uma posicao do tabuleiro.
            elif(self.get(lin, col) == l):
                utilizaAncora = True; 

             # Tentou substituir uma letra do tabuleiro.
            else:
                return False;

            # Determina proxima posicao:
            if(move.dir == 'H'):
                col += 1;
            elif(move.dir == 'V'):
                lin += 1;

        return True;

    def insertWord(self, move, player):
        """ Insere uma jogada valida no tabuleiro. """
        lin = move.pos[0];
        col = move.pos[1];

        #print(player.showHand());

        index = 0;
        for l in move.word:
            if(self.matrix[lin][col].isEmpty()):
                # Checa se uma pedra em branco foi utilizada:
                if(index in move.brancos):
                    player.hand['#'].quantity -= 1;
                    #print("Coloquei # em (" + str(lin) + ", " + str(col) + ").");
                else:
                    player.hand[l].quantity -= 1;
                    #print("Coloquei " + l + " em (" + str(lin) + ", " + str(col) + ").");

            index += 1;

            # Coloca a letra na posicao:
            self.matrix[lin][col].place(l);

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
            self.matrix[lin][col].place(l);

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
    
            # Coloca a letra na posicao:
            self.matrix[lin][col].remove();

            # Posicao para a proxima peca:
            if(move.dir == "H"):
                col += 1;
            elif(move.dir == "V"):
                lin += 1;

    def calcMovePoints(self, move):
        lin = move.pos[0];
        col = move.pos[1];

        pts = 0;
        ptsPalavrasAdd = 0;
        multWord = 1;
        index = 0;

        for l in move.word:

            # Pontuacao da palavra atual:
            # Pega dados da pedra:
            if(index in move.brancos):
                pt = Piece.getLetterData('#', l)[0];
            else:
                pt = Piece.getLetterData(Piece, l)[0];

            square = self.matrix[lin][col];
            if((square.multiplier == "$") or (square.multiplier == "*")):
                multWord = multWord * 2;
                pts = pts + pt;
            elif(square.multiplier == "-"):
                pts = pts + pt * 2;
            elif(square.multiplier == "+"):
                pts = pts + pt * 3;
            elif(square.multiplier == "@"):
                multWord = multWord * 3;
            else:
                pts = pts + pt;

            # Pontuacao de eventuais palavras formadas a mais:
            _lin = lin;
            _col = col;
            _pts = 0;
            _multWord = 1;
            crossWord = "";

            # Nao checa palavras ja existentes (ancora):
            if(self.matrix[lin][col].isEmpty()):

                # Adiciona a letra no tabuleiro para verificacao:
                self.matrix[lin][col].place(l);

                # Direcao horizontal checa por crosswords verticais:
                if(move.dir == 'H'):

                    # Busca o inicio da palavra:
                    pedra = self.get(_lin, _col);
                    while(pedra != ' '):
                        _lin -= 1;
                        pedra = self.get(_lin, _col);

                    # Forma a palavra:
                    _lin += 1;
                    pedra = self.get(_lin, _col);
                    while(pedra != ' '):
                        _lin += 1;
                        crossWord += pedra;

                        # Adiciona pontuacao:
                        _pt = Piece.getLetterData(Piece, pedra)[0];
                        square = self.getSquare(_lin, _col);
                        if(square is None):
                            break;

                        if((square.multiplier == "$") or (square.multiplier == "*")):
                            _multWord = _multWord * 2;
                            _pts = _pts + _pt;
                        elif(square.multiplier == "-"):
                            _pts = _pts + _pt * 2;
                        elif(square.multiplier == "+"):
                            _pts = _pts + _pt * 3;
                        elif(square.multiplier == "@"):
                            _multWord = _multWord * 3;
                        else:
                            _pts = _pts + _pt;

                        pedra = self.get(_lin, _col);

                # Direcao vertical checa por crosswords horizontais:
                elif(move.dir == 'V'):

                    # Busca o inicio da palavra:
                    pedra = self.get(_lin, _col);
                    while(pedra != ' '):
                        _col -= 1;
                        pedra = self.get(_lin, _col);

                    # Forma a palavra:
                    _col += 1;
                    pedra = self.get(_lin, _col);
                    while(pedra != ' '):
                        _col += 1;
                        crossWord += pedra;

                        # Adiciona pontuacao:
                        _pt = Piece.getLetterData(Piece, pedra)[0];
                        square = self.getSquare(_lin, _col);
                        if(square is None):
                            break;

                        if((square.multiplier == "$") or (square.multiplier == "*")):
                            _multWord = _multWord * 2;
                            _pts = _pts + _pt;
                        elif(square.multiplier == "-"):
                            _pts = _pts + _pt * 2;
                        elif(square.multiplier == "+"):
                            _pts = _pts + _pt * 3;
                        elif(square.multiplier == "@"):
                            _multWord = _multWord * 3;
                        else:
                            _pts = _pts + _pt;

                        pedra = self.get(_lin, _col);

                # Remove a letra do tabuleiro:
                self.matrix[lin][col].remove();

                # Determina se a letra formada eh valida:
                if(len(crossWord) <= 2):
                    continue;
                if(self.dict.lookup(crossWord) is False):
                    return False;

                # Acumula pontos de palavras formadas a mais:
                ptsPalavrasAdd += _pts;

            # Determina proxima posicao:
            if(move.dir == 'H'):
                col += 1;
            elif(move.dir == 'V'):
                lin += 1;

            index += 1;

        pts = pts * multWord;
        pts += ptsPalavrasAdd;

        return pts;

    def calcMovePointsOldie(self, move):
        """ Calcula e define a quantidade de pontos
            de uma jogada valida 'move'.
        """
        lin = move.pos[0];
        col = move.pos[1];
        pts = 0;
        multWord = 1;
        index = 0;

        for l in move.word:
            # Pega dados da pedra:
            if(index in move.brancos):
                pt = Piece.getLetterData('#', l)[0];
            else:
                pt = Piece.getLetterData(Piece, l)[0];

            square = self.matrix[lin][col];
            #print("Pt: " + str(pt) + " / " + square.multiplier + " / Row: " + str(square.pos[0]) + " / Col: " + str(square.pos[1]));
            if((square.multiplier == "$") or (square.multiplier == "*")):
                multWord = multWord * 2;
                pts = pts + pt;
            elif(square.multiplier == "-"):
                pts = pts + pt * 2;
            elif(square.multiplier == "+"):
                pts = pts + pt * 3;
            elif(square.multiplier == "@"):
                multWord = multWord * 3;
            else:
                pts = pts + pt;

            if(move.dir == 'H'):
                col += 1;
            elif(move.dir == 'V'):
                lin += 1;

            index += 1;

        pts = pts * multWord;
        #print(">PALAVRA: " + move.word + ". PTS: " + str(pts));
        return pts;

    def get(self, lin, col):
        if((lin < 0) or (lin > 14) or (col < 0) or (col > 14)):
            return ' ';
        return self.matrix[lin][col].value;

    def getSquare(self, lin, col):
        if((lin < 0) or (lin > 14) or (col < 0) or (col > 14)):
            return None;
        return self.matrix[lin][col];

    def __str__(self):
        # Exibe index da coluna:
        board = "    0 1 2 3 4 5 6 7 8 9 A B C D E\n";
        board = board + "    - - - - - - - - - - - - - - -\n";
        for i in range(len(self.matrix)):

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

            for j in range(len(self.matrix[0])):
                node = self.matrix[i][j];
                if(node.value == ' ') and (node.multiplier != '1'):
                    board = board + " " + node.multiplier;
                else:
                    board = board + " " + node.value.upper();
            
            # Exibe index da linha:
            board = board + " |" + lineIndex + "\n";

        board = board + "    - - - - - - - - - - - - - - -\n";
        board = board + "    0 1 2 3 4 5 6 7 8 9 A B C D E\n";
            
        return board;

    def show(self, p1, p2):
        palavrasP1 = deepcopy(p1.words);
        palavrasP2 = deepcopy(p2.words);
        maxchar = 35;

        board = "    0 1 2 3 4 5 6 7 8 9 A B C D E\n";
        board = board + "    - - - - - - - - - - - - - - -\n";
        for i in range(len(self.matrix)):

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

            for j in range(len(self.matrix[0])):
                node = self.matrix[i][j];
                if(node.value == ' ') and (node.multiplier != '1'):
                    board = board + " " + node.multiplier;
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