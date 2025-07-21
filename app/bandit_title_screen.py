#!/usr/bin/env python3
"""
BanditGUI Title Screen Module
Enhanced terminal interface for OverTheWire Bandit wargame web application.
"""

import os
import random
import re
import sys
import time
from typing import Optional

# ASCII Art Banner
BANDIT_TITLE = r"""
 ███▄ ▄███▓ ▄▄▄       ███▄    █   ██████  ██▓███  ▓█████  ██▀███
▓██▒▀█▀ ██▒▒████▄     ██ ▀█   █ ▒██    ▒ ▓██░  ██▒▓█   ▀ ▓██ ▒ ██▒
▓██    ▓██░▒██  ▀█▄  ▓██  ▀█ ██▒░ ▓██▄   ▓██░ ██▓▒▒███   ▓██ ░▄█ ▒
▒██    ▒██ ░██▄▄▄▄██ ▓██▒  ▐▌██▒  ▒   ██▒▒██▄█▓▒ ▒▒▓█  ▄ ▒██▀▀█▄
▒██▒   ░██▒ ▓█   ▓██▒▒██░   ▓██░▒██████▒▒░▒██▒ ░  ░░▒████▒░██▓ ▒██▒
░ ▒░   ░  ░ ▒▒   ▓▒█░░ ▒░   ▒ ▒ ▒ ▒▓▒ ▒ ░░ ▒▓ ░ ▒░░░ ▒░ ░░ ▒▓ ░▒▓░
░  ░      ░  ▒   ▒▒ ░░ ░░   ░ ▒░░ ░▒  ░ ░  ░▒ ░ ▒░ ░ ░  ░  ░▒ ░ ▒░
░      ░     ░   ▒      ░   ░ ░ ░  ░  ░    ░░   ░    ░     ░░   ░
       ░         ░  ░         ░       ░     ░        ░  ░   ░
"""

# Configuration
SUBTITLE = "Web Terminal Interface for OverTheWire Bandit"
LOADING_MESSAGES = [
    "Initializing SSH connection manager...",
    "Loading xterm.js terminal emulator...",
    "Setting up Paramiko SSH client...",
    "Configuring security protocols...",
    "Establishing secure channels...",
    "Ready to connect!",
]
# import datetime
CREDITS = f"(c) {datetime.datetime.now().year} Frederick Pellerin | Enhanced Terminal Experience"


# ANSI Color Codes
from enum import Enum


class Colors(Enum):
    RESET = "\033[0m"
    GREEN = "\033[92m"
    CYAN = "\033[96m"
    YELLOW = "\033[93m"
    RED = "\033[91m"
    BLUE = "\033[94m"
    MAGENTA = "\033[95m"
    WHITE = "\033[97m"
    DIM = "\033[2m"
    BOLD = "\033[1m"
    UNDERLINE = "\033[4m"


def clear_screen():
    """Clear the terminal screen."""
    # amazonq-ignore-next-line
    os.system("cls" if os.name == "nt" else "clear")


def get_terminal_width() -> int:
    """Get terminal width for centering text."""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return 80  # Default width


