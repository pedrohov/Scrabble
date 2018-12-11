# Projeto e Analise de Algoritmos (PAA)
# 2o sem/2018 - IFMG - Campus Formiga
# Pedro Henrique Oliveira Veloso (0002346)
# Saulo Ricardo Dias Fernandes   (0021581)

from player import *;
from random import choice;

class PlayerIA(Player):

    def __init__(self, name, board, dictionary):
        super().__init__(name,  board, dictionary);
        self.anchors  = [];      # Lista de ancoras para formar palavras.
        self.anchor   = None;    # Ancora atual.
        self.bestMove = None;    # Jogada com maior pontuacao.
        self.playDir  = None;    # Direcao da jogada (H/V).
        self.placedNew = False;  # Informa se uma nova peca foi inserida na palavra.

        # Lista de tuplas que informa se foram utilizadas pedras
        # em branco para formar a jogada e a posicao da pedra.
        # Utilizado para calcular o valor da jogada pelo tabuleiro.
        self.brancos = [];

    def play(self, primeira=False):
        """ Determina e realiza a melhor jogada 
            encontrada, tomando 'self.anchors' como
            pontos ancora.
        """

        # Se for a primeira jogada, faca firstPlay:
        if(primeira):
            return self.firstPlay();

        # Determina todos os pontos ancora:
        self.anchors = self.getAnchors();
        # self.debugAnchors();

        for anchor in self.anchors:

            # Define ancora atual:
            self.anchor = (anchor[1].value, anchor[1]);

            # Direcao da jogada:
            self.playDir = anchor[0];

            # Forma palavras:
            self.leftPart("", self.dict, anchor[2], anchor[1]);

        # Faz a melhor jogada encontrada:
        if(self.bestMove is None):
            self.nPass += 1;
            return (self.piecesToChange(), None);
        else:
            self.board.insertWord(self.bestMove, self); # Adiciona a jogada na mesa.
            self.addWord(self.bestMove); # Adiciona a palavra a lista de palavras formadas.
            self.nPass = 0; # Reseta a contagem de turnos passados.
            return ({}, self.bestMove);


    def leftPart(self, word, root, limit, square):
        """ Cria prefixos a esquerda do ponto ancora.
            Sempre que um novo prefixo for formado,
            tenta encontrar as palavras correspondentes.
        """

        # Para cada prefixo formado, cria sufixos:
        self.extendRight(word, root, square);

        # Se houver espaco a esquerda:
        if(limit > 0):
            # Para cada letra possivel:
            for l in root.edges:

                # Demais pedras:
                if(self.hand[l].quantity > 0):
                    self.hand[l].quantity -= 1;
                    newRoot = root.edges[l];
                    self.leftPart(word + l, newRoot, limit - 1, square);
                    self.hand[l].quantity += 1;

                # Trata pedras em branco na mao:
                elif(self.hand['#'].quantity > 0):
                    self.hand['#'].quantity -= 1;
                    newRoot = root.edges[l];
                    
                    # Adiciona a peca em branco a lista:
                    self.brancos.append((l, len(word)));

                    self.leftPart(word + l, newRoot, limit - 1, square);

                    # Remove a pedra em branco da lista:
                    self.brancos.pop();
                    self.hand['#'].quantity += 1;

        return;

    def extendRight(self, word, root, square):
        """ Forma sufixos para um dado prefixo 'word'. 
            Para cada palavra formada cria-se uma nova jogada,
            mantendo a que garantir mais pontos.
        """

        # Posicao atual esta fora do tabuleiro:
        if(square is None):
            return;

        # Define a proxima posicao no tabuleiro:
        nextSquare = None;
        if((self.playDir == "V") and ((square.pos[0] + 1) <= 15)):
            nextSquare = self.board.matrix[square.pos[0] + 1][square.pos[1]];
        elif((self.playDir == "H") and ((square.pos[1] + 1) <= 15)):
            nextSquare = self.board.matrix[square.pos[0]][square.pos[1] + 1];

        if(square.isEmpty()):

            # Cria uma jogada se a palavra estiver marcada como final:
            if(root.final == True):
                # Cria uma nova jogada:
                self.generateMove(word, square);

            for l in root.edges:
                # Define a proxima posicao no dawg:
                newRoot = root.edges[l];

                # Se a letra 'l' esta na mao do jogador:
                if(self.hand[l].quantity > 0):

                    # Remove a peca 'l' da mao do jogador:
                    self.hand[l].quantity -= 1;
                    self.placedNew = True;

                    # Continua a formar palavras a direita:
                    self.extendRight(word + l, newRoot, nextSquare);
                    self.hand[l].quantity += 1;
                    self.placedNew = False;

                # Trata pedras em branco na mao:
                elif(self.hand['#'].quantity > 0):
                    
                    # Remove a peca 'l' da mao do jogador:
                    self.hand['#'].quantity -= 1;
                    self.placedNew = True;

                    # Adiciona a peca em branco a lista:
                    self.brancos.append((l, len(word)));

                    # Continua a formar palavras a direita:
                    self.extendRight(word + l, newRoot, nextSquare);

                    # Remove a pedra em branco da lista:
                    self.brancos.pop();
                    self.hand['#'].quantity += 1;
                    self.placedNew = False;
        else:
            l = square.value;
            if(l in root.edges):
                if(self.playDir == "V"):
                    newRoot = root.edges[l];
                    self.extendRight(word + l, newRoot, nextSquare);
                elif(self.playDir == "H"):
                    newRoot = root.edges[l];
                    self.extendRight(word + l, newRoot, nextSquare);
        return;

    def firstPlay(self):
        """ Faz a primeira jogada. """

        hand = self.hand;
        square = self.board.matrix[7][7];  # Deve utilizar como ancora o centro do tabuleiro.
        self.playDir = choice(['V', 'H']); # Sorteia por fazer uma jogada horizontal ou vertical.
        
        # Cria palavras com todas as pecas da mao do jogador
        # usando cada letra como ancora uma vez:
        for i in range(len(hand)):
            # Pega 'i'esima peca:
            (letter, piece) = list(hand.items())[i];

            if(piece.quantity > 0):
	            hand[letter].quantity -= 1;

	            # Define como ancora:
	            self.anchor = (letter, square);

	            # Forma palavras:
	            self.leftPart("", self.dict, 7, square);

	            # Devolve a peca:
	            hand[letter].quantity += 1;

        # Faz a melhor jogada encontrada:
        if(self.bestMove is None):
            self.nPass += 1;                            # Incrementa a quantidade de turnos passados.
            return (self.piecesToChange(), None);       # (Pedras p/ trocar, Jogada).
        else:
            self.board.insertWord(self.bestMove, self); # Adiciona a jogada na mesa.
            self.addWord(self.bestMove);                # Adiciona a palavra a lista de palavras formadas.
            self.nPass = 0;                             # Reseta a contagem de turnos passados.
            return ({}, self.bestMove);                 # (Pedras p/ trocar, Jogada).

    def generateMove(self, word, square):
        """ Cria uma jogada.
            Mantem a que fizer mais pontos em 'self.bestMove'.
        """

        # Se nao foi colocada nenhuma nova peca
        # a jogada gerada eh invalida:
        if(self.placedNew is False):
            return;

        # Cria a jogada:
        if(self.playDir == "H"):
            # Calcula a posicao no tabuleiro onde a palavra comeca:
            iniY = square.pos[1] - len(word);
            newMove = Move(word, (square.pos[0], iniY), "H");
        elif(self.playDir == "V"):
            anchor = self.anchor[1];
            iniX = square.pos[0] - len(word);
            newMove = Move(word, (iniX, square.pos[1]), "V");

        # print("Move: " + str(newMove),end='')

        # A jogada criada eh invalida:
        if(self.board.isValid(newMove, self) is False):
            # print(" INVALIDA ")
            return;

        # print(" VALIDA")
        # Informa os coringas utilizados se houver:
        newMove.parseBrancos(self.brancos);

        # Calcula a pontuacao da jogada:
        newMove.value = self.board.calcMovePoints(newMove);

        # Mantem a melhor jogada salva em 'self.bestMove':
        if((self.bestMove is None) or (newMove.value > self.bestMove.value)):
            self.bestMove = newMove;

    def getAnchors(self):
        """ Atualiza a lista 'self.anchors' com
            todas as posicoes preenchidas no tabuleiro
            que possuirem uma posicao vazia adjacente. 
        """
        anchors = [];

        # Percorre o tabuleiro:
        for lin in range(len(self.board.matrix)):
            for col in range(len(self.board.matrix[lin])):
                
                # Se a linha for valida:
                if((lin >= 0) and (lin < 15)):
                    # Se a posicao acima estiver vazia, marca esta como ancora:
                    if((self.board.matrix[lin - 1][col].isEmpty()) and (self.board.matrix[lin][col].isEmpty() == False)):

                        # Determina o limite do prefixo:
                        j = lin - 1;
                        limite = 0;
                        square = self.board.getSquare(j, col);
                        while(square is not None) and (square.isEmpty()):
                            j -= 1;
                            limite += 1;
                            square = self.board.getSquare(j, col);

                        # Chegou em outra palavra:
                        if(square is not None) and (j != lin - 1):
                            limite -= 1; # Da um espaco em branco de distancia.

                        if(limite > -1):
                            anchors.append(("V", self.board.matrix[lin][col], limite));

                # Se a coluna for valida:
                if((col >= 0) and (col < 15)):
                    # Se a posicao a esquerda estiver vazia, marca esta como ancora:
                    if((self.board.matrix[lin][col - 1].isEmpty()) and (self.board.matrix[lin][col].isEmpty() == False)):

                        # Determina o limite do prefixo:
                        j = col - 1;
                        limite = 0;
                        square = self.board.getSquare(lin, j);
                        while(square is not None) and (square.isEmpty()):
                            j -= 1;
                            limite += 1;
                            square = self.board.getSquare(lin, j);

                        # Chegou em outra palavra:
                        if(square is not None) and (j != (col - 1)):
                            limite -= 1; # Da um espaco em branco de distancia.

                        if(limite > -1):
                            anchors.append(("H", self.board.matrix[lin][col], limite));

        return anchors;

    def piecesToChange(self):
        """ Forma um dicionario de pecas para serem trocadas.
            Troca apenas letras que nao sao vogais.
        """
        vogais = ['a', 'e', 'i', 'o', 'u', '#'];
        troca  = {};

        # Se nao tiver feito nenhuma jogada por dois turnos,
        # e nao pedir para trocar de pecas, substitui a mao:
        if (len(troca) == 0) and (self.nPass >= 2):
            for l, pieces in self.hand.items():
                if(self.hand[l].quantity > 0):
                    # Adiciona uma unidade da peca para trocar:
                    troca[l] = 1;
                    # Remove a peca da mao do jogador:
                    self.hand[l].quantity -= 1;

        # Ou troca somente pecas que nao forem vogais:
        else:
            for l, piece in self.hand.items():
                # Se a peca nao for uma vogal marca para ser trocada:
                if(l not in vogais) and (self.hand[l].quantity > 0):
                    troca[l] = 1;
                    self.hand[l].quantity -= 1;

        return troca;

    def reset(self):
        self.anchors  = [];
        self.anchor   = None;
        self.bestMove = None;
        self.playDir  = None;
        self.placedNew   = False;
        self.brancos  = [];

    def debugAnchors(self):
        for anchor in self.anchors:
            print(anchor[0] + ' (', end='');
            print(anchor[1], end='');
            print(' Limit: ' + str(anchor[2]));