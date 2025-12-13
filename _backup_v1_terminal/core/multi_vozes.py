"""
Gerenciador de Vozes Multi-Speaker
Usa Coqui TTS com modelos VITS para múltiplas vozes PT-BR
"""

import os
import json
from TTS.api import TTS
import pygame


class GerenciadorVozesMulti:
    """Gerencia múltiplas vozes para diferentes personagens."""
    
    def __init__(self):
        self.vozes_disponiveis = []
        self.modelo = None
        self.mapeamento_personagens = {}
        self.cache_dir = './cache_vozes'
        
        os.makedirs(self.cache_dir, exist_ok=True)
        
        # Inicializar pygame
        pygame.mixer.init(frequency=22050, size=-16, channels=1, buffer=512)
    
    def listar_modelos_ptbr(self):
        """Lista todos os modelos disponíveis em PT-BR."""
        print("\n🔍 Buscando modelos de voz em português...")
        
        try:
            tts = TTS()
            todos_modelos = tts.list_models()
            
            # Filtrar modelos PT-BR
            modelos_pt = [m for m in todos_modelos if 'pt' in m.lower() or 'portuguese' in m.lower()]
            
            print(f"\n✓ Encontrados {len(modelos_pt)} modelos PT-BR:")
            for i, modelo in enumerate(modelos_pt, 1):
                print(f"  {i}. {modelo}")
            
            return modelos_pt
        
        except Exception as e:
            print(f"❌ Erro ao listar modelos: {e}")
            return []
    
    def carregar_modelo(self, modelo_nome: str = None):
        """
        Carrega um modelo TTS multi-speaker.
        Se não especificado, usa o melhor disponível.
        """
        try:
            if not modelo_nome:
                # Tentar modelos em ordem de prioridade
                modelos_prioridade = [
                    "tts_models/pt/cv/vits",  # Common Voice Portuguese
                    "tts_models/multilingual/multi-dataset/your_tts",  # YourTTS multilíngue
                ]
                
                for modelo in modelos_prioridade:
                    try:
                        print(f"\n📦 Carregando modelo: {modelo}")
                        self.modelo = TTS(modelo_nome=modelo, progress_bar=True)
                        print(f"✓ Modelo carregado!")
                        
                        # Verificar se é multi-speaker
                        if hasattr(self.modelo, 'speakers') and self.modelo.speakers:
                            self.vozes_disponiveis = self.modelo.speakers
                            print(f"🎭 {len(self.vozes_disponiveis)} vozes disponíveis!")
                        else:
                            print("⚠️ Modelo de voz única")
                            self.vozes_disponiveis = ["default"]
                        
                        return True
                    except:
                        continue
                
                print("⚠️ Nenhum modelo PT-BR encontrado, tentando multilíngue...")
                self.modelo = TTS(model_name="tts_models/multilingual/multi-dataset/your_tts")
                self.vozes_disponiveis = self.modelo.speakers if hasattr(self.modelo, 'speakers') else ["default"]
                return True
            
            else:
                self.modelo = TTS(modelo_nome=modelo_nome, progress_bar=True)
                self.vozes_disponiveis = self.modelo.speakers if hasattr(self.modelo, 'speakers') else ["default"]
                return True
        
        except Exception as e:
            print(f"❌ Erro ao carregar modelo: {e}")
            return False
    
    def gerar_audio(self, texto: str, voz_id: str = None, velocidade: float = 1.0, arquivo_saida: str = None):
        """
        Gera áudio com uma voz específica.
        
        Args:
            texto: Texto para narrar
            voz_id: ID da voz (nome do speaker)
            velocidade: Multiplicador de velocidade
            arquivo_saida: Caminho do arquivo de saída
        """
        if not self.modelo:
            print("❌ Modelo não carregado. Use carregar_modelo() primeiro.")
            return None
        
        if not arquivo_saida:
            arquivo_saida = os.path.join(self.cache_dir, f"temp_{hash(texto)}.wav")
        
        try:
            # Gerar áudio
            if voz_id and voz_id in self.vozes_disponiveis:
                self.modelo.tts_to_file(
                    text=texto,
                    speaker=voz_id,
                    file_path=arquivo_saida,
                    speed=velocidade
                )
            else:
                self.modelo.tts_to_file(
                    text=texto,
                    file_path=arquivo_saida,
                    speed=velocidade
                )
            
            return arquivo_saida
        
        except Exception as e:
            print(f"❌ Erro ao gerar áudio: {e}")
            return None
    
    def reproduzir_audio(self, arquivo: str):
        """Reproduz arquivo de áudio."""
        try:
            pygame.mixer.music.load(arquivo)
            pygame.mixer.music.play()
            
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
        
        except Exception as e:
            print(f"❌ Erro ao reproduzir: {e}")
    
    def narrar(self, texto: str, voz_id: str = None, velocidade: float = 1.0):
        """Narra texto diretamente."""
        arquivo = self.gerar_audio(texto, voz_id, velocidade)
        
        if arquivo:
            self.reproduzir_audio(arquivo)
            
            # Limpar arquivo temporário
            try:
                os.remove(arquivo)
            except:
                pass
    
    def associar_personagem_voz(self, personagem: str, voz_id: str):
        """Associa um personagem a uma voz específica."""
        if voz_id in self.vozes_disponiveis:
            self.mapeamento_personagens[personagem] = voz_id
            print(f"✓ {personagem} → {voz_id}")
            return True
        else:
            print(f"❌ Voz {voz_id} não disponível")
            return False
    
    def salvar_mapeamento(self, arquivo: str = "config/mapeamento_vozes.json"):
        """Salva mapeamento de personagens para arquivo."""
        os.makedirs(os.path.dirname(arquivo), exist_ok=True)
        
        with open(arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.mapeamento_personagens, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Mapeamento salvo em {arquivo}")
    
    def carregar_mapeamento(self, arquivo: str = "config/mapeamento_vozes.json"):
        """Carrega mapeamento de personagens."""
        if os.path.exists(arquivo):
            with open(arquivo, encoding='utf-8') as f:
                self.mapeamento_personagens = json.load(f)
            
            print(f"✓ Carregado {len(self.mapeamento_personagens)} mapeamentos")
            return True
        
        return False
    
    def listar_vozes(self):
        """Lista todas as vozes disponíveis."""
        print(f"\n🎭 {len(self.vozes_disponiveis)} vozes disponíveis:\n")
        
        for i, voz in enumerate(self.vozes_disponiveis, 1):
            # Verificar se está mapeada para algum personagem
            personagens = [p for p, v in self.mapeamento_personagens.items() if v == voz]
            
            if personagens:
                print(f"  {i}. {voz} → {', '.join(personagens)}")
            else:
                print(f"  {i}. {voz}")
    
    def finalizar(self):
        """Libera recursos."""
        try:
            pygame.mixer.quit()
        except:
            pass


if __name__ == "__main__":
    # Teste
    gerenciador = GerenciadorVozesMulti()
    
    # Listar modelos
    modelos = gerenciador.listar_modelos_ptbr()
    
    # Carregar modelo
    if gerenciador.carregar_modelo():
        gerenciador.listar_vozes()
        
        # Testar primeira voz
        if gerenciador.vozes_disponiveis:
            print(f"\n🎤 Testando voz: {gerenciador.vozes_disponiveis[0]}")
            gerenciador.narrar(
                "Olá! Esta é uma demonstração do sistema multi-vozes.",
                voz_id=gerenciador.vozes_disponiveis[0]
            )
    
    gerenciador.finalizar()
