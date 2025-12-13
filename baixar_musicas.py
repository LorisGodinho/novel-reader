"""
Script para baixar músicas do YouTube para o Novel Reader
"""

import yt_dlp
import os

def baixar_musica(url, nome_saida):
    """Baixa música do YouTube e converte para MP3."""
    
    output_path = f'./assets/audio/background/{nome_saida}'
    
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': output_path,
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'mp3',
            'preferredquality': '128',
        }],
        'ffmpeg_location': '.',  # ffmpeg está na raiz do projeto
        'quiet': False,
        'no_warnings': False,
        'download_ranges': lambda info, _: [
            {
                'start_time': 0,
                'end_time': 180,  # 3 minutos = 180 segundos
            }
        ],
    }
    
    try:
        print(f"\n📥 Baixando: {url}")
        print(f"💾 Salvando como: {nome_saida}.mp3")
        
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        
        print(f"✅ Download concluído: {nome_saida}.mp3\n")
        return True
    except Exception as e:
        print(f"❌ Erro ao baixar: {e}\n")
        return False


if __name__ == "__main__":
    print("="*70)
    print(" BAIXANDO MÚSICAS PARA NOVEL READER")
    print("="*70)
    
    # URLs fornecidas
    musicas = [
        {
            'url': 'https://www.youtube.com/watch?v=1xhK_zVZvBU',
            'nome': 'ambient',
            'tipo': 'Ambiente/Normal'
        },
        {
            'url': 'https://youtu.be/xDuCccDiQQM',
            'nome': 'combat',
            'tipo': 'Combate/Ação'
        }
    ]
    
    # Criar pasta se não existir
    os.makedirs('./assets/audio/background', exist_ok=True)
    
    # Baixar cada música
    sucesso = 0
    for musica in musicas:
        print(f"🎵 Tipo: {musica['tipo']}")
        if baixar_musica(musica['url'], musica['nome']):
            sucesso += 1
    
    print("="*70)
    print(f" ✅ {sucesso}/{len(musicas)} músicas baixadas com sucesso!")
    print("="*70)
    
    if sucesso == len(musicas):
        print("\n🎉 Pronto! Agora execute: python novel_reader_gui.py")
    else:
        print("\n⚠️ Algumas músicas falharam. Verifique os erros acima.")
