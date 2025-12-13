"""
Leitor e Narrador de Novels com TTS
Lê capítulos e narra com vozes diferenciadas
"""

import json
import os
import re
from typing import Dict, List, Optional
from gerenciador_vozes import GerenciadorVozes
from wiki_personagens import WikiPersonagens


class LeitorNovel:
    def __init__(self, caminho_novel: str):
        """
        Inicializa o leitor de novel.
        
        Args:
            caminho_novel: Caminho da pasta da novel
        """
        self.caminho_novel = caminho_novel
        self.metadata = self._carregar_metadata()
        self.gerenciador_vozes = GerenciadorVozes()
        self.wiki = WikiPersonagens(caminho_novel)
        
        # Estado da leitura
        self.capitulo_atual = 0
        self.posicao_atual = 0
    
    def _carregar_metadata(self) -> Dict:
        """Carrega metadados da novel."""
        metadata_path = os.path.join(self.caminho_novel, 'metadata.json')
        if os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def carregar_capitulo(self, numero: int) -> Optional[Dict]:
        """
        Carrega um capítulo específico.
        
        Args:
            numero: Número do capítulo
            
        Returns:
            Dicionário com dados do capítulo ou None
        """
        # Tenta com 3 dígitos primeiro, depois 4
        for formato in [f'cap_{numero:03d}.json', f'cap_{numero:04d}.json']:
            caminho_capitulo = os.path.join(
                self.caminho_novel, 
                'capitulos', 
                formato
            )
            
            if os.path.exists(caminho_capitulo):
                with open(caminho_capitulo, 'r', encoding='utf-8') as f:
                    return json.load(f)
        
        print(f"Capítulo {numero} não encontrado")
        return None
    
    def identificar_dialogos(self, texto: str) -> List[Dict]:
        """
        Identifica diálogos no texto.
        
        Args:
            texto: Texto para análise
            
        Returns:
            Lista de dicionários com diálogos e narrações
        """
        segmentos = []
        
        # Padrões comuns de diálogo
        # Exemplo: "Fala do personagem" disse João
        # Exemplo: — Fala do personagem — disse Maria
        
        # Padrão básico: aspas duplas
        padrao_aspas = r'"([^"]+)"(?:\s+(?:disse|perguntou|gritou|sussurrou)\s+(\w+))?'
        
        # Padrão travessão
        padrao_travessao = r'[—–]\s*([^—–\n]+?)(?:\s+[—–]\s+(?:disse|perguntou|gritou|sussurrou)\s+(\w+))?'
        
        ultima_posicao = 0
        
        # Processa o texto
        for match in re.finditer(padrao_aspas, texto):
            # Adiciona narração antes do diálogo
            if match.start() > ultima_posicao:
                narracao = texto[ultima_posicao:match.start()].strip()
                if narracao:
                    segmentos.append({
                        'tipo': 'narracao',
                        'texto': narracao
                    })
            
            # Adiciona diálogo
            dialogo = match.group(1)
            personagem = match.group(2) if match.group(2) else 'desconhecido'
            
            segmentos.append({
                'tipo': 'dialogo',
                'texto': dialogo,
                'personagem': personagem
            })
            
            ultima_posicao = match.end()
        
        # Adiciona narração final
        if ultima_posicao < len(texto):
            narracao = texto[ultima_posicao:].strip()
            if narracao:
                segmentos.append({
                    'tipo': 'narracao',
                    'texto': narracao
                })
        
        return segmentos
    
    def processar_capitulo(self, numero: int) -> List[Dict]:
        """
        Processa um capítulo completo, separando narrações e diálogos.
        
        Args:
            numero: Número do capítulo
            
        Returns:
            Lista de segmentos com tipo e voz associada
        """
        capitulo = self.carregar_capitulo(numero)
        if not capitulo:
            return []
        
        segmentos_processados = []
        
        for paragrafo in capitulo.get('conteudo', []):
            segmentos = self.identificar_dialogos(paragrafo)
            
            for segmento in segmentos:
                voz_config = None
                
                if segmento['tipo'] == 'narracao':
                    voz_config = self.gerenciador_vozes.obter_voz_narrador()
                else:
                    personagem = segmento['personagem']
                    voz_config = self.gerenciador_vozes.obter_voz_personagem(personagem)
                    
                    # Registra aparição do personagem
                    self.wiki.registrar_aparicao(personagem, numero)
                    
                    # Se não tem voz definida, usa voz do narrador
                    if not voz_config:
                        voz_config = self.gerenciador_vozes.obter_voz_narrador()
                
                segmentos_processados.append({
                    **segmento,
                    'voz_config': voz_config
                })
        
        return segmentos_processados
    
    def narrar_capitulo(self, numero: int):
        """
        Narra um capítulo completo usando TTS.
        
        Args:
            numero: Número do capítulo
        """
        print(f"\n=== Narrando Capítulo {numero} ===\n")
        
        segmentos = self.processar_capitulo(numero)
        
        for i, segmento in enumerate(segmentos, 1):
            tipo = segmento['tipo']
            texto = segmento['texto']
            voz = segmento.get('voz_config', {})
            
            print(f"[{tipo.upper()}]", end=' ')
            if tipo == 'dialogo':
                print(f"({segmento['personagem']})", end=' ')
            print(f": {texto[:50]}...")
            
            # TODO: Implementar síntese de voz real aqui
            # Exemplo: pyttsx3, gTTS, Azure TTS, etc.
            # self._sintetizar_voz(texto, voz)
        
        print(f"\n=== Fim do Capítulo {numero} ===\n")
    
    def _sintetizar_voz(self, texto: str, config_voz: Dict):
        """
        Sintetiza voz para o texto (placeholder).
        
        Args:
            texto: Texto a ser narrado
            config_voz: Configurações da voz
        """
        # TODO: Implementar TTS real
        # Opções: pyttsx3, gTTS, Azure TTS, Coqui TTS
        pass
    
    def listar_capitulos_disponiveis(self) -> List[int]:
        """
        Lista todos os capítulos disponíveis.
        
        Returns:
            Lista de números de capítulos
        """
        pasta_capitulos = os.path.join(self.caminho_novel, 'capitulos')
        if not os.path.exists(pasta_capitulos):
            return []
        
        capitulos = []
        for arquivo in os.listdir(pasta_capitulos):
            if arquivo.startswith('cap_') and arquivo.endswith('.json'):
                # Remove 'cap_' e '.json' e converte para int
                numero_str = arquivo.replace('cap_', '').replace('.json', '')
                numero = int(numero_str)
                capitulos.append(numero)
        
        return sorted(capitulos)


# Exemplo de uso
if __name__ == "__main__":
    print("Leitor de Novels com TTS")
    print("\nPara usar:")
    print("  leitor = LeitorNovel('./novels/minha_novel')")
    print("  leitor.narrar_capitulo(1)")
