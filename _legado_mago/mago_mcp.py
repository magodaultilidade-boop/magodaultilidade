import json
import os
import subprocess
from mcp.server.fastmcp import FastMCP


# Initialize the MCP Server
mcp = FastMCP("MagoMCP")

# Path to the website's product database
PRODUTOS_PATH = "/var/www/magodaultilidade.com.br/html/produtos.json"

@mcp.resource("magodaultilidade://produtos")
def read_produtos() -> str:
    """Reads the current list of products from the website database (produtos.json)."""
    if not os.path.exists(PRODUTOS_PATH):
        return "[]"
    with open(PRODUTOS_PATH, 'r', encoding='utf-8') as f:
        return f.read()

@mcp.tool()
def add_produto(name: str, regular_price: str, external_url: str, description: str, category: str = "Geral", button_text: str = "Comprar no Mercado Livre") -> str:
    """
    Adds a new product to the Mago da Utilidade website.
    Always use this tool when the user asks to add or insert a new product.
    """
    try:
        if os.path.exists(PRODUTOS_PATH):
            with open(PRODUTOS_PATH, 'r', encoding='utf-8') as f:
                data = json.load(f)
        else:
            data = []
            
        new_prod = {
            "name": name,
            "regular_price": str(regular_price),
            "external_url": external_url,
            "button_text": button_text,
            "categories_names": [category],
            "description": description
        }
        data.append(new_prod)
        
        with open(PRODUTOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        return f"Sucesso! O produto '{name}' foi adicionado ao site Mago da Utilidade."
    except Exception as e:
        return f"Erro ao adicionar produto: {str(e)}"

@mcp.tool()
def delete_produto(name: str) -> str:
    """
    Deletes a product from the Mago da Utilidade website by its exact name.
    Always use this tool when the user asks to remove, delete, or exclude a product.
    """
    try:
        if not os.path.exists(PRODUTOS_PATH):
            return "Erro: Arquivo produtos.json não encontrado."
            
        with open(PRODUTOS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        initial_length = len(data)
        # Filter out the product with the matching name (case-insensitive)
        data = [p for p in data if p.get("name", "").lower() != name.lower()]
        
        if len(data) == initial_length:
            return f"Aviso: O produto '{name}' não foi encontrado no site."
            
        with open(PRODUTOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        return f"Sucesso! O produto '{name}' foi removido do site."
    except Exception as e:
        return f"Erro ao remover produto: {str(e)}"

@mcp.tool()
def publicar_wordpress(application_password: str) -> str:
    """
    Executa o script de publicação automática no WordPress.
    IMPORTANT: Você deve pedir a 'Application Password' (senha de aplicativo) do WordPress para o usuário ANTES de usar esta ferramenta.
    Nunca adivinhe a senha. A senha lida com a conexão segura ao WordPress do usuário.
    """
    script_path = "/var/www/magodaultilidade.com.br/html/publicar-produtos-wordpress.py"
    json_path = "/var/www/magodaultilidade.com.br/html/produtos.json"
    python_bin = "/opt/mcp/venv/bin/python"
    
    if not os.path.exists(script_path):
        return f"Erro: Script não encontrado em {script_path}"
        
    try:
        # Run the script non-interactively
        result = subprocess.run(
            [python_bin, script_path, "--arquivo", json_path, "--senha", application_password],
            capture_output=True,
            text=True,
            timeout=60
        )
        
        output = result.stdout
        if result.stderr:
            output += "\nErros/Avisos:\n" + result.stderr
            
        if result.returncode == 0:
            return f"Sucesso na Publicação!\n{output}"
        else:
            return f"Falha ao publicar (Código {result.returncode}):\n{output}"
            
    except subprocess.TimeoutExpired:
        return "Erro: O processo demorou muito e foi cancelado (timeout)."
    except Exception as e:
        return f"Erro na execução: {str(e)}"

@mcp.tool()
def buscar_produtos(query: str) -> str:
    """
    Busca produtos no Mago da Utilidade pelo nome ou categoria.
    Retorna uma lista formatada de todos os produtos que contêm a palavra-chave pesquisada.
    Use query='todos' para listar absolutamente todos os produtos do site.
    """
    try:
        if not os.path.exists(PRODUTOS_PATH):
            return "Erro: Arquivo produtos.json não encontrado."
            
        with open(PRODUTOS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        if not data:
            return "O catálogo de produtos está vazio."
            
        q = query.lower()
        if q == "todos" or q == "all" or q == "*":
            resultados = data
        else:
            resultados = [
                p for p in data 
                if q in p.get("name", "").lower() or 
                   any(q in c.lower() for c in p.get("categories_names", []))
            ]
            
        if not resultados:
            return f"Nenhum produto encontrado para a busca '{query}'."
            
        resposta = f"Encontrados {len(resultados)} produto(s):\n"
        for p in resultados:
            categorias = ", ".join(p.get("categories_names", []))
            resposta += f"- {p.get('name')} | Preço: R$ {p.get('regular_price')} | Categoria: {categorias}\n"
            
        return resposta
    except Exception as e:
        return f"Erro ao buscar produtos: {str(e)}"

@mcp.tool()
def editar_produto(name: str, novo_preco: str = None, nova_url: str = None, nova_descricao: str = None, nova_categoria: str = None) -> str:
    """
    Edita um produto existente no Mago da Utilidade buscando pelo nome (não sensível a maiúsculas).
    Você só precisa enviar os campos que deseja alterar (novo_preco, nova_url, nova_descricao, nova_categoria). 
    Os campos não enviados (ex. deixados como None) permanecerão com seu valor antigo original.
    """
    try:
        if not os.path.exists(PRODUTOS_PATH):
            return "Erro: Arquivo produtos.json não encontrado."
            
        with open(PRODUTOS_PATH, 'r', encoding='utf-8') as f:
            data = json.load(f)
            
        produto_encontrado = False
        for p in data:
            if p.get("name", "").lower() == name.lower():
                produto_encontrado = True
                if novo_preco is not None:
                    p["regular_price"] = str(novo_preco)
                if nova_url is not None:
                    p["external_url"] = nova_url
                if nova_descricao is not None:
                    p["description"] = nova_descricao
                if nova_categoria is not None:
                    p["categories_names"] = [nova_categoria]
                break
                
        if not produto_encontrado:
            return f"Aviso: Produto '{name}' não encontrado para edição."
            
        with open(PRODUTOS_PATH, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=4, ensure_ascii=False)
            
        return f"Sucesso! O produto '{name}' teve os dados atualizados com sucesso."
    except Exception as e:
        return f"Erro ao editar produto: {str(e)}"

if __name__ == "__main__":
    # Starts the server using stdio transport (standard for Claude Desktop over SSH)
    mcp.run()




