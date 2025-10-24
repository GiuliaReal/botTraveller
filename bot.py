import os

from botcity.maestro import *
from rich.console import Console
from rich.markdown import Markdown

from setup.crew import BotTourCrew

maestro = BotMaestroSDK.from_sys_args()
maestro.RAISE_NOT_CONNECTED = False
maestro.VERIFY_SSL_CERT = False

execution = maestro.get_execution()

def run(destino: str, budget: str) -> str:
    inputs = {
        'destino': destino,
        'budget': budget
    }
    output = BotTourCrew().crew().kickoff(inputs=inputs)
    return output.raw

if __name__ == '__main__':

    SERPER_API_KEY = maestro.get_credential(label="workshop_apa", key="SERPER_API_KEY")
    OPENAI_API_KEY = maestro.get_credential(label="workshop_apa", key="OPENAI_API_KEY")
    
    os.environ['OPENAI_API_KEY'] = OPENAI_API_KEY
    os.environ['SERPER_API_KEY'] = SERPER_API_KEY

    try:

        destino: str = execution.parameters.get("destino")
        budget: str = execution.parameters.get("budget")

        maestro.alert(
            task_id=execution.task_id,
            title="Bot Travel iniciou a tarefa",
            message="Bot Iniciado com sucesso",
            alert_type=AlertType.INFO)

        output = run(destino, budget)
        console = Console()
        console.print(Markdown(output))
        nome_arquivo = f"roteiro-viagem-{destino}.md"

        with open(nome_arquivo, 'w', encoding='utf-8') as arquivo:
            arquivo.write(output)

        print(f"Arquivo '{nome_arquivo}' gerado com sucesso!")

        # A extensão é de outros tipos de arquivo
        maestro.post_artifact(
            task_id=execution.task_id,
            artifact_name=f"roteiro-{destino}",
            filepath= f"./{nome_arquivo}"
        )

        status = AutomationTaskFinishStatus.SUCCESS

        message = "Roteiro de viagem finalizada com sucesso!"
        
    except Exception as exc:
        maestro.error(maestro.task_id, exc)
        status = AutomationTaskFinishStatus.FAILED
        message = f"Houve falha de execução ==> erro :{exc}"
    finally:
        maestro.alert(
            task_id=execution.task_id,
            title="Bot Travel FINALIZADO",
            message="Bot Inicifinalizado com sucesso",
            alert_type=AlertType.INFO)
        maestro.finish_task(maestro.task_id,status=status, message=message)
    

