import requests
from bs4 import BeautifulSoup
import pandas as pd

def extrair_noticias():
    # URL do site de exemplo (G1 - Economia)
    url = "https://g1.globo.com/economia/"
    
    # Headers para simular um navegador real e evitar bloqueios
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
    }
    
    print(f"Acessando {url}...")
    response = requests.get(url, headers=headers)
    
    if response.status_code != 200:
        print(f"Erro ao acessar o site: Status {response.status_code}")
        return
        
    # Parse do conteúdo HTML
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # Lista para armazenar os dados extraídos
    dados_noticias = []
    
    # Busca todas as chamadas de matérias (padrão comum no G1)
    noticias = soup.find_all('div', class_='feed-post-body')
    
    for noticia in noticias:
        # Extrai o título da notícia
        link_titulo = noticia.find('a', class_='feed-post-link')
        if link_titulo:
            titulo = link_titulo.text.strip()
            link = link_titulo['href']
        else:
            continue
            
        # Extrai o resumo/descrição (se houver)
        resumo_elem = noticia.find('div', class_='feed-post-body-resumo')
        resumo = resumo_elem.text.strip() if resumo_elem else ""
        
        # Adiciona à nossa lista
        dados_noticias.append({
            "Título": titulo,
            "Resumo": resumo,
            "Link": link
        })
    
    # Cria um DataFrame e exporta para CSV
    if dados_noticias:
        df = pd.DataFrame(dados_noticias)
        df.to_csv("noticias_economia.csv", index=False, encoding="utf-8-sig")
        print(f"Sucesso! {len(dados_noticias)} notícias foram salvas em 'noticias_economia.csv'")
    else:
        print("Nenhuma notícia foi encontrada. O layout do site pode ter mudado.")

if __name__ == "__main__":
    extrair_noticias()
