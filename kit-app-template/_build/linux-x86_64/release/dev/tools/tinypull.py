# SPDX-FileCopyrightText: Copyright (c) 2023-2025 NVIDIA CORPORATION & AFFILIATES. All rights reserved.
# SPDX-License-Identifier: MIT
#

# Pure python script to pull extensions
# written not to use packman, repo tools or any other extra dependencies

import argparse
import collections
import json
import logging
import os
import re
import subprocess
import sys
import time
from string import Template

logger = logging.getLogger(os.path.basename(__file__))


def _run_process_with_stdout_filter(args, exit_on_error=False) -> int:
    returncode = 0
    message = ""
    try:
        print(f"running process: {args}")
        p = subprocess.Popen(
            args, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, encoding="utf8"
        )

        # Launcher only prints stderr to the log. Try to find interesting information to propagate, like errors:
        _filter_output(p.stdout, sys.stderr)
        returncode = p.wait()
    except subprocess.CalledProcessError as e:
        returncode = e.returncode
        message = e.output
    except (FileNotFoundError, OSError) as e:
        returncode = -1
        message = str(e)

    if returncode != 0:
        logger.error(f'error running: {args}, code: {returncode}, message: "{message}"')

        # flush and sleep, that might help Launcher not to miss the output (?)
        sys.stdout.flush()
        sys.stderr.flush()
        time.sleep(1)

        if exit_on_error:
            sys.exit(returncode)
    return returncode


def _filter_output(input_, output):
    writing_lines = False
    log_file_message = None
    buffer = collections.deque()
    total_bytes = 0
    max_buffer = 200 * 1024
    for line in input_:
        line_lower = line.lower()
        # To make the minimal assumption about the log level of the output of the log path,
        # handle the log file path independent from the next if-else block.
        if "logging to" in line_lower:
            for token in line.split():
                if re.search(r"/kit_.+\.log", token):
                    log_file_message = f"An error occurred. See the log file at: {token}\n"
                    break

        if any(pattern in line_lower for pattern in ("[error]", "[warning]", "[warn]")):
            # Keep writing until we see an [info] line. There might be multiple lines.
            writing_lines = True
        elif "[info]" in line_lower:
            writing_lines = False
        else:
            # Keep the state.
            pass
        if writing_lines:
            buffer.append(line)
            total_bytes += len(line)
            while buffer and total_bytes >= max_buffer:
                total_bytes -= len(buffer.popleft())

    if log_file_message and buffer:
        buffer.appendleft(log_file_message)
        # Launcher filters out the output at the beginning when the output size is more than ~200KB, so we need to
        # append the message to the end when there's too many output. Use the threshold ~100KB to avoid
        # potential boundary issue.
        if total_bytes >= 100 * 1024:
            buffer.append(log_file_message)
    for line in buffer:
        output.write(line)
    output.flush()


def run():
    this_file_path = os.path.dirname(os.path.realpath(__file__))
    root_path = os.path.join(this_file_path, "..")
    repo_config = json.load(open(f"{root_path}/repo.json", "r"))

    registries = repo_config["repo_kit_pull_extensions"]["registries"]

    parser = argparse.ArgumentParser(description="Pull extensions for a kit")
    parser.add_argument(
        "--registry",
        dest="registry",
        default="public",
        help="Registry URL type to pull extensions from. (default: %(default)s)",
        choices=registries.keys(),
    )

    # Can be removed later, doesn't do anything anymore, left for backwards compatibility:
    parser.add_argument("-q", "--quiet", action="store_true", dest="quiet", required=False, default=False)

    options = parser.parse_args()

    registries = registries[options.registry]

    tokens = {}
    tokens["root"] = root_path
    tokens["exe_ext"] = ".exe" if os.name == "nt" else ""

    def resolve_tokens(path):
        return Template(path).substitute(tokens)

    tool_config = repo_config["repo_precache_exts"]
    if not tool_config.get("enabled", False):
        return

    kit_path = resolve_tokens(tool_config["kit_path"])

    apps = [resolve_tokens(path) for path in tool_config.get("apps", [])]

    # add generated app if set
    generated_app_path = tool_config.get("generated_app_path")
    if generated_app_path:
        apps += [resolve_tokens(generated_app_path)]

    for app_path in apps:
        args = [kit_path, app_path]

        args += ["--allow-root"]
        args += ["--ext-precache-mode"]
        args += ["--/app/settings/persistent=0"]
        args += ["--/app/settings/loadUserConfig=0"]
        args += ["--/app/enableStdoutOutput=1"]
        args += ["--/app/extensions/registryEnabled=1"]
        args += ["--/app/extensions/mkdirExtFolders=0"]
        args += ["--/log/flushStandardStreamOutput=1"]

        for i, registry in enumerate(registries):
            args += ['--/exts/omni.kit.registry.nucleus/registries/{}/name="{}"'.format(i, registry["name"])]
            args += ['--/exts/omni.kit.registry.nucleus/registries/{}/url="{}"'.format(i, registry["url"])]

        # where to install
        cache_path = resolve_tokens(tool_config["cache_path"])
        if cache_path:
            os.makedirs(cache_path, exist_ok=True)
            args += [f"--/app/extensions/registryCacheFull='{cache_path}'"]

        # portable mode
        if tool_config.get("kit_portable", True):
            args += ["--portable"]

        # ext folders
        ext_folders = [resolve_tokens(path) for path in tool_config.get("ext_folders", [])]
        for ext_folder in ext_folders:
            args += ["--ext-folder", ext_folder]

        if tool_config.get("kit_parallel_pull", False):
            args += ["--/app/extensions/parallelPullEnabled=1"]

        args += tool_config.get("kit_extra_args", [])

        _run_process_with_stdout_filter(args, exit_on_error=True)


if __name__ == "__main__":
    run()
