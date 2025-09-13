import json

# Caminho do arquivo de entrada (mapa em texto)
input_file = "mapa.txt"
# Caminho do arquivo de saída (JSON)
output_file = "mapa.json"

with open(input_file, "r", encoding="utf-8") as f:
    linhas = [linha.rstrip('\n') for linha in f]

mapa_json = {
    "width": max(len(l) for l in linhas),
    "height": len(linhas),
    "tiles": linhas
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(mapa_json, f, ensure_ascii=False, indent=4)

print(f"Mapa convertido para {output_file} com sucesso!")