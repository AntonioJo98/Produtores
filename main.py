
from typing import List
from core import app
import sys

DIRECTOR = "realizador"

def help():

    return f"""regista - regista um novo colaborador
staff - lista os colaboradores registados
cenario - regista um novo local para gravacoes
cenarios - lista os locais para gravacoes registados
marca - marca uma nova gravacao
amua - vedeta deixa de trabalhar com colaborador
reconcilia - vedeta faz as pazes com colaborador
realizadas - lista as gravacoes realizadas
previstas - lista as gravacoes previstas
local - lista as gravacoes previstas para um local
colaborador - lista as gravacoes previstas para um colaborador
grava - executa a proxima gravacao agendada
amuancos - lista os colaboradores com quem uma vedeta esta amuada
ajuda - Mostra a ajuda
sai - Termina a execucao do programa"""


def register():

    worker_info:str = input()

    info:List[str] = worker_info.split(" ")

    try:

        type_worker = info[0].lower()

        if type_worker == "actor" or type_worker == DIRECTOR:
            # info = ["actor", "vedeta", "custo", "nome"]
            eww = info[1].lower()
            info_idx = 2

            if eww != "vedeta" and eww != "normal":
                raise ValueError(f"Tipo de vedeta desconhecido.")
        else:
            # info = ["tecnico", "custo", "nome1", "nome2", ..., "nomek"]
            eww = None

            info_idx = 1

        cost = int(info[info_idx])
        info_idx += 1

        name = " ".join(info[info_idx:])

        topo.register_worker(type_worker, eww == "vedeta", name, cost)

    except ValueError as e:
        print(e)



    


def resolve_cmd(cmd:str):

    cmd = cmd.lower()

    if cmd == "sai":
        sys.exit("Ate a proxima.")
    elif cmd == "ajuda":
        print(help())
    elif cmd == "regista":
        register()
    else:
       raise ValueError(f"Opcao inexistente.")


if __name__ == "__main__":

    topo = app.Application()

    cmd = input("Comando: ")

    while True:

        resolve_cmd(cmd)

    

