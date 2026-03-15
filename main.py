import webbrowser
import http.server
import socketserver
import threading
import os
import time
from pipeline.extractor import main as run_bronze
from pipeline.silver_transform import transform_silver as run_silver
from pipeline.gold_load import load_gold as run_gold
from pipeline.gold_indicators import load_indicators as run_indicators
from pipeline.validate_results import validate

PORT = 8000

def start_server():
    """Inicia um servidor HTTP simples em uma porta específica."""
    class QuietHandler(http.server.SimpleHTTPRequestHandler):
        def log_message(self, format, *args):
            pass # Silencia logs de requisições no terminal

    handler = QuietHandler
    try:
        # Usamos 127.0.0.1 explicitamente para evitar problemas de bind no Windows/IPv6
        with socketserver.TCPServer(("127.0.0.1", PORT), handler) as httpd:
            print(f"\n[SERVER] Servidor ativo em http://127.0.0.1:{PORT}")
            httpd.serve_forever()
    except OSError:
        print(f"\n[SERVER] Porta {PORT} já está em uso (servidor provavelmente já ativo).")

def run_pipeline():
    print("="*60)
    print("INICIANDO PIPELINE DE DADOS: MEDALLION ARCHITECTURE")
    print("="*60)

    try:
        # Camada Bronze
        print("\n[1/4] Executando Camada Bronze (Extração de Dados)...")
        run_bronze()

        # Camada Silver
        print("\n[2/4] Executando Camada Silver (Transformação e Limpeza)...")
        run_silver()

        # Camada Gold
        print("\n[3/4] Executando Camada Gold (Agregação para Consumo JSON)...")
        run_gold()
        run_indicators()

        # Validação
        print("\n[4/4] Executando Validação de Consistência e Qualidade...")
        validate()

        print("\n" + "="*60)
        print("PIPELINE EXECUTADO COM SUCESSO NA ÍNTEGRA")
        print("="*60)
        
        # Inicia o servidor em uma thread separada para não bloquear
        server_thread = threading.Thread(target=start_server, daemon=True)
        server_thread.start()
        
        # Pequena pausa para garantir que o server subiu antes de abrir o browser
        time.sleep(1)

        # Abre o Dashboard no Navegador
        url = f"http://127.0.0.1:{PORT}/index.html"
        print(f"\nAbrindo Dashboard em: {url}")
        print("Mantenha este terminal aberto para continuar visualizando os dados.")
        webbrowser.open(url)
        
        # Mantém o script vivo enquanto o server estiver rodando (opcional)
        while True:
            time.sleep(10)
        
    except KeyboardInterrupt:
        print("\nEncerrando servidor...")
    except Exception as e:
        print("\n" + "="*60)
        print(f"[ERRO CRÍTICO] O Pipeline foi interrompido na etapa atual.")
        print(f"Detalhe: {e}")
        print("="*60)

if __name__ == "__main__":
    run_pipeline()
