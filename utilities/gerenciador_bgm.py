"""
Utilitários para gerenciamento de BGMs do Novel Reader
Consolidação de todas as funções de download, processamento e verificação
"""

import yt_dlp
import subprocess
import os
from pathlib import Path
from typing import Optional, Tuple


class GerenciadorBGM:
    """Gerencia download, processamento e verificação de BGMs"""
    
    def __init__(self, bgm_dir: str = "assets/audio/background"):
        self.bgm_dir = Path(bgm_dir)
        self.bgm_dir.mkdir(parents=True, exist_ok=True)
        self.ffmpeg_cmd = self._encontrar_ffmpeg()
    
    def _encontrar_ffmpeg(self) -> str:
        """Encontra executável do ffmpeg"""
        # Primeiro tenta no diretório atual
        if os.path.exists("ffmpeg.exe"):
            return "ffmpeg.exe"
        # Depois tenta no PATH do sistema
        return "ffmpeg"
    
    def baixar_e_processar(
        self,
        url: str,
        nome: str,
        start: int = 0,
        duration: int = 180,
        tipo: str = "leitura"
    ) -> bool:
        """
        Baixa e processa uma BGM do YouTube
        
        Args:
            url: URL do YouTube
            nome: Nome do arquivo de saída (sem extensão)
            start: Tempo inicial em segundos
            duration: Duração em segundos
            tipo: 'leitura' ou 'combate' (afeta processamento)
        
        Returns:
            True se sucesso, False caso contrário
        """
        print(f"\n🎵 Baixando: {nome}")
        print(f"   URL: {url}")
        print(f"   Trecho: {start}s até {start+duration}s")
        print(f"   Tipo: {tipo}")
        
        temp_file = self.bgm_dir / f'temp_{nome}'
        output_file = self.bgm_dir / f'{nome}.mp3'
        
        try:
            # Download com yt-dlp
            ydl_opts = {
                'format': 'bestaudio/best',
                'outtmpl': str(temp_file),
                'quiet': True,
                'no_warnings': True,
                'postprocessors': [{
                    'key': 'FFmpegExtractAudio',
                    'preferredcodec': 'mp3',
                }],
            }
            
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])
            
            # Processar com ffmpeg
            print("   🎚️ Processando com ffmpeg...")
            temp_mp3 = str(temp_file) + '.mp3'
            
            # Filtros de áudio baseados no tipo
            if tipo == "combate":
                audio_filter = (
                    f'loudnorm=I=-18:TP=-1.5:LRA=11,'
                    f'afade=t=in:st=0:d=2,'
                    f'afade=t=out:st={duration-2}:d=2,'
                    f'bass=g=3'  # Aumenta graves para combate
                )
            else:  # leitura
                audio_filter = (
                    f'loudnorm=I=-20:TP=-1.5:LRA=11,'
                    f'afade=t=in:st=0:d=2,'
                    f'afade=t=out:st={duration-2}:d=2,'
                    f'highpass=f=100'  # Remove ruídos graves para leitura
                )
            
            ffmpeg_cmd = [
                self.ffmpeg_cmd, '-i', temp_mp3,
                '-ss', str(start),
                '-t', str(duration),
                '-af', audio_filter,
                '-b:a', '192k',
                '-y',
                str(output_file)
            ]
            
            subprocess.run(ffmpeg_cmd, check=True, capture_output=True)
            
            # Limpar temporários
            if os.path.exists(temp_file):
                os.remove(temp_file)
            if os.path.exists(temp_mp3):
                os.remove(temp_mp3)
            
            size_mb = output_file.stat().st_size / (1024 * 1024)
            print(f"   ✅ Concluído! {nome}.mp3 ({size_mb:.2f} MB)")
            return True
            
        except Exception as e:
            print(f"   ❌ Erro: {e}")
            # Limpar em caso de erro
            for f in [temp_file, str(temp_file) + '.mp3', output_file]:
                if os.path.exists(f):
                    os.remove(f)
            return False
    
    def verificar_bgms(self) -> dict:
        """
        Verifica todas as BGMs presentes e retorna informações
        
        Returns:
            Dict com informações das BGMs
        """
        bgms = {
            'leitura': [],
            'combate': [],
            'total_size_mb': 0
        }
        
        for mp3 in sorted(self.bgm_dir.glob("*.mp3")):
            if mp3.name.startswith("temp_"):
                continue
            
            size_mb = mp3.stat().st_size / (1024 * 1024)
            bgms['total_size_mb'] += size_mb
            
            info = {
                'nome': mp3.name,
                'tamanho_mb': size_mb,
                'caminho': str(mp3)
            }
            
            if "combat" in mp3.name.lower():
                bgms['combate'].append(info)
            else:
                bgms['leitura'].append(info)
        
        return bgms
    
    def limpar_temporarios(self) -> int:
        """
        Remove arquivos temporários
        
        Returns:
            Número de arquivos removidos
        """
        removidos = 0
        for temp in self.bgm_dir.glob("temp_*"):
            temp.unlink()
            print(f"🗑️ Removido: {temp.name}")
            removidos += 1
        return removidos
    
    def exibir_relatorio(self):
        """Exibe relatório completo das BGMs"""
        self.limpar_temporarios()
        
        print("\n" + "="*70)
        print("🎵 RELATÓRIO DE BGMs")
        print("="*70)
        
        bgms = self.verificar_bgms()
        
        if bgms['leitura']:
            print("\n📖 BGMs de Leitura:")
            for bgm in bgms['leitura']:
                print(f"   {bgm['nome']:30} {bgm['tamanho_mb']:6.2f} MB")
        
        if bgms['combate']:
            print("\n⚔️ BGMs de Combate:")
            for bgm in bgms['combate']:
                print(f"   {bgm['nome']:30} {bgm['tamanho_mb']:6.2f} MB")
        
        print(f"\n{'TOTAL':34} {bgms['total_size_mb']:6.2f} MB")
        print("="*70)
        
        total_bgms = len(bgms['leitura']) + len(bgms['combate'])
        print(f"✅ {total_bgms} BGMs encontradas")
        
        return bgms


