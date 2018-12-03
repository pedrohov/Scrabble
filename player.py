# Projeto e Analise de Algoritmos (PAA)
# 2o sem/2018 - IFMG - Campus Formiga
# Pedro Henrique Oliveira Veloso (0002346)
# Saulo Ricardo Dias Fernandes   (0021581)

from piece import Piece;
from copy  import deepcopy;
from move   import *;

class Player():

    def __init__(self, name, board, dictionary):
        self.name   = name; # Nome do jogador.
        self.hand   = {};   # Pecas na mao do jogador.
        self.words  = [];   # Palavras formadas pelo jogador.
        self.points = 0;    # Pontuacao do jogador.
        self.nPass  = 0;    # Quantidade de vezes que o jogador passou de turno.

        self.board  = board;      # Referencia para a mesa.
        self.dict   = dictionary; # Referencia para o dicionario.

    def play(self, primeira=False):
        move = None;

        while(move is None):
            comando = input("\nInforme a jogada como 'Y X d <palavra>' (Y=linha, X=coluna, D=H/V)\n> ");
            
            # Passou o turno:
            if(comando == 'pass'):
                self.nPass += 1;
                return self.piecesToChange();
            # Sai do jogo:
            elif(comando == 'quit'):
                exit();

            move = self.parseMove(comando, primeira);

        # Faz a jogada se for valida:
        if(move is not None):
            print("Jogada: ", end='')
            print(move)
            self.board.insertWord(move, self);
            self.addWord(move);
            self.nPass = 0;
        
        return {};

    def parseMove(self, entrada, primeira=False):
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

        # Determina a direcao:
        direc = comando[2];
        if(direc.upper() != 'V') and (direc.upper() != 'H'):
            print("Direcao invalida.");
            return None;

        # Determina a palavra:
        palavra = comando[3];
        brancos = self.findBlankPieces(palavra, (lin, col), direc.upper(), primeira);

        # Palavra possui pedras que o jogador nao tem:
        if(brancos is None):
            #print("Nao existem pedras suficientes para formar <" + palavra + ">.");
            return None;

        # Cria uma nova jogada com os dados recebidos:
        jogada = Move(palavra, (lin, col), direc.upper());
        jogada.brancos = brancos;

        # Verifica se a jogada eh valida:
        if(self.board.isValid(jogada, self) == False):
            print("Jogada invalida.");
            return None;

        # Verifica se a jogada utiliza uma palavra no tabuleiro:


        # Determina a pontuacao da jogada:
        jogada.value = self.board.calcMovePoints(jogada);

        # print(comando);

        return jogada;

    def findBlankPieces(self, word, pos, direc, primeira=False):
        """ Verifica se o jogador usou pecas em branco
            para formar a palavra.
        """
        lin = pos[0];
        col = pos[1];
        index = 0;
        brancos = {};
        mao = deepcopy(self.hand);
        ancora = False;

        for l in word:
            if(self.board.matrix[lin][col].isEmpty()):

                # Retira peca da mao:
                if((l in mao) and (mao[l].quantity > 0)):
                    mao[l].quantity -= 1;

                # Retira branco da mao:
                elif(('#' in mao) and (mao['#'].quantity > 0)):
                    mao['#'].quantity -= 1;
                    brancos[index] = l;

                # Jogador nao tem pedras suficientes pra formar a palavra:
                else:
                    print("Nao existem pedras suficientes para formar <" + word + ">.");
                    return None;

            # Jogador tentou substituir pedra do tabuleiro.
            elif(self.board.get(lin, col) != l):
                print("Nao e possivel substituir palavras do tabuleiro.");
                return None; 

            # Jogador utilizou uma ancora:
            else:
                ancora = True;

            # Posicao para a proxima peca:
            if(direc == "H"):
                col += 1;
            elif(direc == "V"):
                lin += 1;

            index += 1;

        # Se o jogador nao utilizou uma ancora:
        if(ancora == False) and (primeira == False):
            print("E preciso utilizar ao menos uma pedra do tabuleiro.");
            return None;

        return brancos;

    def firstPlay(self):
        self.play(True);

    def addWord(self, move):
        self.points += move.value;
        self.words.append(move);

    def piecesToChange(self):
        """ Forma um dicionario de pecas para serem trocadas.
            Troca apenas letras que nao sao vogais.
        """
        self.showHand();
        troca  = {};

        while(True):
            comando = input("\nInforme as pecas que deseja trocar (separadas por espaco).\n> ");
            pieces = comando.split(' ');

            # Passou o turno:
            if(pieces[0] == 'pass'):
                return {};

            # Checa se todas as pecas estao na mao do jogador:
            erro = False;
            for l in pieces:
                # Trata apenas pecas em lowercase:
                l = l.lower();
                if(l not in self.hand) or (self.hand[l].quantity == 0):
                    print("Voce nao possui a peca " + l.upper() + ".");
                    erro = True;
                    break;

            # Remove as pecas e forma o conjunto a ser trocado:
            if(not erro):
                for l in pieces:
                    # Trata apenas pecas em lowercase:
                    l = l.lower();

                    # Se nao existir no dicionario, cria uma chave nova:
                    if(l not in troca):
                        troca[l] = 1;
                    # Ou incrementa a quantidade existente:
                    else:
                        troca[l] += 1;

                    # Remove a peca da mao do jogador:
                    self.hand[l].quantity -= 1;

                return troca;
        return {};

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