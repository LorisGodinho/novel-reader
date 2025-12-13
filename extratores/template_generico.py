"""
Template genérico para extrator de novels.
Adapte este template para cada site específico.
"""

import requests
from bs4 import BeautifulSoup
import json
import os
from typing import Dict, List, Optional


class ExtratorGenerico:
    def __init__(self, url_base: str, nome_site: str):
        """
        Inicializa o extrator.
        
        Args:
            url_base: URL base do site
            nome_site: Nome identificador do site
        """
        self.url_base = url_base
        self.nome_site = nome_site
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
    
    def extrair_capitulo(self, url_capitulo: str) -> Dict:
        """
        Extrai o conteúdo de um capítulo.
        
        Args:
            url_capitulo: URL do capítulo
            
        Returns:
            Dicionário com dados do capítulo
        """
        response = self.session.get(url_capitulo, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # TODO: Adaptar seletores CSS para o site específico
        titulo = self._extrair_titulo(soup)
        conteudo = self._extrair_conteudo(soup)
        numero = self._extrair_numero_capitulo(soup)
        
        return {
            'titulo': titulo,
            'numero': numero,
            'conteudo': conteudo,
            'url_origem': url_capitulo,
            'site_origem': self.nome_site
        }
    
    def _extrair_titulo(self, soup: BeautifulSoup) -> str:
        """Extrai o título do capítulo."""
        # TODO: Implementar seletor específico
        titulo_tag = soup.find('h1')  # Exemplo genérico
        return titulo_tag.text.strip() if titulo_tag else 'Sem título'
    
    def _extrair_conteudo(self, soup: BeautifulSoup) -> List[str]:
        """Extrai o conteúdo do capítulo em parágrafos."""
        # TODO: Implementar seletor específico
        conteudo_div = soup.find('div', class_='conteudo')  # Exemplo genérico
        
        if not conteudo_div:
            return []
        
        paragrafos = []
        for p in conteudo_div.find_all('p'):
            texto = p.text.strip()
            if texto:
                paragrafos.append(texto)
        
        return paragrafos
    
    def _extrair_numero_capitulo(self, soup: BeautifulSoup) -> Optional[int]:
        """Extrai o número do capítulo."""
        # TODO: Implementar lógica específica
        return None
    
    def extrair_lista_capitulos(self, url_novel: str) -> List[Dict]:
        """
        Extrai a lista de todos os capítulos da novel.
        
        Args:
            url_novel: URL da página principal da novel
            
        Returns:
            Lista de dicionários com informações dos capítulos
        """
        response = self.session.get(url_novel, timeout=30)
        response.raise_for_status()
        
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # TODO: Adaptar para o site específico
        capitulos = []
        links = soup.find_all('a', class_='capitulo-link')  # Exemplo genérico
        
        for i, link in enumerate(links, 1):
            capitulos.append({
                'numero': i,
                'titulo': link.text.strip(),
                'url': link.get('href')
            })
        
        return capitulos
    
    def salvar_capitulo(self, dados_capitulo: Dict, caminho_novel: str):
        """
        Salva o capítulo extraído em arquivo JSON.
        
        Args:
            dados_capitulo: Dados do capítulo
            caminho_novel: Caminho da pasta da novel
        """
        pasta_capitulos = os.path.join(caminho_novel, 'capitulos')
        os.makedirs(pasta_capitulos, exist_ok=True)
        
        numero = dados_capitulo.get('numero', 0)
        nome_arquivo = f"cap_{numero:03d}.json"
        caminho_arquivo = os.path.join(pasta_capitulos, nome_arquivo)
        
        with open(caminho_arquivo, 'w', encoding='utf-8') as f:
            json.dump(dados_capitulo, f, ensure_ascii=False, indent=2)
        
        print(f"Capítulo {numero} salvo em: {caminho_arquivo}")


# Exemplo de uso
if __name__ == "__main__":
    print("Este é um template genérico.")
    print("Crie um arquivo específico para cada site que deseja extrair.")
    print("\nExemplo:")
    print("  extrator = ExtratorGenerico('https://site.com', 'nome_site')")
    print("  capitulo = extrator.extrair_capitulo('https://site.com/novel/cap1')")
    print("  extrator.salvar_capitulo(capitulo, './novels/minha_novel')")
