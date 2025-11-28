#! /usr/bin/python3

"""
manage.py stop all
manage.py stop traefik nextcloud

manage.py start all
manage.py start traefik nextcloud
"""

from pathlib import Path
import argparse
import subprocess
from dataclasses import dataclass
import logging
from typing import Literal

LOGGER = logging.getLogger()
logging.basicConfig(level=logging.DEBUG)

HELP_TEXT_LIST = "Either 'all' or a list of services"
SUBPATH_PROD = "prod"
CWD = Path(__file__).parent

@dataclass
class Service:
    """Represents one docker-compose service.

    Requires directory structure:
    -NAME
        |-prod
            |-NAME.docker-compose.yaml
            |-compose.override.yaml
    """
    name: str
    dir: Path
    compose_file: Path
    override_file: Path

def find_service_paths(dir: Path) -> list[Path]:
    """Searches for directories within dir that contain a 'prod' directory.

    Args:
        dir: Root directory

    Returns:
        List of parent directories containing a 'prod' directory
    """
    paths = []
    for path in dir.iterdir():
        if path.is_dir() and path.joinpath(SUBPATH_PROD).is_dir():
            paths.append(path)

    return paths

def find_services(paths: list[Path]) -> tuple[dict[str, Service], list[Service]]:
    """Generates a set of services based on a list of valid service root directories.

    Args:
        paths: Service directories (directories that contain a 'prod' sub-directory)

    Returns:
        Map of valid services (service name -> service) and a list of potential invalid services
    """
    services = dict()
    faulty = list()

    for path in paths:
        service_name = str(path.relative_to(CWD))
        service = Service(
            name = service_name,
            dir=path,
            compose_file=path.joinpath(SUBPATH_PROD).joinpath(f"{service_name}.docker-compose.yaml"),
            override_file=path.joinpath(SUBPATH_PROD).joinpath("compose.override.yaml")
        )

        if len(validate_service(service)) >0:
            faulty.append(service)
        else:
            services[service_name] = service

    return services, faulty

def validate_service(service: Service) -> list[Path]:
    """Validates a service. A service is valid if all directories and files exist.

    Args:
        service: Service

    Returns:
        List of invalid paths
    """
    faulty_paths = list()
    if not service.dir.is_dir():
        faulty_paths.append(service.dir)

    if not service.compose_file.is_file() or not service.compose_file.suffix == ".yaml":
        faulty_paths.append(service.compose_file)

    if not service.override_file.is_file() or not service.override_file.suffix == ".yaml":
        faulty_paths.append(service.override_file)

    return faulty_paths

def docker_command_for(service: Service, command: Literal["up", "down"]) -> list[str]:
    """Create a list of commands that can be executed on the CLI for the docker compose command specified.

    Args:
        service: Target service
        command: Docker compose command (up, down)

    Returns:
        List of commands that can be executed e.g. as a subprocess.
    """
    _command = ["docker", "compose", "-f", str(service.compose_file), "-f", str(service.override_file), command]

    if command == "up":
        _command.append("-d")

    return _command

def do_command(service_names: list[str], command: Literal["up", "down"]) -> None:
    """Execute a command for a set of service names (can be ['all'] or a list of services ['s1', 's2']).

    Args:
        service_names: Services to execute the command for
        command: Docker compose command (up, down)
    """
    paths = find_service_paths(CWD)
    services, faulty = find_services(paths)

    if len(faulty) > 0:
        LOGGER.warning(f"Faulty services found: {faulty}")

    service_names = services.keys() if "all" in service_names else service_names
    LOGGER.debug(f"Executing '{command}' for {service_names}")

    for name in service_names:
        if name not in services:
            LOGGER.error(f"Unknown service: '{name}")
        else:
            service = services[name]

            proc = subprocess.run(docker_command_for(service, command))

            if proc.returncode != 0:
                LOGGER.error(f"Failed to '{command}' service: '{service.name}'")

def do_start(service_names: list[str]) -> None:
    """Run 'up' for a set of services.

    Args:
        service_names: Service names (either ['all'] or a set of names ['s1', 's2'])
    """
    LOGGER.info(f"Starting services {service_names}")
    do_command(service_names, "up")
    LOGGER.info("Done.")

def do_stop(service_names: list[str]):
    """Run 'down -d' for a set of services.

    Args:
        service_names: Service names (either ['all'] or a set of names ['s1', 's2'])
    """
    LOGGER.info(f"Stopping services {service_names}")
    do_command(service_names, "down")
    LOGGER.info("Done.")

def get_log_level(level_str: Literal["debug", "info", "error"]) -> int:
    """Map a string log level to a logging log level.

    Args:
        level_str: String log level

    Returns:
        Log level compatible to the logging module
    """
    match level_str:
        case "debug":
            return logging.DEBUG
        case "info":
            return logging.INFO
        case "error":
            return logging.ERROR
        
    return logging.INFO

if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="manager")
    parser.add_argument("--log", default="info", choices=["debug", "info", "error"])
    
    subparser = parser.add_subparsers()

    parser_stop = subparser.add_parser("stop")
    parser_stop.add_argument("LIST", nargs="+", help=HELP_TEXT_LIST)
    parser_stop.set_defaults(func=do_stop)

    parser_start = subparser.add_parser("start")
    parser_start.add_argument("LIST", nargs="+", help=HELP_TEXT_LIST)
    parser_start.set_defaults(func=do_start)

    args = parser.parse_args()

    LOGGER.setLevel(get_log_level(args.log))

    args.func(args.LIST)