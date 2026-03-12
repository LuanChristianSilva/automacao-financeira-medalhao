import csv
import uuid
import datetime
import subprocess
import os

class PipelineLogger:
    def __init__(self, stage, script_name, log_file_path):
        """
        Inicializa o Logger para o Power BI.
        
        :param stage: Bronze, Silver, Gold ou Validation
        :param script_name: Nome do arquivo atual (ex: extractor.py)
        :param log_file_path: Caminho completo para o CSV de log desta etapa
        """
        self.stage = stage
        self.script_name = script_name
        self.log_file_path = log_file_path
        
        # Gera o ID unico da Execucao completa (Run ID)
        self.run_id = str(uuid.uuid4())
        
        # Tenta pegar os identificadores do Git (CI / Rastreabilidade)
        self.branch = self._get_git_branch()
        self.commit_sha = self._get_git_commit()
        
        # Detecta o ambiente.
        # No futuro, se houver GitHub Actions ou Jenkins, pode olhar pra variaveis de ambiente
        self.environment = "CI" if os.environ.get("CI") else "local"

        # Variavel auxiliar para medir tempo
        self._start_time = None

    def _get_git_branch(self):
        try:
            return subprocess.check_output(['git', 'rev-parse', '--abbrev-ref', 'HEAD'], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        except Exception:
            return "unknown-branch"

    def _get_git_commit(self):
        try:
             return subprocess.check_output(['git', 'rev-parse', '--short', 'HEAD'], stderr=subprocess.DEVNULL).decode('utf-8').strip()
        except Exception:
            return "unknown-commit"
            
    def _write_log(self, status, severity, input_path="", output_path="", 
                   entity_name="", metric_name="", metric_value="", metric_unit="", 
                   row_count="", error_code="", error_message="", action_taken="", 
                   duration_ms="", notes=""):
        """Grava a linha formatada no arquivo CSV com header padrão"""
        
        now_iso = datetime.datetime.now(datetime.timezone.utc).astimezone().replace(microsecond=0).isoformat()
        log_id = str(uuid.uuid4())
        
        row = {
            "log_id": log_id,
            "run_id": self.run_id,
            "event_ts": now_iso,
            "stage": self.stage,
            "script_name": self.script_name,
            "status": status,
            "severity": severity,
            "environment": self.environment,
            "branch": self.branch,
            "commit_sha": self.commit_sha,
            "input_path": input_path,
            "output_path": output_path,
            "entity_name": entity_name,
            "metric_name": metric_name,
            "metric_value": metric_value,
            "metric_unit": metric_unit,
            "row_count": row_count,
            "error_code": error_code,
            "error_message": error_message,
            "action_taken": action_taken,
            "duration_ms": duration_ms,
            "notes": notes
        }
        
        # Garante que as pastas e o arquivo existam
        os.makedirs(os.path.dirname(self.log_file_path), exist_ok=True)
        file_exists = os.path.exists(self.log_file_path)
        
        # Faz o append no CSV
        with open(self.log_file_path, mode='a', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=row.keys())
            if not file_exists:
                writer.writeheader()
            writer.writerow(row)
            
    def start(self, notes=""):
        """Inicia a medição de tempo e loga evento de STARTED"""
        self._start_time = datetime.datetime.now()
        self._write_log(status="STARTED", severity="INFO", notes=notes)
        
    def finish(self, notes=""):
        """Calcula o tempo desde o start e loga evento de FINISHED"""
        duration = ""
        if self._start_time:
            delta = datetime.datetime.now() - self._start_time
            duration = int(delta.total_seconds() * 1000)
            
        self._write_log(status="FINISHED", severity="INFO", duration_ms=duration, notes=notes)

    def log_metric(self, entity_name, metric_name, metric_value, metric_unit="", row_count="", notes=""):
        """Log para medições e volumes de dados do Data Pipeline"""
        self._write_log(status="SUCCESS", severity="INFO",
                        entity_name=entity_name, metric_name=metric_name, 
                        metric_value=metric_value, metric_unit=metric_unit, 
                        row_count=row_count, notes=notes)

    def log_error(self, error_message, error_code="", action_taken="", notes=""):
        """Log para registrar exceções ou falhas operacionais"""
        self._write_log(status="ERROR", severity="ERROR",
                        error_message=str(error_message), error_code=error_code,
                        action_taken=action_taken, notes=notes)

    def log_warning(self, error_message, error_code="", action_taken="", notes=""):
        """Log para alertas que não interrompem 100% o pipeline"""
        self._write_log(status="WARNING", severity="WARN",
                        error_message=str(error_message), error_code=error_code,
                        action_taken=action_taken, notes=notes)
