import pathlib, datetime

OUT_DIR = pathlib.Path("keylog_lab")
LOG = OUT_DIR / "keylog_simulated.txt"

def run():
    OUT_DIR.mkdir(exist_ok=True)
    print("== Keylogger SIMULADO ==")
    print("Tudo que você digitar aqui será salvo em keylog_lab/keylog_simulated.txt")
    print("Digite /sair para encerrar.\n")
    with LOG.open("a", encoding="utf-8") as fp:
        while True:
            line = input("> ")
            if line.strip().lower() == "/sair":
                print("Encerrando simulação.")
                break
            ts = datetime.datetime.now().isoformat(timespec="seconds")
            fp.write(f"[{ts}] {line}\n")
    print("[OK] Log salvo em", LOG)

if __name__ == "__main__":
    run()