def center_text(text: str, width: Optional[int] = None) -> str:
    """Center text based on terminal width."""
    if width is None:
        width = get_terminal_width()

    lines = text.split("\n")
    centered_lines = []

    for line in lines:
        # Remove ANSI codes for length calculation
        # Use regex to strip all ANSI escape sequences
        clean_line = re.sub(r"\x1B(?:[@-Z\\-_]|\[[0-?]*[ -/]*[@-~])", "", line)
        padding = max(0, (width - len(clean_line)) // 2)
        centered_lines.append(" " * padding + line)

    return "\n".join(centered_lines)


def matrix_effect(text: str, duration: float = 2.0):
    """Create a Matrix-style digital rain effect."""
    lines = text.split("\n")
    chars = "01"

    start_time = time.time()
    while time.time() - start_time < duration:
        display_lines = []
        for line in lines:
            if random.random() < 0.3:  # 30% chance to show random chars
                random_line = "".join(random.choice(chars) for _ in range(len(line)))
                display_lines.append(Colors.GREEN + random_line + Colors.RESET)
            else:
                display_lines.append(line)

        print("\n".join(display_lines))
        time.sleep(0.1)
        if time.time() - start_time < duration - 0.1:
            print("\033[{}A".format(len(lines)), end="")  # Move cursor up

    # Show final text
    print("\n".join(lines))


# Import random and time modules for random choice and sleep functionality


def glitch_effect(text: str, glitch_times: int = 5, delay: float = 0.1):
    """Create a glitch effect with the text."""
    glitch_chars = "!@#$%^&*()_+-=[]{}|;':\",./<>?"

    for _ in range(glitch_times):
        # Create glitched version
        glitched = []
        for char in text:
            if char != "\n" and random.random() < 0.1:
                glitched.append(random.choice(glitch_chars))
            else:
                glitched.append(char)

        print("".join(glitched), end="\r")
        time.sleep(delay)

    print(text)


def typing_effect(text: str, delay: float = 0.04, newline: bool = True):
    """Simulate typing effect."""
    # import asyncio
    # ToDo: Implement asyncio-based typing effect for non-blocking delays
    for char in text:
        sys.stdout.write(char)
        sys.stdout.flush()
        time.sleep(delay)

    if newline:
        sys.stdout.write("\n")
        sys.stdout.flush()


def loading_sequence():
    """Enhanced loading sequence with progress indicators."""
    PROGRESS_BAR_LENGTH = 20  # Define constant for progress bar length
    for i, message in enumerate(LOADING_MESSAGES):
        progress = int((i + 1) / len(LOADING_MESSAGES) * PROGRESS_BAR_LENGTH)
        bar = "█" * progress + "░" * (PROGRESS_BAR_LENGTH - progress)

        typing_effect(f"{Colors.YELLOW}[{bar}] {message}{Colors.RESET}", delay=0.02)
        time.sleep(0.5)


def animated_prompt():
    """Create an animated prompt with pulsing effect."""
    prompt_text = "Press [Enter] to launch BanditGUI"
    duration = 5.4  # Total animation duration in seconds
    start_time = time.time()

    while time.time() - start_time < duration:
        elapsed = time.time() - start_time
        cycle = int(elapsed / 1.8) % 3
        intensity = int((elapsed % 1.8) / 0.6)

        if intensity == 0:
            color = Colors.DIM + Colors.GREEN
        elif intensity == 1:
            color = Colors.GREEN
        else:
            color = Colors.BOLD + Colors.GREEN

        sys.stdout.write(f"\r{color}>> {prompt_text}{Colors.RESET}")
        sys.stdout.flush()
        time.sleep(0.1)

    # Final fade out
    sys.stdout.write(f"\r{Colors.DIM}>> {prompt_text}{Colors.RESET}")
    sys.stdout.flush()


def show_enhanced_banner():
    """Display the enhanced banner with effects."""
    clear_screen()

    # Matrix effect for the banner
    print(Colors.BOLD + Colors.GREEN)
    matrix_effect(BANDIT_TITLE, duration=1.5)
    print(Colors.RESET)

    time.sleep(0.5)

    # Glitch effect for subtitle
    print(Colors.CYAN + Colors.BOLD)
    glitch_effect(center_text(SUBTITLE), glitch_times=3, delay=0.1)
    print(Colors.RESET)

    time.sleep(0.3)

    # Separator line
    width = get_terminal_width()
    separator = "═" * min(60, width - 10)
    print(center_text(Colors.BLUE + separator + Colors.RESET))

    time.sleep(0.5)


def display_system_info():
    """Display system information and status."""
    # Define color constants for improved readability and maintainability
    STATUS_COLOR = Colors.CYAN
    CHECK_COLOR = Colors.GREEN
    READY_COLOR = Colors.YELLOW

    info_lines = [
        f"{STATUS_COLOR}System Status:{Colors.RESET}",
        f"  {CHECK_COLOR}✓{Colors.RESET} Terminal Interface: Ready",
        f"  {CHECK_COLOR}✓{Colors.RESET} SSH Client: Initialized",
        f"  {CHECK_COLOR}✓{Colors.RESET} Security Protocols: Active",
        f"  {CHECK_COLOR}✓{Colors.RESET} Web Terminal: Loaded",
        "",
        f"{READY_COLOR}Ready to connect to OverTheWire Bandit levels!{Colors.RESET}",
    ]

    for line in info_lines:
        print(center_text(line))


def display_credits():
    """Display credits with fade-in effect."""
    print()
    typing_effect(center_text(f"{Colors.DIM}{CREDITS}{Colors.RESET}"), delay=0.01)


def run_title_sequence():
    """Run the complete title sequence."""
    try:
        show_enhanced_banner()
        loading_sequence()
        print()
        display_system_info()
        display_credits()
        print()

        # Animated prompt
        animated_prompt()

        # Wait for user input
        sys.stdout.write(f"{Colors.BOLD}{Colors.GREEN}>> {Colors.RESET}")
        sys.stdout.flush()

        input()  # Wait for Enter

        # Exit message
        print(f"\n{Colors.CYAN}Launching BanditGUI...{Colors.RESET}")
        time.sleep(1)
        print("BANDIT TITLE SCREEN LOADED")  # Unique marker for E2E test

    except KeyboardInterrupt:
        print(f"\n\n{Colors.RED}Interrupted by user. Exiting...{Colors.RESET}")
        sys.exit(0)
    except (ValueError, TypeError, AttributeError) as e:
        print(f"\n{Colors.RED}Error: {e}{Colors.RESET}")
        sys.exit(1)


def main():
    """Main entry point."""
    run_title_sequence()


if __name__ == "__main__":
    main()
