from __future__ import annotations

from jarvis.ai.router import AIRouter
from jarvis.conversation.history import ConversationHistory
from jarvis.skills.router import SkillRouter
from jarvis.skills.registry import SkillRegistry


class ConversationManager:

    def __init__(self, router: AIRouter):
        self.router = router
        self.history = ConversationHistory()

        self.skills = SkillRouter()

        registry = SkillRegistry()
        registry.load_defaults()

        for skill in registry.all():
            self.skills.register(skill)

    def chat(self, prompt: str) -> str:
        self.history.add_user(prompt)

        skill_answer = self.skills.execute(prompt)

        if skill_answer is not None:
            answer = skill_answer
        else:
            conversation = self.history.as_text()
            answer = self.router.chat(conversation)

        self.history.add_assistant(answer)

        return answer