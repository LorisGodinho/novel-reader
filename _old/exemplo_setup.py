"""
Script de exemplo demonstrando o fluxo completo do Novel Reader
"""

import os
import sys

# Adiciona o diretório src ao path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from gerenciador_vozes import GerenciadorVozes
from wiki_personagens import WikiPersonagens
import json


def exemplo_completo():
    """Demonstração do fluxo completo do sistema."""
    
    print("="*60)
    print(" EXEMPLO DE USO - NOVEL READER")
    print("="*60)
    
    # 1. Configurar Gerenciador de Vozes
    print("\n[1] Configurando vozes...")
    gv = GerenciadorVozes()
    
    # Definir voz do narrador (Maria - Português Brasil)
    gv.definir_voz_narrador(
        modelo='HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_PT-BR_MARIA_11.0',
        idioma='pt-BR',
        velocidade=1.0,
        pitch=1.0
    )
    print("✓ Voz do narrador configurada: Microsoft Maria Desktop")
    
    # 2. Adicionar vozes para personagens
    print("\n[2] Adicionando vozes de personagens...")
    
    # Voz para protagonista masculino (usando Zira como exemplo)
    voz_protagonista = gv.adicionar_voz(
        nome='Protagonista Masculino',
        tipo='personagem',
        modelo='HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_EN-US_ZIRA_11.0',
        velocidade=0.9,  # Um pouco mais lento
        pitch=0.9  # Tom um pouco mais grave
    )
    print(f"✓ Voz do protagonista criada: {voz_protagonista}")
    
    # Voz para personagem feminino
    voz_heroina = gv.adicionar_voz(
        nome='Heroína',
        tipo='personagem',
        modelo='HKEY_LOCAL_MACHINE\\SOFTWARE\\Microsoft\\Speech\\Voices\\Tokens\\TTS_MS_PT-BR_MARIA_11.0',
        velocidade=1.1,  # Um pouco mais rápido
        pitch=1.2  # Tom mais agudo
    )
    print(f"✓ Voz da heroína criada: {voz_heroina}")
    
    # 3. Criar uma novel de exemplo
    print("\n[3] Criando estrutura de novel de exemplo...")
    
    caminho_novel = './novels/exemplo_novel'
    os.makedirs(caminho_novel, exist_ok=True)
    os.makedirs(os.path.join(caminho_novel, 'capitulos'), exist_ok=True)
    
    # Criar metadata
    metadata = {
        'titulo': 'A Jornada do Herói',
        'autor': 'Autor Exemplo',
        'site_origem': 'exemplo.com',
        'url_original': 'https://exemplo.com/novel/123',
        'idioma': 'pt-BR',
        'generos': ['Fantasia', 'Aventura'],
        'status': 'Exemplo',
        'total_capitulos': 1
    }
    
    with open(os.path.join(caminho_novel, 'metadata.json'), 'w', encoding='utf-8') as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)
    
    print(f"✓ Novel criada em: {caminho_novel}")
    
    # 4. Criar capítulo de exemplo
    print("\n[4] Criando capítulo de exemplo...")
    
    capitulo_exemplo = {
        'numero': 1,
        'titulo': 'O Despertar',
        'conteudo': [
            'Era uma manhã fria quando João acordou. Ele olhou pela janela e viu o céu nublado.',
            '"Que estranho," pensou João, "nunca vi o céu assim."',
            'Maria entrou no quarto e disse: "Bom dia, João! Você precisa ver isso!"',
            '"O que aconteceu?" perguntou João, preocupado.',
            'Maria respondeu: "A cidade está diferente. Tudo mudou durante a noite."',
            'João se levantou rapidamente. Ele sabia que algo grande estava prestes a acontecer.',
            '"Vamos investigar," disse João com determinação.'
        ],
        'url_origem': 'https://exemplo.com/novel/cap1',
        'site_origem': 'exemplo.com',
        'data_extracao': '2025-12-12'
    }
    
    with open(os.path.join(caminho_novel, 'capitulos', 'cap_001.json'), 'w', encoding='utf-8') as f:
        json.dump(capitulo_exemplo, f, ensure_ascii=False, indent=2)
    
    print("✓ Capítulo 1 criado com conteúdo de exemplo")
    
    # 5. Configurar Wiki de Personagens
    print("\n[5] Configurando wiki de personagens...")
    
    wiki = WikiPersonagens(caminho_novel)
    
    wiki.adicionar_personagem(
        nome='João',
        descricao='Protagonista masculino, corajoso e determinado',
        primeiro_aparecimento='Capítulo 1'
    )
    
    wiki.adicionar_personagem(
        nome='Maria',
        descricao='Heroína, inteligente e observadora',
        primeiro_aparecimento='Capítulo 1'
    )
    
    # Associar vozes aos personagens
    wiki.associar_voz('João', voz_protagonista)
    wiki.associar_voz('Maria', voz_heroina)
    
    # Associar no gerenciador também
    gv.associar_voz_personagem('João', voz_protagonista)
    gv.associar_voz_personagem('Maria', voz_heroina)
    
    print("✓ Personagens João e Maria adicionados à wiki")
    print("✓ Vozes associadas aos personagens")
    
    # 6. Resumo
    print("\n" + "="*60)
    print(" CONFIGURAÇÃO COMPLETA!")
    print("="*60)
    print(f"\n📚 Novel: {metadata['titulo']}")
    print(f"📖 Capítulos disponíveis: 1")
    print(f"👥 Personagens cadastrados: 2 (João, Maria)")
    print(f"🎤 Vozes configuradas:")
    print(f"   • Narrador: Microsoft Maria Desktop")
    print(f"   • João: {voz_protagonista}")
    print(f"   • Maria: {voz_heroina}")
    
    print("\n" + "="*60)
    print(" PRÓXIMOS PASSOS")
    print("="*60)
    print("\n1. Para narrar o capítulo de exemplo:")
    print("   python exemplo_narrar.py")
    print("\n2. Para extrair uma novel real:")
    print("   • Forneça o HTML do site")
    print("   • Crie um extrator específico")
    print("   • Execute a extração")
    print("\n3. Para adicionar mais vozes:")
    print("   • Baixe vozes PT-BR do Windows")
    print("   • Ou use gTTS/Azure TTS")
    print("="*60)


if __name__ == "__main__":
    try:
        exemplo_completo()
        print("\n✅ Exemplo executado com sucesso!")
    except Exception as e:
        print(f"\n❌ Erro: {e}")
        import traceback
        traceback.print_exc()