# Configurações de BGMs recomendadas
BGM_CONFIGS = {
    'leitura': [
        {
            'nome': 'bgm_u_1',
            'url': 'https://www.youtube.com/watch?v=EXEMPLO1',
            'start': 0,
            'duration': 180
        },
        {
            'nome': 'bgm_u_2',
            'url': 'https://www.youtube.com/watch?v=EXEMPLO2',
            'start': 0,
            'duration': 180
        },
        {
            'nome': 'bgm_u_3',
            'url': 'https://www.youtube.com/watch?v=EXEMPLO3',
            'start': 0,
            'duration': 180
        },
    ],
    'combate': [
        {
            'nome': 'combat_battle_1',
            'url': 'https://www.youtube.com/watch?v=EXEMPLO4',
            'start': 0,
            'duration': 180
        },
        {
            'nome': 'combat_battle_2',
            'url': 'https://www.youtube.com/watch?v=EXEMPLO5',
            'start': 0,
            'duration': 180
        },
        {
            'nome': 'combat_battle_3',
            'url': 'https://www.youtube.com/watch?v=EXEMPLO6',
            'start': 0,
            'duration': 180
        },
    ]
}


def main():
    """Função principal para uso via CLI"""
    import argparse
    
    parser = argparse.ArgumentParser(description='Gerenciador de BGMs do Novel Reader')
    parser.add_argument('--verificar', action='store_true', help='Verificar BGMs existentes')
    parser.add_argument('--limpar', action='store_true', help='Limpar arquivos temporários')
    parser.add_argument('--baixar', type=str, help='Baixar BGM (URL)')
    parser.add_argument('--nome', type=str, help='Nome da BGM')
    parser.add_argument('--start', type=int, default=0, help='Tempo inicial (segundos)')
    parser.add_argument('--duration', type=int, default=180, help='Duração (segundos)')
    parser.add_argument('--tipo', type=str, default='leitura', choices=['leitura', 'combate'])
    
    args = parser.parse_args()
    
    gerenciador = GerenciadorBGM()
    
    if args.verificar:
        gerenciador.exibir_relatorio()
    elif args.limpar:
        removidos = gerenciador.limpar_temporarios()
        print(f"✅ {removidos} arquivo(s) temporário(s) removido(s)")
    elif args.baixar:
        if not args.nome:
            print("❌ Erro: --nome é obrigatório para download")
            return
        gerenciador.baixar_e_processar(
            args.baixar,
            args.nome,
            args.start,
            args.duration,
            args.tipo
        )
    else:
        gerenciador.exibir_relatorio()


if __name__ == "__main__":
    main()
