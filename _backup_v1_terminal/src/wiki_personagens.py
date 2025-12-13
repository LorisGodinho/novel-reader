"""
Sistema de Wiki de Personagens
Identifica e mantém registro de personagens das novels
"""

import json
import os
from typing import Dict, List, Optional
import re


class WikiPersonagens:
    def __init__(self, caminho_novel: str):
        """
        Inicializa a wiki para uma novel específica.
        
        Args:
            caminho_novel: Caminho da pasta da novel
        """
        self.caminho_novel = caminho_novel
        self.caminho_personagens = os.path.join(
            caminho_novel.replace('novels', 'personagens')
        )
        os.makedirs(self.caminho_personagens, exist_ok=True)
        
        self.arquivo_wiki = os.path.join(
            self.caminho_personagens, 'personagens.json'
        )
        self.personagens = self._carregar_wiki()
    
    def _carregar_wiki(self) -> Dict:
        """Carrega a wiki de personagens do arquivo."""
        if os.path.exists(self.arquivo_wiki):
            with open(self.arquivo_wiki, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def salvar_wiki(self):
        """Salva a wiki de personagens no arquivo."""
        with open(self.arquivo_wiki, 'w', encoding='utf-8') as f:
            json.dump(self.personagens, f, ensure_ascii=False, indent=2)
    
    def adicionar_personagem(self, nome: str, descricao: str = '', 
                            voz_id: Optional[str] = None, 
                            primeiro_aparecimento: Optional[str] = None):
        """
        Adiciona um novo personagem à wiki.
        
        Args:
            nome: Nome do personagem
            descricao: Descrição do personagem
            voz_id: ID da voz associada
            primeiro_aparecimento: Capítulo de primeira aparição
        """
        if nome in self.personagens:
            print(f"Personagem '{nome}' já existe na wiki")
            return
        
        self.personagens[nome] = {
            'nome': nome,
            'descricao': descricao,
            'voz_id': voz_id,
            'primeiro_aparecimento': primeiro_aparecimento,
            'aparicoes': [],
            'dialogos_exemplo': [],
            'caracteristicas': []
        }
        
        self.salvar_wiki()
        print(f"Personagem '{nome}' adicionado à wiki")
    
    def atualizar_personagem(self, nome: str, **kwargs):
        """
        Atualiza informações de um personagem.
        
        Args:
            nome: Nome do personagem
            **kwargs: Campos a serem atualizados
        """
        if nome not in self.personagens:
            print(f"Personagem '{nome}' não encontrado")
            return
        
        self.personagens[nome].update(kwargs)
        self.salvar_wiki()
        print(f"Personagem '{nome}' atualizado")
    
    def associar_voz(self, nome: str, voz_id: str):
        """
        Associa uma voz a um personagem.
        
        Args:
            nome: Nome do personagem
            voz_id: ID da voz
        """
        if nome not in self.personagens:
            self.adicionar_personagem(nome, voz_id=voz_id)
        else:
            self.personagens[nome]['voz_id'] = voz_id
            self.salvar_wiki()
        
        print(f"Voz '{voz_id}' associada a '{nome}'")
    
    def registrar_aparicao(self, nome: str, numero_capitulo: int):
        """
        Registra aparição de um personagem em um capítulo.
        
        Args:
            nome: Nome do personagem
            numero_capitulo: Número do capítulo
        """
        if nome not in self.personagens:
            self.adicionar_personagem(
                nome, 
                primeiro_aparecimento=f"Capítulo {numero_capitulo}"
            )
        
        if numero_capitulo not in self.personagens[nome]['aparicoes']:
            self.personagens[nome]['aparicoes'].append(numero_capitulo)
            self.salvar_wiki()
    
    def adicionar_dialogo_exemplo(self, nome: str, dialogo: str):
        """
        Adiciona um diálogo de exemplo do personagem.
        
        Args:
            nome: Nome do personagem
            dialogo: Texto do diálogo
        """
        if nome not in self.personagens:
            return
        
        if len(self.personagens[nome]['dialogos_exemplo']) < 5:
            self.personagens[nome]['dialogos_exemplo'].append(dialogo)
            self.salvar_wiki()
    
    def identificar_personagens_texto(self, texto: str) -> List[str]:
        """
        Identifica personagens conhecidos em um texto.
        
        Args:
            texto: Texto para análise
            
        Returns:
            Lista de nomes de personagens encontrados
        """
        personagens_encontrados = []
        
        for nome in self.personagens.keys():
            # Busca pelo nome completo ou variações
            if re.search(rf'\b{re.escape(nome)}\b', texto, re.IGNORECASE):
                personagens_encontrados.append(nome)
        
        return personagens_encontrados
    
    def listar_personagens(self) -> List[str]:
        """
        Lista todos os personagens cadastrados.
        
        Returns:
            Lista de nomes de personagens
        """
        return list(self.personagens.keys())
    
    def obter_info_personagem(self, nome: str) -> Optional[Dict]:
        """
        Obtém informações completas de um personagem.
        
        Args:
            nome: Nome do personagem
            
        Returns:
            Dicionário com informações ou None
        """
        return self.personagens.get(nome)
    
    def exportar_resumo(self) -> str:
        """
        Exporta um resumo da wiki em formato texto.
        
        Returns:
            String com resumo formatado
        """
        resumo = "=== Wiki de Personagens ===\n\n"
        
        for nome, info in self.personagens.items():
            resumo += f"• {nome}\n"
            if info.get('descricao'):
                resumo += f"  Descrição: {info['descricao']}\n"
            if info.get('voz_id'):
                resumo += f"  Voz: {info['voz_id']}\n"
            if info.get('primeiro_aparecimento'):
                resumo += f"  Primeira aparição: {info['primeiro_aparecimento']}\n"
            resumo += f"  Total de aparições: {len(info.get('aparicoes', []))}\n\n"
        
        return resumo


# Exemplo de uso
if __name__ == "__main__":
    print("Sistema de Wiki de Personagens")
    print("Crie uma instância passando o caminho da novel:")
    print("  wiki = WikiPersonagens('./novels/minha_novel')")
