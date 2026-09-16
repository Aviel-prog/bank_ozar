"""The interactive menu: one option per action, rendered from a single dict."""

from dataclasses import dataclass

TITLE = "BANK OZAR CORE SERVICES"
PROMPT = "Command > "


@dataclass(frozen=True)
class MenuOption:
    """One selectable action: the name the user types about, and what it does."""

    label: str
    description: str


# The single source of truth for the menu. The keys are the choices the api
# dispatches on, so a new option cannot appear on screen without a route
# behind it, or the other way around.
MENU_OPTIONS: dict[str, MenuOption] = {
    "1": MenuOption("balance", "View current funds"),
    "2": MenuOption("deposit", "Add funds"),
    "3": MenuOption("withdraw", "Get cash"),
    "4": MenuOption("sub:add", "New recurring payment"),
    "5": MenuOption("sub:remove", "Cancel subscription"),
    "6": MenuOption("sub:list", "View subscriptions"),
    "7": MenuOption("balance:next day", "Project the next pay day"),
    "8": MenuOption("purge", "Close account"),
    "9": MenuOption("exit", "Terminate session"),
}


def render_menu() -> str:
    """Builds the menu box by iterating the options, so it never drifts."""
    label_width = max(len(option.label) for option in MENU_OPTIONS.values())
    description_width = max(len(option.description) for option in MENU_OPTIONS.values())

    rows = [
        f"   [{key}] {option.label:<{label_width}} \u2500\u2500 {option.description:<{description_width}}"
        for key, option in MENU_OPTIONS.items()
    ]
    inner_width = max(len(row) for row in rows) + 3

    header = f"[ {TITLE} ]".center(inner_width, "\u2500")
    lines = [f"\u250c{header}\u2510", f"\u2502{'':<{inner_width}}\u2502"]
    lines += [f"\u2502{row:<{inner_width}}\u2502" for row in rows]
    lines += [f"\u2502{'':<{inner_width}}\u2502", f"\u2514{'\u2500' * inner_width}\u2518"]

    return "\n" + "\n".join(lines) + "\n" + PROMPT
