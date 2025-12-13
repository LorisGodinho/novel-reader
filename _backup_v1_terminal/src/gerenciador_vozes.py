"""
Gerenciador de Vozes TTS para Novel Reader
Suporta múltiplos modelos de voz locais
"""

import json
import os
from typing import Dict, List, Optional


class GerenciadorVozes:
    def __init__(self, config_path: str = './config/vozes_config.json'):
        """
        Inicializa o gerenciador de vozes.
        
        Args:
            config_path: Caminho para arquivo de configuração
        """
        self.config_path = config_path
        self.config = self._carregar_config()
        self.vozes_disponiveis = self.config.get('vozes_disponiveis', [])
        self.mapeamento_personagens = self.config.get('mapeamento_personagens', {})
    
    def _carregar_config(self) -> Dict:
        """Carrega configurações do arquivo JSON."""
        if os.path.exists(self.config_path):
            with open(self.config_path, 'r', encoding='utf-8') as f:
                return json.load(f)
        return {}
    
    def salvar_config(self):
        """Salva configurações no arquivo JSON."""
        with open(self.config_path, 'w', encoding='utf-8') as f:
            json.dump(self.config, f, ensure_ascii=False, indent=2)
    
    def listar_vozes_sistema(self) -> List[str]:
        """
        Lista todas as vozes TTS disponíveis no sistema.
        
        Returns:
            Lista de nomes de vozes disponíveis
        """
        # TODO: Implementar detecção de vozes do sistema
        # Pode usar: pyttsx3, gTTS, Azure TTS, etc.
        print("Função para listar vozes do sistema a ser implementada")
        print("Opções: pyttsx3, Azure TTS, Google Cloud TTS, Coqui TTS, etc.")
        return []
    
    def adicionar_voz(self, nome: str, tipo: str, modelo: str, **kwargs) -> str:
        """
        Adiciona uma nova voz ao sistema.
        
        Args:
            nome: Nome identificador da voz
            tipo: 'narrador' ou 'personagem'
            modelo: Modelo TTS a ser usado
            **kwargs: Configurações adicionais
            
        Returns:
            ID da voz criada
        """
        voz_id = f"voz_{len(self.vozes_disponiveis) + 1:03d}"
        
        nova_voz = {
            'id': voz_id,
            'nome': nome,
            'tipo': tipo,
            'modelo': modelo,
            **kwargs
        }
        
        self.vozes_disponiveis.append(nova_voz)
        self.config['vozes_disponiveis'] = self.vozes_disponiveis
        self.salvar_config()
        
        return voz_id
    
    def associar_voz_personagem(self, nome_personagem: str, voz_id: str, 
                                configuracoes: Optional[Dict] = None):
        """
        Associa uma voz específica a um personagem.
        
        Args:
            nome_personagem: Nome do personagem
            voz_id: ID da voz a ser associada
            configuracoes: Configurações específicas (velocidade, pitch, etc.)
        """
        if configuracoes is None:
            configuracoes = {'velocidade': 1.0, 'pitch': 1.0}
        
        self.mapeamento_personagens[nome_personagem] = {
            'voz_id': voz_id,
            'configuracoes_especificas': configuracoes
        }
        
        self.config['mapeamento_personagens'] = self.mapeamento_personagens
        self.salvar_config()
        
        print(f"Voz '{voz_id}' associada ao personagem '{nome_personagem}'")
    
    def obter_voz_personagem(self, nome_personagem: str) -> Optional[Dict]:
        """
        Obtém a configuração de voz de um personagem.
        
        Args:
            nome_personagem: Nome do personagem
            
        Returns:
            Dicionário com configurações da voz ou None
        """
        return self.mapeamento_personagens.get(nome_personagem)
    
    def obter_voz_narrador(self) -> Dict:
        """
        Obtém a configuração da voz do narrador padrão.
        
        Returns:
            Dicionário com configurações da voz do narrador
        """
        return self.config.get('voz_narrador_padrao', {})
    
    def definir_voz_narrador(self, modelo: str, idioma: str = 'pt-BR', 
                            velocidade: float = 1.0, pitch: float = 1.0, 
                            volume: float = 1.0):
        """
        Define a voz padrão do narrador.
        
        Args:
            modelo: Modelo TTS a ser usado
            idioma: Idioma da voz
            velocidade: Velocidade da fala
            pitch: Tom da voz
            volume: Volume da voz
        """
        self.config['voz_narrador_padrao'] = {
            'modelo': modelo,
            'idioma': idioma,
            'velocidade': velocidade,
            'pitch': pitch,
            'volume': volume
        }
        self.salvar_config()
        print(f"Voz do narrador definida: {modelo}")


# Exemplo de uso
if __name__ == "__main__":
    gerenciador = GerenciadorVozes()
    
    print("=== Gerenciador de Vozes ===\n")
    print("Comandos disponíveis:")
    print("1. Adicionar voz")
    print("2. Associar voz a personagem")
    print("3. Definir voz do narrador")
    print("4. Listar vozes disponíveis")
