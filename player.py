# Projeto e Analise de Algoritmos (PAA)
# 2o sem/2018 - IFMG - Campus Formiga
# Pedro Henrique Oliveira Veloso (0002346)
# Saulo Ricardo Dias Fernandes   (0021581)

from piece import Piece;
from copy  import deepcopy;
from move   import *;

class Player():

    def __init__(self, name, board, dictionary):
        self.name   = name;
        self.hand   = {};
        self.words  = [];
        self.points = 0;

        self.board    = board;
        self.dict     = dictionary;

    def play(self):
        move = None;

        while(move is None):
            comando = input("\nInforme a jogada como 'Y X d <palavra>' (Y=linha, X=coluna, D=H/V)\n> ");
            move = self.parseMove(comando);

    def parseMove(self, entrada):
        """ Recebe uma linha do terminal, 
            cria uma nova Move() e a valida.
            Insere a jogada no tabuleiro se for valida.
        """
        comando = entrada.split(' ');
        jogada  = None;

        # Determina a linha:
        lin = comando[0];
        if(lin.upper() == 'A'):
            lin = 10;
        elif(lin.upper() == 'B'):
            lin = 11;
        elif(lin.upper() == 'C'):
            lin = 12;
        elif(lin.upper() == 'D'):
            lin = 13;
        elif(lin.upper() == 'E'):
            lin = 14;
        elif(lin >= '0') and (lin <= '9'):
            lin = int(lin);
        else:
            print("Linha invalida.");
            return None;

        # Determina a coluna:
        col = comando[1];
        if(col.upper() == 'A'):
            col = 10;
        elif(col.upper() == 'B'):
            col = 11;
        elif(col.upper() == 'C'):
            col = 12;
        elif(col.upper() == 'D'):
            col = 13;
        elif(col.upper() == 'E'):
            col = 14;
        elif(col >= '0') and (col <= '9'):
            col = int(col);
        else:
            print("Coluna invalida.");
            return None;

        direc = comando[2];
        if(direc.upper() != 'V') and (direc.upper() != 'H'):
            print("Direcao invalida.");
            return None;

        palavra = comando[3];
        brancos = self.findBlankPieces(palavra);

        if(brancos is None):
            print("Nao existem pedras suficientes para formar <" + palavra + ">.");
            return None;

        print(comando);
        jogada = Move(palavra, (lin, col), direc);
        jogada.brancos = brancos;

        return jogada;

    def findBlankPieces(self, word):
        """ Verifica se o jogador usou pecas em branco
            para formar a palavra.
        """
        brancos = {};
        mao = deepcopy(self.hand);
        index = 0;
        for l in word:
            # Retira peca da mao:
            if((l in mao) and (mao[l].quantity > 0)):
                mao[l].quantity -= 1;
            # Retira branco da mao:
            elif(('#' in mao) and (mao['#'].quantity > 0)):
                mao['#'].quantity -= 1;
                brancos[index] = l;

            # Jogador nao tem pedras suficientes pra formar a palavra:
            else:
                return None;

            index += 1;

        return brancos;

    def firstPlay(self):
        self.play();

    def addWord(self, move):
        self.points += move.value;
        self.words.append(move);

    def showHand(self):
        res = "";
        for letter, piece in self.hand.items():
            for i in range(piece.quantity):
                res += letter.upper() + " ";
        print(res);

    def __str__(self):
        return self.name;

    def reset(self):
        return;