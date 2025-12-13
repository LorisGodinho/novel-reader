"""
Engine de Narração Multi-Vozes com Edge TTS
Usa Microsoft Edge TTS com 5 vozes em português
"""

import os
import sys
import tempfile
import time
import asyncio
import edge_tts
import pygame


class EngineNarracao:
    """Engine de narração multi-vozes com Edge TTS."""
    
    # Vozes disponíveis
    VOZES = {
        'Francisca': 'pt-BR-FranciscaNeural',      # Feminino BR
        'Thalita': 'pt-BR-ThalitaMultilingualNeural',  # Feminino BR Multilíngue
        'Antonio': 'pt-BR-AntonioNeural',          # Masculino BR
        'Raquel': 'pt-PT-RaquelNeural',            # Feminino PT
        'Duarte': 'pt-PT-DuarteNeural'             # Masculino PT
    }
    
    def __init__(self, voz_padrao='Francisca'):
        self.temp_dir = tempfile.gettempdir()
        self.voz_atual = self.VOZES.get(voz_padrao, self.VOZES['Francisca'])
        self.mapeamento_personagens = {}
        
        # Inicializar pygame
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
        
        print(f"✓ Engine iniciado com voz: {voz_padrao}")
    
    def trocar_voz(self, nome_voz: str):
        """Troca a voz atual."""
        if nome_voz in self.VOZES:
            self.voz_atual = self.VOZES[nome_voz]
            return True
        return False
    
    def associar_personagem(self, personagem: str, voz: str):
        """Associa um personagem a uma voz."""
        if voz in self.VOZES:
            self.mapeamento_personagens[personagem.lower()] = self.VOZES[voz]
            return True
        return False
    
    async def _gerar_audio_async(self, texto: str, voz: str, velocidade: float):
        """Gera áudio usando Edge TTS (async)."""
        temp_file = os.path.join(self.temp_dir, f'tts_{hash(texto)}.mp3')
        
        # Ajustar taxa de velocidade (Edge TTS usa formato: +XX% ou -XX%)
        rate_pct = int((velocidade - 1.0) * 100)
        rate_str = f"+{rate_pct}%" if rate_pct >= 0 else f"{rate_pct}%"
        
        communicate = edge_tts.Communicate(texto, voz, rate=rate_str)
        await communicate.save(temp_file)
        
        return temp_file
    
    def narrar_segmento(self, texto: str, config_emocao: dict, voz_override: str = None, controlador=None):
        """
        Narra um segmento com emoção específica.
        
        Args:
            texto: Texto limpo (sem tags)
            config_emocao: Configuração da emoção
            voz_override: Voz específica para este segmento (opcional)
            controlador: Controlador de narração (opcional)
        """
        if not texto.strip():
            return
        
        # Pausa antes
        pausa_antes = config_emocao.get('pausa_antes', 0)
        if pausa_antes > 0:
            time.sleep(pausa_antes)
        
        # Escolher voz
        voz = voz_override if voz_override else self.voz_atual
        
        # Configurar velocidade
        velocidade = config_emocao.get('velocidade', 1.0)
        
        # Gerar áudio
        try:
            arquivo = asyncio.run(self._gerar_audio_async(texto, voz, velocidade))
            
            # Reproduzir
            pygame.mixer.music.load(arquivo)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                # Verificar controles
                if controlador:
                    # Pausar
                    if controlador.deve_pausar():
                        pygame.mixer.music.pause()
                        while controlador.deve_pausar():
                            time.sleep(0.1)
                            if controlador.deve_parar() or controlador.deve_avancar() or controlador.deve_retroceder():
                                pygame.mixer.music.stop()
                                break
                        if pygame.mixer.music.get_busy():
                            pygame.mixer.music.unpause()
                    
                    # Pular/Parar
                    if controlador.deve_parar() or controlador.deve_avancar() or controlador.deve_retroceder():
                        pygame.mixer.music.stop()
                        break
                
                pygame.time.Clock().tick(10)
            
            # Limpar
            try:
                os.remove(arquivo)
            except:
                pass
        
        except Exception as e:
            print(f"   ⚠️ Erro: {e}")
        
        # Pausa depois
        pausa_depois = config_emocao.get('pausa_depois', 0.05)
        if pausa_depois > 0:
            time.sleep(pausa_depois)
    
    def finalizar(self):
        """Libera recursos."""
        try:
            pygame.mixer.quit()
        except:
            pass
