#!/usr/bin/env python3
"""
Script simplificado para gerenciar BGMs do Novel Reader
Uso: python gerenciar_bgms.py [--verificar|--limpar|--baixar URL --nome NOME]
"""

import sys
import os

# Adicionar diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from utilities.gerenciador_bgm import main

if __name__ == "__main__":
    main()
