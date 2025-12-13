"""
Sistema de Emoções Customizado - 100% Gratuito
Manipula texto e áudio para criar efeitos emocionais realistas
"""

import re
from typing import Dict, List, Tuple


class ProcessadorEmocoes:
    """Processa tags de emoção e aplica transformações no texto e áudio."""
    
    # Configurações de emoções
    EMOCOES = {
        'normal': {
            'velocidade': 1.0,
            'volume': 0,
            'pausa_antes': 0.0,
            'pausa_depois': 0.0
        },
        'sussurro': {
            'velocidade': 1.0,
            'volume': -10,  # dB
            'pausa_antes': 0.0,
            'pausa_depois': 0.0
        },
        'grito': {
            'velocidade': 1.0,
            'volume': 5,
            'pausa_antes': 0.0,
            'pausa_depois': 0.0
        },
        'riso': {
            'insercao': 'ha ha ha',
            'velocidade': 1.0,
            'volume': 2,
            'pausa_antes': 0.0,
            'pausa_depois': 0.0
        },
        'brincalhao': {
            'velocidade': 1.0,
            'volume': 1,
            'pausa_antes': 0.0,
            'pausa_depois': 0.0
        },
        'misterioso': {
            'velocidade': 1.0,
            'volume': -5,
            'pausa_antes': 0.0,
            'pausa_depois': 0.0
        },
        'animado': {
            'velocidade': 1.0,
            'volume': 3,
            'pausa_antes': 0.0,
            'pausa_depois': 0.0
        },
        'triste': {
            'velocidade': 1.0,
            'volume': -3,
            'pausa_antes': 0.0,
            'pausa_depois': 0.0
        },
        'raiva': {
            'velocidade': 1.0,
            'volume': 6,
            'pausa_antes': 0.0,
            'pausa_depois': 0.0
        },
        'suspiro': {
            'insercao': 'ahhh',
            'velocidade': 1.0,
            'volume': -5,
            'pausa_antes': 0.0,
            'pausa_depois': 0.0
        }
    }
    
    # Mapeamento de tags para emoções
    TAGS_MAPEAMENTO = {
        'whispers': 'sussurro',
        'sussurro': 'sussurro',
        'murmurou': 'sussurro',
        'shouting': 'grito',
        'grito': 'grito',
        'gritando': 'grito',
        'gritou': 'grito',
        'berrou': 'grito',
        'giggles': 'riso',
        'rindo': 'riso',
        'riu': 'riso',
        'risada': 'riso',
        'brincalhao': 'brincalhao',
        'provocador': 'brincalhao',
        'mysterious': 'misterioso',
        'misterioso': 'misterioso',
        'excited': 'animado',
        'animado': 'animado',
        'sadly': 'triste',
        'triste': 'triste',
        'angrily': 'raiva',
        'raiva': 'raiva',
        'sighs': 'suspiro',
        'suspiro': 'suspiro'
    }
    
    def __init__(self):
        self.padrao_tags = re.compile(r'\[([^\]]+)\]')
    
    def extrair_segmentos(self, texto: str) -> List[Dict]:
        """
        Extrai segmentos de texto com suas emoções.
        
        Returns:
            Lista de dicionários: [{'emocao': str, 'texto': str, 'original': str}]
        """
        segmentos = []
        ultima_pos = 0
        emocao_atual = 'normal'
        
        for match in self.padrao_tags.finditer(texto):
            tag = match.group(1).lower().strip()
            pos_inicio = match.start()
            pos_fim = match.end()
            
            # Atualiza emoção para o próximo segmento
            emocao_atual = self.TAGS_MAPEAMENTO.get(tag, 'normal')
            ultima_pos = pos_fim
        
        # Adiciona texto final (se houver)
        if ultima_pos < len(texto):
            texto_final = texto[ultima_pos:].strip()
            if texto_final:
                segmentos.append({
                    'emocao': emocao_atual,
                    'texto': texto_final,
                    'original': texto_final
                })
        
        # Se não houver segmentos, retorna texto completo como normal
        if not segmentos:
            segmentos.append({
                'emocao': 'normal',
                'texto': texto.strip(),
                'original': texto.strip()
            })
        
        return segmentos
    
    def processar_texto(self, texto: str, emocao: str) -> str:
        """
        Processa o texto para uma emoção específica.
        Remove tags e aplica transformações.
        """
        # Remove todas as tags
        texto_limpo = self.padrao_tags.sub('', texto).strip()
        
        if not texto_limpo:
            return ''
        
        config = self.EMOCOES.get(emocao, self.EMOCOES['normal'])
        
        # Inserção de sons (riso, suspiro)
        if 'insercao' in config:
            texto_limpo = f"{config['insercao']}... {texto_limpo}"
        
        return texto_limpo
    
    def _silabificar(self, texto: str, separador: str = '-') -> str:
        """
        Separa palavras por sílabas para efeito brincalhão.
        Exemplo: "não" -> "nã-ão", "faça" -> "fa-ça"
        """
        # Simplificado: adiciona separador entre vogais e consoantes
        resultado = []
        
        for palavra in texto.split():
            if len(palavra) <= 2:
                resultado.append(palavra)
                continue
            
            # Adiciona separadores em posições estratégicas
            palavra_sep = ''
            for i, char in enumerate(palavra):
                palavra_sep += char
                if i < len(palavra) - 1:
                    # Adiciona separador entre consoante-vogal ou vogal-consoante
                    if self._e_vogal(char) != self._e_vogal(palavra[i + 1]):
                        palavra_sep += separador
            
            resultado.append(palavra_sep)
        
        return ' '.join(resultado)
    
    def _e_vogal(self, char: str) -> bool:
        """Verifica se é vogal."""
        return char.lower() in 'aeiouáéíóúâêîôûãõ'
    
    def detectar_climax(self, texto: str) -> bool:
        """
        Detecta se o texto é um momento de clímax.
        Baseado em pontuação, palavras-chave e contexto.
        """
        texto_lower = texto.lower()
        
        # Múltiplas exclamações
        if texto.count('!') >= 2:
            return True
        
        # Palavras de ação intensa
        palavras_climax = [
            'explodiu', 'destruiu', 'rasgou', 'matou', 'morreu',
            'gritou', 'berrou', 'rugiu', 'atacou', 'golpeou',
            'sangue', 'morte', 'poder', 'energia', 'batalha'
        ]
        
        if any(palavra in texto_lower for palavra in palavras_climax):
            return True
        
        # Frases entre aspas com exclamação (diálogos emocionais)
        if '"' in texto and '!' in texto:
            return True
        
        return False
    
    def obter_config_emocao(self, emocao: str) -> Dict:
        """Retorna configuração de uma emoção."""
        return self.EMOCOES.get(emocao, self.EMOCOES['normal'])
    
    def detectar_emocao_contextual(self, texto: str) -> str:
        """
        Detecta emoção baseada no contexto do texto.
        Usado quando não há tags explícitas.
        """
        texto_lower = texto.lower()
        
        # Sussurro
        if any(palavra in texto_lower for palavra in ['sussurrou', 'murmurou', 'silêncio']):
            return 'sussurro'
        
        # Grito
        if any(palavra in texto_lower for palavra in ['gritou', 'berrou', 'rugiu']):
            return 'grito'
        
        # Riso
        if any(palavra in texto_lower for palavra in ['riu', 'risada', 'sorriu', 'gargalh']):
            return 'riso'
        
        # Raiva
        if any(palavra in texto_lower for palavra in ['furioso', 'raiva', 'ódio', 'irritado']):
            return 'raiva'
        
        # Tristeza
        if any(palavra in texto_lower for palavra in ['chorou', 'lágrimas', 'tristeza', 'sofr']):
            return 'triste'
        
        # Mistério
        if any(palavra in texto_lower for palavra in ['mistério', 'sombra', 'escuro', 'oculto']):
            return 'misterioso'
        
        # Animação
        if '!' in texto and len(texto) < 100:
            return 'animado'
        
        return 'normal'
