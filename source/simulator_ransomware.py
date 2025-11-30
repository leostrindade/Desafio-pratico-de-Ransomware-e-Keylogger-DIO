import base64, os, time, pathlib, argparse

LAB_DIR = pathlib.Path("lab_data")
NOTE = LAB_DIR / "RANSOM_NOTE.txt"
HEADER = b"SIM_LOCK_v1\n"  # marcador didático

def ensure_lab():
    LAB_DIR.mkdir(exist_ok=True)
    # cria arquivos apenas se a pasta estiver vazia
    if not any(LAB_DIR.iterdir()):
        samples = {
            "relatorio.txt": "Relatório interno – amostra\nConfidencial? Não. Uso didático.\n",
            "dados.csv": "id,nome,score\n1,Ana,83\n2,Bruno,91\n",
            "anotacoes.md": "# Notebook de testes\n- item 1\n- item 2\n",
        }
        for name, content in samples.items():
            (LAB_DIR / name).write_text(content, encoding="utf-8")
def lock():
    ensure_lab()
    for p in LAB_DIR.iterdir():
        if p.is_file() and p.suffix != ".locked" and p.name != NOTE.name:
            raw = p.read_bytes()
            encoded = base64.b64encode(HEADER + raw)
            locked_path = p.with_suffix(p.suffix + ".locked")
            locked_path.write_bytes(encoded)
            p.unlink()
    NOTE.write_text(
        "SEUS ARQUIVOS DE TESTE FORAM 'SIMULADOS'!\n"
        "Este é um exercício DIDÁTICO. Nada real foi criptografado.\n"
        "Para reverter, rode: python src/simulator_ransomware.py --unlock\n",
        encoding="utf-8"
    )
    print("[OK] Simulação de lock concluída em", LAB_DIR)

def unlock():
    if not LAB_DIR.exists():
        print("Nada a reverter.")
        return
    for p in LAB_DIR.glob("*.locked"):
        data = base64.b64decode(p.read_bytes())
        if not data.startswith(HEADER):
            print(f"[!] {p.name} não tem cabeçalho esperado; ignorando.")
            continue
        original = data[len(HEADER):]
        # remove apenas a extensão final .locked
        dest = p.with_suffix(p.suffix.replace(".locked", ""))
        dest.write_bytes(original)
        p.unlink()
    if NOTE.exists():
        NOTE.unlink()
    print("[OK] Simulação de unlock concluída em", LAB_DIR)

if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--unlock", action="store_true", help="Reverte o lock didático")
    args = ap.parse_args()
    if args.unlock:
        unlock()
    else:
        lock()
