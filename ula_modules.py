#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Blocos combinacionais de somadores em MyHDL.

Este modulo declara implementacoes de:
- meio somador (half adder),
- somador completo (full adder),
- somador de 2 bits,
- somador generico por encadeamento,
- somador vetorial comportamental.
"""

from myhdl import *


@block
def halfAdder(a, b, soma, carry):
    """Meio somador de 1 bit.

    Args:
        a: Entrada de 1 bit.
        b: Entrada de 1 bit.
        soma: Saida de soma.
        carry: Saida de carry.
    """


    @always_comb
    def comb():
        
        soma.next = a ^ b      
        carry.next = a & b     
            

    return instances()


@block
def fullAdder(a, b, c, soma, carry):
    s = [Signal(bool(0)) for i in range(3)]
    haList = [None for i in range(2)]  # (1)

    haList[0] = halfAdder(a, b, s[0], s[1]) 
    haList[1] = halfAdder(c, s[0], soma, s[2])

    @always_comb
    def comb():
        carry.next = s[1] | s[2]

    return instances()


@block
def adder2bits(x, y, soma, carry):
    """Somador de 2 bits.

    Implementacao esperada com dois full adders, gerando
    uma soma de 2 bits e carry final.

    Args:
        x: Vetor de entrada de 2 bits.
        y: Vetor de entrada de 2 bits.
        soma: Vetor de saida de 2 bits.
        carry: Carry de saida.
    """
    c_int = Signal(bool(0))  # Carry intermediário entre adders
    
    # Primeiro full adder: carry_in = 0
    b1 = fullAdder(x[0], y[0], Signal(bool(0)), soma[0], c_int)
    
    # Segundo full adder: carry_in = c_int (ripple-carry)
    b2 = fullAdder(x[1], y[1], c_int, soma[1], carry)

    return instances()


@block
def adder(x, y, soma, carry):
    """Somador generico para vetores de mesmo tamanho.

    Implementacao esperada por ripple-carry (encadeamento de carries)
    usando celulas de full adder.

    Args:
        x: Vetor de entrada.
        y: Vetor de entrada.
        soma: Vetor de saida com mesma largura de x/y.
        carry: Carry de saida mais significativo.
    """
    n = len(x)
    c = [Signal(bool(0)) for _ in range(n)]  # Carries intermediários
    faList = [None for _ in range(n)]  # Lista de full adders
    
    for i in range(n):
        # Primeiro adder tem carry_in = 0, outros têm carry_in do anterior
        carry_in = Signal(bool(0)) if i == 0 else c[i - 1]
        # Último adder tem carry_out = carry final
        carry_out = carry if i == n - 1 else c[i]
        faList[i] = fullAdder(x[i], y[i], carry_in, soma[i], carry_out)

    return instances()


@block
def addervb(x, y, soma, carry):
    """Somador vetorial em estilo comportamental.

    Versao combinacional que pode usar operacoes aritmeticas diretas
    sobre os vetores para gerar soma e carry.

    Args:
        x: Vetor de entrada.
        y: Vetor de entrada.
        soma: Vetor de saida.
        carry: Carry de saida.
    """
    @always_comb
    def comb():
        result = x + y
        soma.next = result
        carry.next = (result >> len(soma)) & 1

    return instances()
