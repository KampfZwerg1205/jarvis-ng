from __future__ import annotations

from jarvis.ai.router import AIRouter
from jarvis.conversation.history import ConversationHistory
from jarvis.skills.router import SkillRouter
from jarvis.skills.registry import SkillRegistry
from jarvis.system.actions import SystemActions


class ConversationManager:
    """Verwaltet Gespräche und sichere Systembestätigungen."""

    def __init__(self, router: AIRouter):
        self.router = router
        self.history = ConversationHistory()

        self.skills = SkillRouter()

        registry = SkillRegistry()
        registry.load_defaults()

        for skill in registry.all():
            self.skills.register(skill)

        # Wartet auf eine Bestätigung für eine gefährliche Aktion.
        self.pending_action: str | None = None

    def chat(self, prompt: str) -> str:
        prompt = prompt.strip()

        # ---------------------------------------------------------
        # Ausstehende Sicherheitsbestätigung
        # ---------------------------------------------------------

        if self.pending_action is not None:
            answer = self._handle_confirmation(prompt)

            self.history.add_user(prompt)
            self.history.add_assistant(answer)

            return answer

        self.history.add_user(prompt)

        # ---------------------------------------------------------
        # Normale Skills
        # ---------------------------------------------------------

        skill = self.skills.find(prompt)

        if skill is not None:
            # Gefährliche Aktionen zunächst nur bestätigen lassen.
            if skill.name == "system_actions":
                normalized = prompt.lower().strip()

                if self._is_shutdown_command(normalized):
                    self.pending_action = "shutdown"
                    answer = (
                        "Sir, soll ich den PC wirklich herunterfahren? "
                        "(Ja/Nein)"
                    )

                    self.history.add_assistant(answer)
                    return answer

                if self._is_restart_command(normalized):
                    self.pending_action = "restart"
                    answer = (
                        "Sir, soll ich den PC wirklich neu starten? "
                        "(Ja/Nein)"
                    )

                    self.history.add_assistant(answer)
                    return answer

            answer = skill.execute(prompt)

            self.history.add_assistant(answer)

            return answer

        # ---------------------------------------------------------
        # KI
        # ---------------------------------------------------------

        conversation = self.history.as_text()
        answer = self.router.chat(conversation)

        self.history.add_assistant(answer)

        return answer

    def _handle_confirmation(self, prompt: str) -> str:
        """Verarbeitet die Antwort auf eine Sicherheitsabfrage."""

        answer = prompt.lower().strip()

        yes_words = (
            "ja",
            "j",
            "ja bitte",
            "bestätigt",
            "bestätige",
        )

        no_words = (
            "nein",
            "n",
            "abbrechen",
            "abbruch",
            "stopp",
            "stop",
        )

        # ---------------------------------------------------------
        # Ablehnung
        # ---------------------------------------------------------

        if answer in no_words:
            self.pending_action = None
            return "Verstanden. Der Vorgang wurde abgebrochen."

        # ---------------------------------------------------------
        # Bestätigung
        # ---------------------------------------------------------

        if answer in yes_words:
            action = self.pending_action
            self.pending_action = None

            if action == "shutdown":
                if SystemActions.shutdown_pc():
                    return "Der PC wird jetzt heruntergefahren."

                return "Der PC konnte nicht heruntergefahren werden."

            if action == "restart":
                if SystemActions.restart_pc():
                    return "Der PC wird jetzt neu gestartet."

                return "Der PC konnte nicht neu gestartet werden."

        # ---------------------------------------------------------
        # Unklare Antwort
        # ---------------------------------------------------------

        return "Bitte antworten Sie mit „Ja“ oder „Nein“."

    @staticmethod
    def _is_shutdown_command(prompt: str) -> bool:
        """Erkennt Befehle zum Herunterfahren."""

        commands = (
            "fahre meinen pc herunter",
            "fahr meinen pc herunter",
            "fahre den pc herunter",
            "fahr den pc herunter",
            "fahre meinen computer herunter",
            "fahr meinen computer herunter",
            "pc herunterfahren",
            "computer herunterfahren",
            "herunterfahren",
        )

        return any(command in prompt for command in commands)

    @staticmethod
    def _is_restart_command(prompt: str) -> bool:
        """Erkennt Befehle zum Neustarten."""

        commands = (
            "starte meinen pc neu",
            "starte den pc neu",
            "starte meinen computer neu",
            "starte den computer neu",
            "pc neu starten",
            "computer neu starten",
            "pc neustarten",
            "computer neustarten",
        )

        return any(command in prompt for command in commands)