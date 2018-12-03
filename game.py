# Projeto e Analise de Algoritmos (PAA)
# 2o sem/2018 - IFMG - Campus Formiga
# Pedro Henrique Oliveira Veloso (0002346)
# Saulo Ricardo Dias Fernandes   (0021581)

from player import *;
from piece  import *;
from move   import *;
from dawg   import *;
from board  import *;
from playerIA import *;

import cProfile;
import re;

class Game():

    def __init__(self, boardFile, dawgFile):
        self.dict  = load(dawgFile).root;
        self.board = Board(boardFile, self.dict);

        self.pieces = {'#': 3, 'a': 14, 'e': 11, 'i': 10, 'o': 10,
                       's': 8, 'u': 7 , 'm': 6 , 'r': 6 , 't': 5 ,
                       'd': 5, 'l': 5 , 'c': 4 , 'p': 4 , 'n': 4 ,
                       'b': 3, 'ç': 2 , 'f': 2 , 'g': 2 , 'h': 2 ,
                       'v': 2, 'j': 2 , 'q': 1 , 'x': 1 , 'z': 1 };

        self.player1 = None;
        self.player2 = None;

    def start(self):

        # Definir jogador Humano/Computador:
        opcao = 0;
        while(opcao < 1) or (opcao > 3):
            try:
                opcao = int(input("\nSCRABBLE\n1 - Jogador vs Jogador.\n2 - Jogador vs Com\n3 - Com vs Com\n\nOpcao: "));
            except ValueError:
                opcao = 0;

        print("");
        self.setupPlayers(opcao);

        # Loop de jogadas:
        self.run();

    def run(self):
        """ Loop de jogo """
        firstPlay = True;

        while(True):
            # Mostra o estado atual do jogo:
            self.showBoard();

            # Faz a jogada do jogador atual:
            (pecasTrocar, jogada) = self.turn.play(firstPlay);

            # Mostra a jogada feita:
            self.showMove(jogada);

            # Determina se nao e mais a primeira jogada:
            if(jogada is not None) and (firstPlay):
                firstPlay = False;

            # Se o jogador passar o turno
            # troca as pecas da mao que ele pedir para trocar:
            self.changePieces(pecasTrocar, self.turn);

            # Passa o turno do jogador atual:
            self.changeTurn();

            # Checa se o jogo chegou ao fim (ambos os jogadores passaram 2x):
            self.isGameOver();

    def startingHand(self):
        """ Sorteia uma mao inicial e a retorna como dicionario de Pieces."""
        res = {};
        i = 0;
        while(i < 7):
            # Sorteia uma peca aleatoria:
            (piece, qtd) = random.choice(list(self.pieces.items()));
            if(qtd > 0):
                # Remove a peca do saquinho:
                self.pieces[piece] -= 1;
                i += 1;

                # Adiciona a peca a mao:
                if piece in res:
                    res[piece].quantity += 1;
                else:
                    res[piece] = Piece(piece);

        return res;

    def changePieces(self, pieces, player):
        """ Troca as pecas selecionadas pelo jogador.
            No final da troca passa o turno.
            Se nao for informada nenhuma peca, apenas passa o turno.
        """

        # Checa se existem pecas suficiente para fazer a troca:
        qtdPedida = 0;
        qtdSaquinho = 0;
        for piece, quantity in self.pieces.items():
            if quantity > 0:
                qtdSaquinho += 1;

        for piece, quantity in pieces.items():
            if quantity > 0:
                qtdPedida += 1;

        # Foram pedidas mais pecas do que existe no saquinho:
        if(qtdPedida > qtdSaquinho):
            print("Nao existem pecas suficientes para fazer a troca.");
            return;

        for piece, quantity in pieces.items():
            # Sorteia uma nova peca aleatoria:
            (new, qtd) = random.choice(list(self.pieces.items()));

            # Garante que foi sorteada uma peca que esta no saquinho:
            while(qtd == 0):
                (new, qtd) = random.choice(list(self.pieces.items()));

            # Adiciona a nova peca a mao do jogador:
            if(new not in player.hand):
                player.hand[new] = Piece(new);
            else:
                player.hand[new].quantity += 1;

            # Adiciona a peca antiga ao saquinho do jogo:
            self.pieces[piece] += 1;

        return;


    def showBoard(self):
        #print(self.board);
        self.board.show(self.player1, self.player2);
        print(self.player1.__str__() + "\t" + self.turn.showHand() + "\t" + self.player2.__str__());

    def changeTurn(self):
        """ Troca o turno do jogador atual.
            Reseta as informacoes utilizadas para criar a jogada.
        """
        if(self.turn == self.player1):
            self.turn = self.player2;
            self.player1.reset();
        else:
            self.turn = self.player1;
            self.player2.reset();

    def setupPlayers(self, opcao):
        if(opcao == 1):
            self.player1 = Player("JOGADOR 1", self.board, self.dict);
            self.player2 = Player("JOGADOR 2", self.board, self.dict);
        elif(opcao == 2):
            self.player1 = Player("JOGADOR", self.board, self.dict);
            self.player2 = PlayerIA("COMPUTADOR", self.board, self.dict);
        else:
            self.player1 = PlayerIA("COM1", self.board, self.dict);
            self.player2 = PlayerIA("COM2", self.board, self.dict);

        self.player1.hand = self.startingHand();
        self.player2.hand = self.startingHand();

        # Sorteia um jogador para comecar:
        if(random.choice([True, False])):
            self.turn = self.player1;
        else:
            self.turn = self.player2;

    def showMove(self, move):
        if(move is not None):
            print("\n# O jogador " + self.turn.name + " colocou " + move.word + " por " + str(move.value) + " pontos.\n");
        else:
            print("\n# O jogador " + self.turn.name + " passou o turno.\n");

    def isGameOver(self):
        if(self.player1.nPass >= 2) and (self.player2.nPass >= 2):
            print("Fim do jogo.");
            exit();


if __name__ == "__main__":
    jogo = Game("board.txt", "dict.dawg");
    jogo.start();