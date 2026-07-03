---
name: devcontainer-bridge
description: >
  Execute CLI commands and technical workflows inside a project's dev-container,
  ensuring environment consistency with project-defined dependencies and tool versions.
  Use this skill whenever the workspace has a .devcontainer/ directory and the task
  requires running shell commands, build tools, test suites, or any CLI tools.
  Trigger even if the user doesn't say "container" — if they ask to run tests,
  execute a workflow, or use a project-specific CLI and a .devcontainer exists,
  bridge into the container first. This prevents "works on my machine" issues and
  ensures the right runtime versions are always used.
---

# Container-Bridge Skill

This skill bridges the agent into a running dev-container so all CLI commands execute
in the project's defined environment — not the host machine. The container is defined
by `.devcontainer/devcontainer.json` and may install tools via `postCreateCommand`
or features — check that file first to understand what's available inside.

## When to use this skill

- The workspace has a `.devcontainer/devcontainer.json` file
- The task involves running any CLI command, build step, or test suite
- The user asks to "run in the container" or "use the dev environment"
- The command requires tools that aren't guaranteed to exist on the host (e.g., specific Node versions, Python envs, project-specific CLIs)

Do **not** bridge for browser automation or tasks explicitly intended for the host.

---

## Step 1: Detect the environment

Check that the right pieces are in place before attempting a bridge:

```bash
# Confirm devcontainer config exists
ls .devcontainer/devcontainer.json

# Confirm Docker daemon is running
docker info --format '{{.ServerVersion}}'

# Confirm devcontainer CLI is available
devcontainer --version
```

If `devcontainer` CLI is missing, install it:
```bash
npm install -g @devcontainers/cli
```

If Docker isn't running, inform the user — the container won't start without it.

---

## Step 2: Start the container (if not already running)

```bash
devcontainer up --workspace-folder .
```

This is idempotent — safe to run even if the container is already up. It will pull the
image on first run, which can take a minute.

---

## Step 3: Establish a persistent bridge session

Use `run_command` with `RunPersistent: true` to create a reusable terminal session
inside the container:

```
run_command:
  CommandLine: devcontainer exec --workspace-folder . bash
  RunPersistent: true
```

Save the returned **TerminalID**. All subsequent commands should reuse this ID so they
run in the same container shell — this preserves environment variables, working
directory, and avoids container startup overhead on every command.

---

## Step 4: Verify the bridge

First, read the expected remote user from the devcontainer config on the **host**:

```bash
cat .devcontainer/devcontainer.json | grep remoteUser
```

Then, inside the container session, run a generic OS identity check:

```bash
uname -a && id && pwd
```

Confirm:
- `uname` shows Linux (not Darwin) — you're inside the container, not the host
- `id` shows the user matches the `remoteUser` value from `devcontainer.json`
- `pwd` reflects the workspace directory

If `postCreateCommand` tools aren't available yet, wait a moment or check the
Docker logs for the setup progress (`docker logs <container-id>`).

---

## Step 5: Execute commands via the persistent session

All build, test, and CLI commands should be sent as input to the stored TerminalID:

```
send_command_input:
  CommandId: <TerminalID from Step 3>
  Input: <your command here>\n
```

**Error recovery**: If a command fails unexpectedly, check whether the container is
still running (`docker ps`). If the session was lost, repeat from Step 3 to re-establish
the bridge. You do not need to re-run `devcontainer up`.

---

## Step 6: Clean up (optional)

There's no need to explicitly stop the container after each task — Docker containers
persist until the user stops them or restarts Docker. Close the persistent terminal
session when the task is complete to free resources.

---

## Reminders

- Check `devcontainer.json` for bind mounts — host paths mounted into the container affect credential and config access
- The remote user varies by project — always check `remoteUser` in `devcontainer.json` to know who owns files created inside the container
- Host-side tasks (browser automation, file access outside workspace) should use host tools directly, not the container bridge
