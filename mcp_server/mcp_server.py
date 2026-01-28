from typing import Dict, List, Optional
from mcp.server.fastmcp import FastMCP
import json

# Charger les données
try:
    with open("city_scores.json", "r") as f:
        data = json.load(f)
except FileNotFoundError:
    data = {}
    print("⚠️ Fichier city_scores.json non trouvé. Le serveur démarre avec des données vides.")

# Créer le serveur MCP
mcp = FastMCP(
    name="city-ranker",
    host="0.0.0.0",
    port=8001
)

@mcp.tool()
def find_city_ranking(city: str) -> Dict:
    """
    Retourne le classement Numbeo (Ranking N) d'une ville.
    Attention: 1 est le meilleur score possible (Top 1).
    
    Args:
        city: Le nom de la ville à rechercher
    
    Returns:
        Un dictionnaire contenant la ville, son classement et un message
    """
    city_clean = city.lower().strip()
    rank = data.get(city_clean)
    
    if rank:
        return {
            "city": city,
            "ranking": rank,
            "message": f"La ville de {city} est classée #{rank} au classement Qualité de Vie (N)."
        }
    else:
        return {
            "city": city,
            "ranking": None,
            "message": f"Aucune donnée de classement pour {city}."
        }

@mcp.tool()
def list_cities(limit: int = 10) -> Dict:
    """
    Liste les villes et leur classement (N), triées par meilleur classement.
    
    Args:
        limit: Nombre maximum de villes à retourner (par défaut: 10)
    
    Returns:
        Un dictionnaire contenant le nombre de villes et la liste des villes avec leur classement
    """
    sorted_cities = sorted(data.items(), key=lambda item: item[1])
    subset = sorted_cities[:limit]
    
    cities_list = [
        {"city": city.title(), "ranking": rank}
        for city, rank in subset
    ]
    
    return {
        "count": len(cities_list),
        "cities": cities_list
    }

#def main(): #STDIO pour l'inspection MCP
    #print("🚀 Démarrage du serveur MCP City Ranker...")
    #print(f"📊 {len(data)} villes chargées")
    #print("🔧 Utilisez l'inspecteur MCP pour tester:")
    #print("   npx @modelcontextprotocol/inspector uv run --python 3.11 mcp_server.py")
    #mcp.run()
    
def main(): #pour le workflow n8n
    import sys
    print("🚀 Démarrage du serveur MCP City Ranker...", file=sys.stderr)
    print(f"📊 {len(data)} villes chargées", file=sys.stderr)
    
    # Pour HTTP/StreamableHttp
    mcp.run(transport="streamable-http", mount_path="/mcp")


if __name__ == "__main__":
    main()