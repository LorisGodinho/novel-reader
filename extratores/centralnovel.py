"""
Extrator específico para Central Novel (centralnovel.com)
Novel: Martial World e outras do site
"""

import requests
from bs4 import BeautifulSoup
import json
import os
import re
import time
from typing import Dict, List, Optional


class ExtratorCentralNovel:
    def __init__(self):
        """Inicializa o extrator para Central Novel."""
        self.url_base = 'https://centralnovel.com'
        self.nome_site = 'centralnovel'
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36'
        })
    
    def extrair_capitulo(self, url_capitulo: str) -> Dict:
        """
        Extrai o conteúdo de um capítulo.
        
        Args:
            url_capitulo: URL do capítulo
            
        Returns:
            Dicionário com dados do capítulo
        """
        print(f"Extraindo: {url_capitulo}")
        
        try:
            response = self.session.get(url_capitulo, timeout=30)
            response.raise_for_status()
        except Exception as e:
            print(f"Erro ao acessar URL: {e}")
            return None
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Extrair informações
        titulo = self._extrair_titulo(soup)
        numero = self._extrair_numero_capitulo(url_capitulo, titulo)
        conteudo = self._extrair_conteudo(soup)
        
        return {
            'numero': numero,
            'titulo': titulo,
            'conteudo': conteudo,
            'url_origem': url_capitulo,
            'site_origem': self.nome_site,
            'data_extracao': time.strftime('%Y-%m-%d')
        }
    
    def _extrair_titulo(self, soup: BeautifulSoup) -> str:
        """Extrai o título do capítulo."""
        # Tenta encontrar o h1 com o título
        titulo_tag = soup.find('h1')
        if titulo_tag:
            return titulo_tag.text.strip()
        return 'Sem título'
    
    def _extrair_conteudo(self, soup: BeautifulSoup) -> List[str]:
        """Extrai o conteúdo do capítulo em parágrafos."""
        paragrafos = []
        
        # O conteúdo geralmente está em divs ou elementos após o título
        # Procura por todos os parágrafos no corpo do texto
        content_area = soup.find('article') or soup.find('div', class_='entry-content') or soup.find('div', class_='post-content')
        
        if content_area:
            # Extrai todos os parágrafos
            for p in content_area.find_all('p'):
                texto = p.get_text(strip=True)
                
                # Filtra parágrafos vazios ou indesejados
                if texto and len(texto) > 10:
                    # Remove links de navegação e doações
                    if not any(palavra in texto.lower() for palavra in [
                        'prev', 'next', 'índice', 'doação', 'contribua',
                        'assinatura vip', 'comentários', 'central novel'
                    ]):
                        paragrafos.append(texto)
        
        return paragrafos
    
    def _extrair_numero_capitulo(self, url: str, titulo: str) -> int:
        """Extrai o número do capítulo da URL ou título."""
        # Tenta extrair da URL primeiro: .../capitulo-961/
        match = re.search(r'capitulo[_-](\d+)', url)
        if match:
            return int(match.group(1))
        
        # Tenta extrair do título: "Capítulo 961"
        match = re.search(r'cap[íi]tulo\s+(\d+)', titulo, re.IGNORECASE)
        if match:
            return int(match.group(1))
        
        return 0
    
    def extrair_novel_info(self, url_novel: str) -> Dict:
        """
        Extrai informações da novel (página principal).
        
        Args:
            url_novel: URL da página principal da novel
            
        Returns:
            Dicionário com informações da novel
        """
        print(f"Extraindo informações da novel: {url_novel}")
        
        response = self.session.get(url_novel, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        titulo = soup.find('h1')
        titulo_texto = titulo.text.strip() if titulo else 'Desconhecido'
        
        return {
            'titulo': titulo_texto,
            'url_original': url_novel,
            'site_origem': self.nome_site,
            'idioma': 'pt-BR'
        }
    
    def extrair_lista_capitulos(self, url_novel: str) -> List[Dict]:
        """
        Extrai a lista de todos os capítulos da novel.
        
        Args:
            url_novel: URL da página principal da novel
            
        Returns:
            Lista de dicionários com informações dos capítulos
        """
        print(f"Extraindo lista de capítulos: {url_novel}")
        
        response = self.session.get(url_novel, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        capitulos = []
        
        # Procura por links de capítulos
        links = soup.find_all('a', href=re.compile(r'capitulo[_-]\d+'))
        
        for link in links:
            url = link.get('href')
            if not url.startswith('http'):
                url = self.url_base + url
            
            titulo = link.text.strip()
            numero = self._extrair_numero_capitulo(url, titulo)
            
            if numero > 0:
                capitulos.append({
                    'numero': numero,
                    'titulo': titulo,
                    'url': url
                })
        
        # Remove duplicatas e ordena
        capitulos_unicos = {cap['numero']: cap for cap in capitulos}
        capitulos = sorted(capitulos_unicos.values(), key=lambda x: x['numero'])
        
        return capitulos
    
    def salvar_capitulo(self, dados_capitulo: Dict, caminho_novel: str):
        """
        Salva o capítulo extraído em arquivo JSON.
        
        Args:
            dados_capitulo: Dados do capítulo
            caminho_novel: Caminho da pasta da novel
        """
        if not dados_capitulo:
            print("Nenhum dado para salvar.")
            return
        
        pasta_capitulos = os.path.join(caminho_novel, 'capitulos')
        os.makedirs(pasta_capitulos, exist_ok=True)
        
        numero = dados_capitulo.get('numero', 0)
        nome_arquivo = f"cap_{numero:04d}.json"
        caminho_arquivo = os.path.join(pasta_capitulos, nome_arquivo)
        
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_capitulo, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Capítulo {numero} salvo: {nome_arquivo}")
    
    def salvar_metadata(self, info_novel: Dict, caminho_novel: str):
        """Salva metadata da novel."""
        os.makedirs(caminho_novel, exist_ok=True)
        
        metadata_path = os.path.join(caminho_novel, 'metadata.json')
        with open(metadata_path, 'w', encoding='utf-8') as f:
            json.dump(info_novel, f, ensure_ascii=False, indent=2)
        
        print(f"✓ Metadata salva em: {metadata_path}")


# Exemplo de uso
if __name__ == "__main__":
    extrator = ExtratorCentralNovel()
    
    print("="*60)
    print(" EXTRATOR SITE DE NOVELS")
    print("="*60)
    print("\nExemplo de uso:")
    print("\n1. Extrair um capítulo:")
    print("   cap = extrator.extrair_capitulo('URL_DO_CAPITULO')")
    print("   extrator.salvar_capitulo(cap, './novels/martial_world')")
    print("\n2. Extrair informações da novel:")
    print("   info = extrator.extrair_novel_info('URL_DA_NOVEL')")
    print("   extrator.salvar_metadata(info, './novels/martial_world')")
    print("\n3. Ver exemplo completo:")
    print("   python extrair_martial_world.py")
    print("="*60)
