from enum import Enum


class TargetedPart(Enum):
    """Supported document areas for candidate extraction.

    :cvar HEADER: Top lines of each page.
    :cvar FOOTER: Bottom lines of each page.
    """

    HEADER = 1
    FOOTER = 2
