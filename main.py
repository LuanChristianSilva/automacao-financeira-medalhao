from pipeline.extractor import main as run_bronze
from pipeline.silver_transform import transform_silver as run_silver
from pipeline.gold_load import load_gold as run_gold
from pipeline.validate_results import validate

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

        # Validação
        print("\n[4/4] Executando Validação de Consistência e Qualidade...")
        validate()

        print("\n" + "="*60)
        print("PIPELINE EXECUTADO COM SUCESSO NA ÍNTEGRA")
        print("="*60)
        
    except Exception as e:
        print("\n" + "="*60)
        print(f"[ERRO CRÍTICO] O Pipeline foi interrompido na etapa atual.")
        print(f"Detalhe: {e}")
        print("="*60)

if __name__ == "__main__":
    run_pipeline()
