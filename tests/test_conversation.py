from jarvis.conversation.history import ConversationHistory


def test_conversation_history() -> None:
    history = ConversationHistory()

    history.add_user("Hallo")
    history.add_assistant("Hi!")

    assert len(history.messages) == 2
    assert history.messages[0].role == "user"
    assert history.messages[1].role == "assistant"

    history.clear()

    assert len(history.messages) == 0