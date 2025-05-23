#!/usr/bin/env python3
import os
import subprocess
from pathlib import Path
import shutil
import sys

# Directories to run `npm install`
NPM_DIRS = [
    "./demo/bank-app/frontend",
    "./demo/bank-app/backend",
    "./demo/dmv-app/frontend",
    "./demo/dmv-app/backend",
]

# Directory to run `yarn install`
YARN_DIR = "./snap"

# Backend .env targets (wallet + infura)
ENV_DIRS_BACKEND = [
    "./demo/bank-app/backend",
    "./demo/dmv-app/backend"
]

# Snap .env target (infura + companion origin)
ENV_DIR_SNAP = "./snap/packages/snap"

# Frontend local env target
ENV_FILE_BANK_FRONTEND = "./demo/bank-app/frontend/.env.local"

def check_command_exists(command):
    return shutil.which(command) is not None

def run_install(command, path):
    try:
        print(f"🔧 Running `{command} install` in {path}...")
        subprocess.run([command, "install"], cwd=path, check=True)
    except subprocess.CalledProcessError:
        print(f"❌ Error: `{command} install` failed in {path}.")
        sys.exit(1)

def write_env_file_backend(path, wallet_key, infura_id):
    env_path = Path(path) / ".env"
    env_contents = f'WALLET_PRIVATE_KEY="{wallet_key}"\nINFURA_PROJECT_ID="{infura_id}"\n'
    env_path.write_text(env_contents)
    print(f"✅ Wrote backend .env to {path}")

def write_env_file_snap(path, infura_id):
    env_path = Path(path) / ".env"
    env_contents = (
        f'INFURA_PROJECT_ID="{infura_id}"\n'
        'COMPANION_APP_ORIGIN="http://localhost:8000"\n'
    )
    env_path.write_text(env_contents)
    print(f"✅ Wrote snap .env to {path}")

def write_env_local_frontend(path):
    env_path = Path(path)
    env_contents = (
        'DB_HOST="127.0.0.1"\n'
        '# DB_PORT="3306"\n'
        'DB_USER="root"\n'
        '# DB_PASSWORD="your_db_password"\n'
        'DB_NAME="demo"\n'
    )
    env_path.write_text(env_contents)
    print(f"✅ Wrote frontend .env.local to {path}")

def main():
    print("🚀 Project setup starting...\n")

    if not check_command_exists("npm"):
        print("❌ Error: `npm` is not installed or not in PATH.")
        sys.exit(1)

    if not check_command_exists("yarn"):
        print("❌ Error: `yarn` is not installed or not in PATH.")
        sys.exit(1)

    wallet_key = input("🔑 Enter your Ethereum wallet private key: ").strip()
    infura_id = input("🔌 Enter your Infura testnet project ID: ").strip()

    for directory in NPM_DIRS:
        run_install("npm", directory)

    run_install("yarn", YARN_DIR)

    for directory in ENV_DIRS_BACKEND:
        write_env_file_backend(directory, wallet_key, infura_id)

    write_env_file_snap(ENV_DIR_SNAP, infura_id)

    write_env_local_frontend(ENV_FILE_BANK_FRONTEND)

    print("\n✅ Setup complete! You're ready to start development.")

if __name__ == "__main__":
    main()
