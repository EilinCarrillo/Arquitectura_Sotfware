function enableButtons() {
    document.getElementById("btnAttack").disabled = false;
    document.getElementById("btnDefend").disabled = false;
    document.getElementById("btnHeal").disabled = false;
}

function disableButtons() {
    document.getElementById("btnAttack").disabled = true;
    document.getElementById("btnDefend").disabled = true;
    document.getElementById("btnHeal").disabled = true;
}

async function startGame() {
    const res = await fetch("/start");
    const data = await res.json();

    document.getElementById("playerHP").innerText = data.player_hp;
    document.getElementById("enemyHP").innerText = data.enemy_hp;
    document.getElementById("msg").innerText = data.message;

    enableButtons();
}

async function attack() {
    const res = await fetch("/attack");
    const data = await res.json();

    document.getElementById("playerHP").innerText = data.player_hp;
    document.getElementById("enemyHP").innerText = data.enemy_hp;
    document.getElementById("msg").innerText = data.message;

    if (data.player_hp <= 0 || data.enemy_hp <= 0) {
        disableButtons();
    }
}

async function defend() {
    const res = await fetch("/defend");
    const data = await res.json();

    document.getElementById("playerHP").innerText = data.player_hp;
    document.getElementById("enemyHP").innerText = data.enemy_hp;
    document.getElementById("msg").innerText = data.message;

    if (data.player_hp <= 0) disableButtons();
}

async function heal() {
    const res = await fetch("/heal");
    const data = await res.json();

    document.getElementById("playerHP").innerText = data.player_hp;
    document.getElementById("enemyHP").innerText = data.enemy_hp;
    document.getElementById("msg").innerText = data.message;

    if (data.player_hp <= 0) disableButtons();
}
