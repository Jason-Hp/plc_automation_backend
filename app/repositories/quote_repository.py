from __future__ import annotations

from app.schemas import Quote, QuoteListResponse

class QuoteRepository:

    # 1 table for quote and 1 JOIN table with product (using product and quote id)
    def __init__(self):
        pass

    def get_all_quotes(self, search: str, page: int, per_page: int) -> QuoteListResponse:
        # rmb to use join table
        # use pagination here, if empty search return all, search is used to match with names or cpmany or email or phone number etc
        pass

    def get_quote_by_id(self, id: int) -> Quote:
        # rmb to use join table
        pass

    def add_quote(self, quote: Quote) -> int:
        # Break quote object into 
        # actual persistence/entity quote which is id, ispaid, total amount, and everything in enquiryrequests schema
        # add that into quote repo/entity
        # then retrieve the product preview with quantity list from quote
        # for each product, get the id and quantity right, then add it in the JOIN table QUOTES_PRODUCTS
        # add the quote id, product id and quantity
        # return quote entity id
        pass

    def update_quote(self, id: int, quote: Quote) -> None:
        # rmb to use join table
        pass

    def delete_quote(self, id: int) -> None:
        # rmb to use join table
        pass
    
    # Join Table stuff
    def add_products_to_quote(self, quote_id: int, product_ids: list[int]) -> None:
        pass

    def delete_all_products_from_quote(self, quote_id: int) -> None:
        #Delete all entires in the JOIN TABLE with quote id
        pass

    def update_products_to_quote(self, quote_id: int, product_ids: list[int]) -> None:
        self.delete_all_products_from_quote(quote_id)
        self.add_products_to_quote(quote_id, product_ids)