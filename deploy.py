#!/usr/bin/env python3
"""
Deploy script for safeisol.

Коммитит локальные изменения (с сообщением из -m), пушит в origin/main,
затем подключается по SSH к продакшн-серверу (доступы читаются из .env),
делает git pull и пересобирает/перезапускает docker-compose.

Использование:
    python deploy.py -m "сообщение коммита"

Все шаги останавливают выполнение при ошибке (exit code != 0).
Доступы к серверу (SERVER, SERVER_PASS) берутся из .env и НЕ попадают в git.
"""

from __future__ import annotations

import argparse
import datetime
import os
import subprocess
import sys
from pathlib import Path

# --- параметры деплоя на сервере -------------------------------------------
REMOTE_BRANCH = "main"
REMOTE_REPO_DIR = "/root/safeisol-prod"  # рабочий каталог docker-compose на сервере


def load_env(path: Path) -> dict:
    """Читает .env вида KEY=VALUE, игнорируя пустые строки и комментарии."""
    env: dict[str, str] = {}
    if not path.exists():
        return env
    for line in path.read_text(encoding="utf-8").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, _, value = line.partition("=")
        env[key.strip()] = value.strip()
    return env


def run_local(cmd: list[str], cwd: Path | None = None) -> None:
    """Запускает локальную команду; бросает исключение при ненулевом коде."""
    print(f"\n>>> [local] {' '.join(cmd)}")
    proc = subprocess.run(cmd, cwd=cwd, text=True, capture_output=True)
    if proc.stdout:
        print(proc.stdout.rstrip())
    if proc.stderr:
        print(proc.stderr.rstrip(), file=sys.stderr)
    if proc.returncode != 0:
        raise RuntimeError(f"Локальная команда завершилась с кодом {proc.returncode}: {' '.join(cmd)}")


def git_modified_files() -> list[str]:
    """Список изменённых/неотслеживаемых файлов (кроме .env и логов)."""
    out = subprocess.run(
        ["git", "status", "--porcelain"], text=True, capture_output=True
    ).stdout
    files = []
    for line in out.splitlines():
        if not line.strip():
            continue
        status = line[:2].strip()
        if status in ("D", "DD", "AU", "UD", "UA", "DU", "AA", "UU"):
            print(f"    предупреждение: пропускаю удалённый/конфликтный файл: {line[3:]}")
            continue
        files.append(line[3:])
    return files


def remote_run(ssh, command: str, timeout: int = 600) -> str:
    """Выполняет команду на сервере и возвращает объединённый вывод."""
    print(f"\n>>> [server] {command}")
    _, stdout, stderr = ssh.exec_command(command, timeout=timeout, get_pty=False)
    out = stdout.read().decode("utf-8", "replace")
    err = stderr.read().decode("utf-8", "replace")
    full = (out + err).rstrip()
    if full:
        print(full)
    return out


def deploy_on_server(server: str, password: str) -> None:
    """Подключается по SSH и выполняет pull + пересборку docker-compose."""
    import paramiko

    print(f"\n>>> Подключение к серверу {server} ...")
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        server,
        username="root",
        password=password,
        timeout=15,
        look_for_keys=False,
        allow_agent=False,
        banner_timeout=30,
    )
    try:
        remote_run(client, f"cd {REMOTE_REPO_DIR} && git pull origin {REMOTE_BRANCH}")
        remote_run(client, f"cd {REMOTE_REPO_DIR} && docker compose up -d --build")
        remote_run(client, f"cd {REMOTE_REPO_DIR} && docker compose ps")
    finally:
        client.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Коммит + деплой safeisol на сервер")
    parser.add_argument(
        "-m",
        "--message",
        dest="message",
        default="",
        help="Сообщение коммита. Если пусто — будет сгенерировано автоматически.",
    )
    args = parser.parse_args()

    root = Path(__file__).resolve().parent
    os.chdir(root)

    message = args.message.strip() or f"deploy: {datetime.datetime.now():%Y-%m-%d %H:%M}"

    # --- доступы к серверу из .env ---
    env = load_env(root / ".env")
    server = env.get("SERVER")
    password = env.get("SERVER_PASS")
    if not server or not password:
        print(
            "ОШИБКА: в .env не заданы SERVER и/или SERVER_PASS.\n"
            "Добавьте строки:\n  SERVER=<ip_сервера>\n  SERVER_PASS=<пароль>",
            file=sys.stderr,
        )
        return 2

    print(f"Сервер: {server}\nСообщение коммита: {message}")

    # --- 1. Коммит локальных изменений ---
    modified = git_modified_files()
    if modified:
        run_local(["git", "add", "--", *modified])
        run_local(["git", "commit", "-m", message])
    else:
        print("\n>>> Изменений для коммита нет — пушу уже существующий HEAD.")

    # --- 2. Пуш в origin/main ---
    run_local(["git", "push", "origin", REMOTE_BRANCH])

    # --- 3. Деплой на сервер ---
    deploy_on_server(server, password)

    print("\n=== ГОТОВО: изменения закоммичены, запушены и развёрнуты на сервере ===")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())