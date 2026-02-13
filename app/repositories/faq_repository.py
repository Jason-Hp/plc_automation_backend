from app.schemas import FAQ

class FaqRepository:
    def __init__(self):
        self._faqs: list[FAQ] = []
        self._next_id = 1

    def get_all_faqs(self) -> list[FAQ]:
        return self._faqs

    def add_faq(self, question: str, answer: str) -> None:
        self._faqs.append(FAQ(id=self._next_id, question=question, answer=answer))
        self._next_id += 1

    def delete_faq(self, faq_id: int) -> None:
        self._faqs = [faq for faq in self._faqs if faq.id != faq_id]

    def update_faq(self, faq_id: int, question: str, answer: str) -> None:
        for idx, faq in enumerate(self._faqs):
            if faq.id == faq_id:
                self._faqs[idx] = FAQ(id=faq_id, question=question, answer=answer)
                return
