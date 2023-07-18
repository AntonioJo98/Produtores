
from typing import List
from core import app
import sys
import datetime

DIRECTOR = "realizador"

def help() -> str:

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


def register() -> None:
    """
    regista - regista um novo colaborador

    regista\n <tipo> <vedeta> <custo> <nome>


    """

    worker_info:str = input()
    info:List[str] = worker_info.split(" ")
    info_idx = 0

    try:
        type_worker = info[info_idx].lower()
        info_idx += 1

        if type_worker == "actor" or type_worker == DIRECTOR:
            # info = ["actor", "vedeta", "custo", "nome"]
            eww = info[1].lower()
            info_idx += 1
        else:
            # info = ["tecnico", "custo", "nome1", "nome2", ..., "nomek"]
            eww = None

        cost = int(info[info_idx])
        info_idx += 1

        name = " ".join(info[info_idx:]) # nome = "nome1 nome2 ... nomek"

        topo.check_worker(type_worker, eww, name, cost)

        topo.register_worker(type_worker, eww, name, cost)
        print("> Colaborador registado com sucesso!")
    except ValueError as e:
        print(f"> {e}")


def staff() -> str:
    """
    staff - lista os colaboradores registados

    """

    return topo.print_staff()
    

def register_stage():
    stage_name = input("")
    stage_price = int(input(""))
    try:
        topo.check_stage(stage_name, stage_price)
        topo.register_stage(stage_name, stage_price)
        print("> Cenario registado.")
    except ValueError as e:    
        print(f"> {e}")


def stages():
    return topo.print_stages()

def print_done():
    return topo.print_done()

def print_scheduled():
    return topo.print_scheduled()


def schedule():

    stage_name = input("")
    time = input("").split(" ")
    duration = int(time[-1])
    time = " ".join(time[:-1])
    time += " 00"
    date = datetime.datetime.strptime(time, '%Y %m %d %H %M %S')
    
    producer_name = input("")
    director_name = input("")
    tech_name = input("")

    n_colab = int(input(""))
    colabs = []
    for _ in range(n_colab):
        colab = input("")
        colabs.append(colab)
    try:
        topo.check_event(date, duration, stage_name, producer_name, director_name, tech_name, colabs)
        topo.schedule(date, duration, stage_name, producer_name, director_name, tech_name, colabs)
        print("> Gravacao agendada com sucesso!")
    except ValueError as e:
        print(f"> {e}")


def record():
    print(f"> {topo.record()}")


def print_stage_events():
    try:
        stage_name = input("")
        print("> " + topo.print_tbd_stage(stage_name))
    except ValueError as e:
        print(f"> {e}")

def print_worker_events():
    try:
        worker_name = input("")
        print("> " + topo.print_tbd_colaborator(worker_name))
    except ValueError as e:
        print(f"> {e}")

def amua():
    try:
        vedeta = input("")
        colaborador = input("")
        topo.check_amua(vedeta, colaborador)
        suspended_recordings = topo.amua(vedeta, colaborador)
        print(f"> {vedeta} colocou {colaborador} na sua lista negra, suspendendo {suspended_recordings} gravacoes.")
    except ValueError as e:
        print(f"> {e}")

def reconcilia():
    try:
        vedeta = input("")
        colaborador = input("")
        topo.check_reconcilia(vedeta, colaborador)
        saved_recordings = topo.reconcilia(vedeta, colaborador)
        print(f"> {vedeta} <3 {colaborador}. {saved_recordings} gravacoes salvas!")
    except ValueError as e:
        print(f"> {e}")

def resolve_cmd(cmd:str):

    cmd = cmd.lower()

    if cmd == "sai":
        print("> Ate a proxima")
        sys.exit(0)
    elif cmd == "ajuda":
        print("> " + help())
    elif cmd == "regista":
        register()
    elif cmd == "staff":
        print("> " + staff())
    elif cmd == "cenario":
        register_stage()
    elif cmd == "cenarios":
        print("> " + stages())
    elif cmd == 'marca':
        schedule()
    elif cmd == "realizadas":
        print("> " + print_done())
    elif cmd == "previstas":
        print("> " + print_scheduled())
    elif cmd == "grava":
        record()
    elif cmd == "local":
        print_stage_events()
    elif cmd == "colaborador":
        print_worker_events()
    elif cmd == "amua":
        amua()
    elif cmd == "reconcilia":
        reconcilia()
    else:
       print("Opcao inexistente.")


if __name__ == "__main__":

    topo = app.Application()

    while True:
        cmd = input()
        resolve_cmd(cmd)

    

