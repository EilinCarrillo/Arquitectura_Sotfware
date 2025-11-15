from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
import random

app = FastAPI(title="Mini Combate RPG")

# Servir carpeta static en /static
app.mount("/static", StaticFiles(directory="static"), name="static")


class GameState:
    def __init__(self):
        self.reset()

    def reset(self):
        self.player_hp = 100
        self.enemy_hp = 100
        self.turn = "player"
        self.message = "Nueva partida iniciada."

    def to_dict(self):
        return {
            "player_hp": self.player_hp,
            "enemy_hp": self.enemy_hp,
            "turn": self.turn,
            "message": self.message,
        }

game = GameState()


class ActionRequest(BaseModel):
    action: str  # "attack", "defend", "heal"


def enemy_action():
    # 75% atacar (15 daño), 25% curarse (10)
    if random.random() < 0.75:
        return ("attack", 15)
    else:
        return ("heal", 10)


@app.post("/start")
def start():
    global game
    game.reset()
    game.message = "Juego iniciado (backend)."
    return {"message": "Juego iniciado", **game.to_dict()}


@app.post("/action")
def action(req: ActionRequest):
    global game
    a = req.action.lower()

    # Si la partida está terminada, reiniciar automáticamente y avisar
    if game.player_hp <= 0 or game.enemy_hp <= 0:
        prev = "Se reinicia la partida porque la anterior terminó."
        game.reset()
        game.message = prev
        return {"message": prev, **game.to_dict()}

    game.message = ""
    # Acción del jugador
    if a == "attack":
        dmg = 20
        game.enemy_hp -= dmg
        game.message = f"Atacaste y causaste {dmg} de daño."
    elif a == "defend":
        heal = 5
        game.player_hp = min(100, game.player_hp + heal)
        game.message = f"Te defendiste y recuperaste {heal} HP."
    elif a == "heal":
        heal = 15
        game.player_hp = min(100, game.player_hp + heal)
        game.message = f"Te curaste {heal} HP."
    else:
        return {"error": "Acción inválida. Usa 'attack', 'defend' o 'heal'."}

    # Si el enemigo murió por el ataque del jugador
    if game.enemy_hp <= 0:
        msg = f"{game.message} | ¡Ganaste! Reiniciando partida..."
        game.reset()
        game.message = msg
        return {"message": msg, **game.to_dict()}

    # Turno del enemigo
    e_act, value = enemy_action()
    if e_act == "attack":
        game.player_hp -= value
        game.message += f" | Turno del enemigo: te atacó y te hizo {value} de daño."
    else:
        game.enemy_hp = min(100, game.enemy_hp + value)
        game.message += f" | Turno del enemigo: se curó {value} HP."

    # Revisar si el jugador murió
    if game.player_hp <= 0:
        msg = f"{game.message} | Perdiste. Reiniciando partida..."
        game.reset()
        game.message = msg
        return {"message": msg, **game.to_dict()}

    # Normal: devolver estado actual
    return {"message": game.message, **game.to_dict()}


@app.get("/status")
def status():
    return game.to_dict()

import os
import uvicorn

if __name__ == "__main__":
    port = int(os.getenv("PORT", 8000))  # Railway define PORT automáticamente
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=port
    )