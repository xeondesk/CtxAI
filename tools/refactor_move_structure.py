import shutil
from pathlib import Path

ROOT = Path(".").resolve()
SRC = ROOT / "src" / "ctxai"

DRY_RUN = False

# Mapping: old -> new
MOVE_MAP = {

    # helpers → core
    "helpers/runtime.py": "src/ctxai/core/runtime/runtime.py",
    "helpers/call_llm.py": "src/ctxai/core/llm/call_llm.py",
    "helpers/tool.py": "src/ctxai/core/tools/tool.py",
    "helpers/plugins.py": "src/ctxai/core/plugins/plugin_manager.py",
    "helpers/subagents.py": "src/ctxai/core/agent/subagents.py",

    # helpers → infrastructure
    "helpers/docker.py": "src/ctxai/infrastructure/docker/docker_manager.py",
    "helpers/git.py": "src/ctxai/infrastructure/git/git_service.py",
    "helpers/playwright.py": "src/ctxai/infrastructure/browser/playwright_service.py",
    "helpers/websocket.py": "src/ctxai/infrastructure/websocket/server.py",
    "helpers/websocket_manager.py": "src/ctxai/infrastructure/websocket/manager.py",
    "helpers/email_client.py": "src/ctxai/infrastructure/email/client.py",
    "helpers/vector_db.py": "src/ctxai/infrastructure/vector/vector_db.py",

    # helpers → storage
    "helpers/history.py": "src/ctxai/storage/history_store.py",
    "helpers/cache.py": "src/ctxai/storage/cache_store.py",
    "helpers/persist_chat.py": "src/ctxai/storage/chat_store.py",
    "helpers/state_snapshot.py": "src/ctxai/storage/state_snapshot.py",

    # helpers → config
    "helpers/settings.py": "src/ctxai/config/settings.py",
    "helpers/providers.py": "src/ctxai/config/providers.py",
    "helpers/secrets.py": "src/ctxai/config/secrets.py",

    # helpers → utils
    "helpers/crypto.py": "src/ctxai/utils/crypto.py",
    "helpers/strings.py": "src/ctxai/utils/strings.py",
    "helpers/dirty_json.py": "src/ctxai/utils/dirty_json.py",
    "helpers/guids.py": "src/ctxai/utils/guids.py",
    "helpers/wait.py": "src/ctxai/utils/wait.py",

    # agents
    "agents": "src/ctxai/agents",

    # prompts
    "prompts": "src/ctxai/prompts",

    # skills
    "skills": "src/ctxai/skills",

    # tools
    "tools": "src/ctxai/tools",

    # extensions
    "extensions": "src/ctxai/extensions",

    # conf
    "conf": "src/ctxai/config",

}


def ensure_init(path: Path):
    while path != ROOT:
        init = path / "__init__.py"
        if not init.exists():
            init.touch()
        path = path.parent


def move_item(src, dst):

    src_path = ROOT / src
    dst_path = ROOT / dst

    if not src_path.exists():
        print("SKIP missing:", src)
        return

    if dst_path.exists():
        print("CONFLICT exists:", dst)
        return

    print("MOVE:", src, "->", dst)

    if DRY_RUN:
        return

    dst_path.parent.mkdir(parents=True, exist_ok=True)

    shutil.move(str(src_path), str(dst_path))

    ensure_init(dst_path.parent)

    # create compatibility shim
    if src_path.suffix == ".py":

        module_path = (
            dst.replace("src/", "")
            .replace("/", ".")
            .replace(".py", "")
        )

        shim = f'# AUTO-GENERATED COMPATIBILITY SHIM\nfrom {module_path} import *\n'

        src_path.parent.mkdir(parents=True, exist_ok=True)

        with open(src_path, "w") as f:
            f.write(shim)

        print("Shim created:", src)


def main():

    print("\nCTXAI Refactor Move Script\n")

    for src, dst in MOVE_MAP.items():
        move_item(src, dst)

    print("\nDONE\n")


if __name__ == "__main__":
    main()