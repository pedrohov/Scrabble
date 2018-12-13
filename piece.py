#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Projeto e Analise de Algoritmos (PAA)
# 2o sem/2018 - IFMG - Campus Formiga
# Pedro Henrique Oliveira Veloso (0002346)
# Saulo Ricardo Dias Fernandes   (0021581)

class Piece():
	def __init__(self, letter):
		self.letter   = letter;
		self.quantity = 0;

		data = self.getLetterData(letter);
		self.value = data[0];
		self.max   = data[1];
		
	def getLetterData(self, letter):
		if(letter == '#'):
			return (0, 3);
		elif(letter == 'a'):
			return (1, 14);
		elif(letter == 'e'):
			return (1, 11);
		elif(letter == 'i'):
			return (1, 10);
		elif(letter == 'o'):
			return (1, 10);
		elif(letter == 's'):
			return (1, 8);
		elif(letter == 'u'):
			return (1, 7);
		elif(letter == 'm'):
			return (1, 6);
		elif(letter == 'r'):
			return (1, 6);
		elif(letter == 't'):
			return (1, 5);
		elif(letter == 'd'):
			return (2, 5);
		elif(letter == 'l'):
			return (2, 5);
		elif(letter == 'c'):
			return (2, 4);
		elif(letter == 'p'):
			return (2, 4);
		elif(letter == 'n'):
			return (3, 4);
		elif(letter == 'b'):
			return (3, 3);
		elif(letter == 'ç'):
			return (3, 2);
		elif(letter == 'f'):
			return (4, 2);
		elif(letter == 'g'):
			return (4, 2);
		elif(letter == 'h'):
			return (4, 2);
		elif(letter == 'v'):
			return (4, 2);
		elif(letter == 'j'):
			return (5, 2);
		elif(letter == 'q'):
			return (6, 1);
		elif(letter == 'x'):
			return (8, 1);
		elif(letter == 'z'):
			return (8, 1);
		else:
			return (None, None);

	def __str__(self):
		res = "Letter: " + self.letter + ". Qtd: " + str(self.quantity);
		res = res + ". Value: " + str(self.value) + ". Max: " + str(self.max);
		return res;


if __name__ == "__main__":
	tst = Piece('g');
	print(tst);