"""
Script para extrair Martial World do site de novels
Uso: python extrair_martial_world.py [numero_capitulo_inicial] [numero_capitulo_final]
"""

import os
import sys
import time

# Adiciona o diretório extratores ao path
sys.path.insert(0, os.path.dirname(__file__))

from extratores.centralnovel import ExtratorCentralNovel


def extrair_capitulo_unico(numero: int):
    """Extrai um único capítulo."""
    extrator = ExtratorCentralNovel()
    
    # URL do capítulo
    url = f'https://centralnovel.com/martial-world-capitulo-{numero}/'
    
    print(f"\n{'='*60}")
    print(f" EXTRAINDO CAPÍTULO {numero}")
    print(f"{'='*60}\n")
    
    # Extrair
    capitulo = extrator.extrair_capitulo(url)
    
    if capitulo and capitulo['conteudo']:
        # Salvar
        caminho_novel = './novels/martial_world'
        extrator.salvar_capitulo(capitulo, caminho_novel)
        
        print(f"\n✅ Capítulo {numero} extraído com sucesso!")
        print(f"   Título: {capitulo['titulo']}")
        print(f"   Parágrafos: {len(capitulo['conteudo'])}")
        return True
    else:
        print(f"\n❌ Falha ao extrair capítulo {numero}")
        return False


def extrair_range_capitulos(inicio: int, fim: int, delay: int = 3):
    """
    Extrai um intervalo de capítulos.
    
    Args:
        inicio: Número do primeiro capítulo
        fim: Número do último capítulo (inclusivo)
        delay: Segundos de espera entre requisições
    """
    extrator = ExtratorCentralNovel()
    caminho_novel = './novels/martial_world'
    
    print(f"\n{'='*60}")
    print(f" EXTRAINDO MARTIAL WORLD")
    print(f" Capítulos {inicio} a {fim}")
    print(f"{'='*60}\n")
    
    # Criar metadata se não existir
    metadata_path = os.path.join(caminho_novel, 'metadata.json')
    if not os.path.exists(metadata_path):
        metadata = {
            'titulo': 'Martial World',
            'autor': 'Desconhecido',
            'site_origem': 'centralnovel.com',
            'url_original': 'https://centralnovel.com/series/martial-world-20230928/',
            'idioma': 'pt-BR',
            'generos': ['Ação', 'Aventura', 'Fantasia', 'Artes Marciais'],
            'status': 'Em extração'
        }
        extrator.salvar_metadata(metadata, caminho_novel)
    
    sucessos = 0
    falhas = 0
    
    for numero in range(inicio, fim + 1):
        url = f'https://centralnovel.com/martial-world-capitulo-{numero}/'
        
        print(f"\n[{numero - inicio + 1}/{fim - inicio + 1}] Capítulo {numero}...")
        
        try:
            capitulo = extrator.extrair_capitulo(url)
            
            if capitulo and capitulo['conteudo']:
                extrator.salvar_capitulo(capitulo, caminho_novel)
                sucessos += 1
                print(f"   ✓ Extraído ({len(capitulo['conteudo'])} parágrafos)")
            else:
                falhas += 1
                print(f"   ✗ Sem conteúdo")
        
        except Exception as e:
            falhas += 1
            print(f"   ✗ Erro: {e}")
        
        # Aguarda antes da próxima requisição
        if numero < fim:
            print(f"   Aguardando {delay}s...")
            time.sleep(delay)
    
    print(f"\n{'='*60}")
    print(f" EXTRAÇÃO CONCLUÍDA")
    print(f"{'='*60}")
    print(f"\n✅ Sucessos: {sucessos}")
    print(f"❌ Falhas: {falhas}")
    print(f"📂 Salvos em: {caminho_novel}/capitulos/")
    print(f"{'='*60}\n")


def menu_interativo():
    """Menu interativo para extração."""
    while True:
        print("\n" + "="*60)
        print(" EXTRATOR MARTIAL WORLD - CENTRAL NOVEL")
        print("="*60)
        print("\n1. Extrair capítulo único")
        print("2. Extrair intervalo de capítulos")
        print("3. Extrair capítulo de teste (961)")
        print("4. Sair")
        print("\n" + "-"*60)
        
        escolha = input("\nEscolha uma opção: ").strip()
        
        if escolha == '1':
            try:
                numero = int(input("Número do capítulo: ").strip())
                extrair_capitulo_unico(numero)
            except ValueError:
                print("❌ Número inválido.")
        
        elif escolha == '2':
            try:
                inicio = int(input("Capítulo inicial: ").strip())
                fim = int(input("Capítulo final: ").strip())
                delay = int(input("Delay entre requisições (segundos, recomendado 3): ").strip() or "3")
                
                confirmar = input(f"\nExtrair capítulos {inicio} a {fim}? (s/n): ").strip().lower()
                if confirmar == 's':
                    extrair_range_capitulos(inicio, fim, delay)
            except ValueError:
                print("❌ Entrada inválida.")
        
        elif escolha == '3':
            extrair_capitulo_unico(961)
        
        elif escolha == '4':
            print("\n👋 Até logo!")
            break
        
        else:
            print("❌ Opção inválida.")


if __name__ == "__main__":
    if len(sys.argv) == 2:
        # Um argumento: capítulo único
        try:
            numero = int(sys.argv[1])
            extrair_capitulo_unico(numero)
        except ValueError:
            print("❌ Uso: python extrair_martial_world.py [numero_capitulo]")
    
    elif len(sys.argv) == 3:
        # Dois argumentos: range de capítulos
        try:
            inicio = int(sys.argv[1])
            fim = int(sys.argv[2])
            extrair_range_capitulos(inicio, fim)
        except ValueError:
            print("❌ Uso: python extrair_martial_world.py [inicio] [fim]")
    
    else:
        # Sem argumentos: menu interativo
        menu_interativo()
