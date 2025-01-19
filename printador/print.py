import os
import time

def capturar_tela(caminho_pasta="capturas"):
    """
    Captura a tela do dispositivo Android conectado via ADB e salva em arquivos sequenciais.
    :param caminho_pasta: Caminho da pasta onde os prints serão salvos.
    """
    # Criar a pasta se não existir
    if not os.path.exists(caminho_pasta):
        os.makedirs(caminho_pasta)

    # Determinar o próximo número do arquivo
    arquivos = os.listdir(caminho_pasta)
    numeros = [
        int(f.replace("imagem", "").replace(".png", "")) 
        for f in arquivos if f.startswith("imagem") and f.endswith(".png")
    ]
    proximo_numero = max(numeros) + 1 if numeros else 1

    # Nome do próximo arquivo
    nome_arquivo = os.path.join(caminho_pasta, f"imagem{proximo_numero}.png")

    # Comando ADB para capturar a tela
    comando = f"adb exec-out screencap -p > {nome_arquivo}"
    os.system(comando)

    print(f"Captura de tela salva como: {nome_arquivo}")

# Função principal para capturar em loop
def main():
    print("Pressione Enter para capturar a tela ou digite 'sair' para finalizar.")
    while True:
        comando = input("Comando: ")
        if comando.lower() == "sair":
            print("Encerrando o programa.")
            break
        capturar_tela()

if __name__ == "__main__":
    main()
