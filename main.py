import openai
import config
import typer
from rich import print
from rich.console import Console
from rich.table import Table

console = Console()

# Constantes
EXIT_COMMAND = "exit"
NEW_CONVERSATION_COMMAND = "new"
MAX_MESSAGES = 10

def main():

    openai.api_key = config.api_key

    console.print("[bold red]MIATAGPT (CHATGPTAPI) en Python[/bold red]")

    table = Table("Comando", "Descripción")
    table.add_row(EXIT_COMMAND, "Salir de la App")
    table.add_row(NEW_CONVERSATION_COMMAND, "Crear una nueva conversación")

    console.print(table)

    # Contexto del asistente
    context = {"role": "system", "content": "Eres un asistente de automoción japonesa"} 
    messages = [context]

    while True:
        content = __prompt()

        if content == NEW_CONVERSATION_COMMAND:
            messages = [context]
            content = __prompt()
        
        if content == EXIT_COMMAND:
            if typer.confirm("¿Estás seguro que deseas salir?"):
                console.print("¡Hasta luego!")
                raise typer.Abort()

        messages.append({"role": "user", "content": content})

        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=f"\n\n\nUsuario: {messages[-1]['content']}\nAsistente: ",
            max_tokens=50,
            temperature=0.5,
            n=1,
            stop=None,
            messages=messages[-MAX_MESSAGES:],
        )

        response_text = response.choices[0].text.strip()
        messages.append({"role": "assistant", "content": response_text})

        console.print(f"[bold blue]Asistente:[/bold blue] {response_text}")


def __prompt() -> str:
    prompt = typer.prompt("\n¿Sobre qué quieres hablar? ")
        
    return prompt.lower().strip()

if __name__ == "__main__":
    typer.run(main)
