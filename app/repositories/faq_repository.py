
from app.schemas import FAQResponse

# TODO: Implement the methods for FAQRepository
class FaqRepository:
    def __init__(self):
        pass

    def get_all_faqs(self) -> list[FAQResponse]:
        pass

    def add_faq(self, question: str, answer: str) -> None:
        pass

    def delete_faq(self, faq_id: int) -> None:
        pass

    def update_faq(self, faq_id: int, question: str, answer: str) -> None:
        pass