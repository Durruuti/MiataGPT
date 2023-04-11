import openai
import config
import typer
from rich import print
from rich.table import Table

def main():

    openai.api_key = config.api_key

    print("[bold red]MIATAGPT (CHATGPTAPI) en Python[/bold red]")

    table = Table("Comando", "Descripción")
    table.add_row("exit", "Salir de la App")
    table.add_row("new", "Crear una nueva conversación")

    print(table)

    # Contexto del asistente

    context = {"role": "system", "content": "Eres un asistente de automoción japonesa"} 
    mensajes = [context]
    while True:

        contenido = __prompt()
        
        if contenido == "new":
            mensajes = [context]
            contenido = __prompt()
        
        mensajes.append({"role": "user", "content": contenido})

        respuesta = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", messages=mensajes)
        
        respuesta_content = respuesta.choices[0].messafe.content
        
        mensajes.append({"role": "assistant", "content": respuesta_content})

        print(f"[green]{respuesta_content}[/green]")


def __prompt() -> str:
    prompt = typer.prompt("\n¿Sobre qué quieres hablar? ")
        
    if prompt == "exit":
            exit = typer.confirm("¿Estás seguro? ")
            if exit:
                print("Hasta luego! ")
                raise typer.Abort()
            
            return __prompt()

    return prompt

if __name__ == "__main__":
    typer.run(main)