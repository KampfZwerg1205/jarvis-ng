from __future__ import annotations

from jarvis.conversation.message import Message


class ConversationHistory:
    """Speichert den aktuellen Gesprächsverlauf."""

    def __init__(self) -> None:
        self._messages: list[Message] = []

    def add(self, role: str, content: str) -> None:
        self._messages.append(Message(role, content))

    def add_user(self, content: str) -> None:
        self.add("user", content)

    def add_assistant(self, content: str) -> None:
        self.add("assistant", content)

    def clear(self) -> None:
        self._messages.clear()

    @property
    def messages(self) -> list[Message]:
        return list(self._messages)

    def as_dicts(self) -> list[dict[str, str]]:
        return [message.to_dict() for message in self._messages]

    def as_text(self) -> str:
        """Gibt den Gesprächsverlauf als formatierten Text zurück."""

        lines: list[str] = []

        for message in self._messages:
            role = "Benutzer" if message.role == "user" else "JARVIS"
            lines.append(f"{role}: {message.content}")

        return "\n".join(lines)