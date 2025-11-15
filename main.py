from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import JSONResponse
import random
import os
import uvicorn

app = FastAPI()

# Estado del juego
player_hp = 100
enemy_hp = 100
game_over = False


@app.get("/start")
def start_game():
    global player_hp, enemy_hp, game_over
    player_hp = 100
    enemy_hp = 100
    game_over = False
    return {"player_hp": player_hp, "enemy_hp": enemy_hp, "message": "Juego iniciado!"}


@app.get("/attack")
def attack():
    global player_hp, enemy_hp, game_over
    if game_over:
        return {"message": "El juego ha terminado."}

    damage = random.randint(10, 20)
    enemy_hp -= damage

    if enemy_hp <= 0:
        game_over = True
        enemy_hp = 0
        return {"player_hp": player_hp, "enemy_hp": enemy_hp, "message": f"Atacaste e hiciste {damage} de daño. ¡Ganaste la batalla!"}

    # enemigo contraataca
    enemy_damage = random.randint(5, 15)
    player_hp -= enemy_damage

    if player_hp <= 0:
        game_over = True
        player_hp = 0
        return {"player_hp": player_hp, "enemy_hp": enemy_hp, "message": f"Hiciste {damage} de daño, pero el enemigo te derrotó..."}

    return {
        "player_hp": player_hp,
        "enemy_hp": enemy_hp,
        "message": f"Atacaste e hiciste {damage} de daño. El enemigo contraataca por {enemy_damage}."
    }


@app.get("/defend")
def defend():
    global player_hp, enemy_hp, game_over
    if game_over:
        return {"message": "El juego ha terminado."}

    reduced = random.randint(5, 10)
    enemy_damage = max(0, random.randint(10, 20) - reduced)

    player_hp -= enemy_damage

    if player_hp <= 0:
        game_over = True
        player_hp = 0
        return {"player_hp": player_hp, "enemy_hp": enemy_hp, "message": "Te defendiste, pero aun así perdiste..."}

    return {
        "player_hp": player_hp,
        "enemy_hp": enemy_hp,
        "message": f"Te defendiste. El daño reducido fue {reduced}. Recibiste {enemy_damage}."
    }


@app.get("/heal")
def heal():
    global player_hp, enemy_hp, game_over
    if game_over:
        return {"message": "El juego ha terminado."}

    heal_amount = random.randint(10, 20)
    player_hp = min(100, player_hp + heal_amount)

    enemy_damage = random.randint(5, 15)
    player_hp -= enemy_damage

    if player_hp <= 0:
        game_over = True
        player_hp = 0
        return {"player_hp": player_hp, "enemy_hp": enemy_hp, "message": "Te curaste pero el enemigo te derrotó."}

    return {
        "player_hp": player_hp,
        "enemy_hp": enemy_hp,
        "message": f"Te curaste {heal_amount}. El enemigo atacó causando {enemy_damage}."
    }


# Servir archivos estáticos
app.mount("/static", StaticFiles(directory="static"), name="static")

# Para Railway
if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))
    uvicorn.run("main:app", host="0.0.0.0", port=port)
