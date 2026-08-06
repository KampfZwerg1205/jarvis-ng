from __future__ import annotations

from jarvis.ai.router import AIRouter
from jarvis.conversation.history import ConversationHistory


class ConversationManager:

    def __init__(self, router: AIRouter):
        self.router = router
        self.history = ConversationHistory()

    def chat(self, prompt: str) -> str:
        self.history.add_user(prompt)

        conversation = self.history.as_text()

        answer = self.router.chat(conversation)

        self.history.add_assistant(answer)

        return answer