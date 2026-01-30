# Internship Abroad Search Automation

Ce projet automatise la recherche de stages à l'étranger en combinant un serveur MCP personnalisé, Tavily API et des agents IA (Mistral).

## 🛠️ Technologies utilisées
- **n8n** : Orchestration du workflow.
- **MCP (Model Context Protocol)** : Scoring dynamique des villes.
- **Tavily** : Sourcing des offres d'emploi en temps réel.
- **Mistral AI** : Analyse, filtrage et synthèse des offres.
- **Discord** : Notifications finales.

## 🚀 Installation & Lancement

### 1. Prérequis
* **Python 3.11+** (gestion via `uv` recommandée)
* **Node.js** installé (pour `npx`)
* Un compte **Tavily** et un accès **LLM** (Mistral)

### 2. Lancement du Serveur MCP (Python)
Le serveur doit être lancé pour que n8n puisse récupérer les scores des villes via le protocole MCP.

**Option A : Pour le développement et les tests (mode Inspecteur)**
*Note : ça le transport STDIO, donc dans le code il fuat avoir `mcp.run()`*
```bash
npx @modelcontextprotocol/inspector uv run --python 3.11 python ./mcp_server/mcp_server.py
```
**Option B : Pour l'utilisation avec le workflow n8n (mode Production)** 
*Note : ça le transport SSE pour être accessible par n8n, donc dans le code il fuat avoir `mcp.run(transport="streamable-http", mount_path="/mcp")`*
```bash
uv run --python 3.11 python ./mcp_server/mcp_server.py
```
### 3. Lancement de n8n
Ouvrez un nouveau terminal et lancez l'orchestrateur :
```bash
npx n8n
```
## 🛠️ Configuration du Workflow

1. Import : Dans l'interface n8n, importez le fichier `./workflow.json`.

2. Clés API : Renseignez vos clés (Tavily et Mistral) dans les nœuds correspondants.

3. Discord : Collez l'URL de votre Webhook dans le nœud Discord pour recevoir les notifications finales.

## 📊 Résultats
Le workflow génère un fichier CSV (cf. `output/internships_offers.csv`) qui est envoyé sur Discord accompagné d'un message détaillant les top 3 recommendantions et un bilan global sur la recherche (cf. `images/discord_message.png`).