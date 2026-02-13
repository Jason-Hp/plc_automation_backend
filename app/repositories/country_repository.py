from app.schemas import Country, Product

class CountryRepository:

    def __init__(self):
        self._countries: list[Country] = []

    def get_all_countries(self) -> list[Country]:
        return self._countries

    def get_country_by_id(self, country_id: int) -> Country | None:
        for country in self._countries:
            if country.id == country_id:
                return country
            
    def get_country_by_code(self, code: str) -> Country | None:
        for country in self._countries:
            if country.code.lower() == code.lower():
                return country
        return None
    
    def get_country_by_name(self, name: str) -> Country | None:
        for country in self._countries:
            if country.name.lower() == name.lower():
                return country
        return None
    
    def add_country(self, country: Country) -> None:
        self._countries.append(country)

    def update_country(self, country_id: int, country: Country) -> None:
        for index, current in enumerate(self._countries):
            if current.id == country_id:
                self._countries[index] = country
                return
            
    def delete_country(self, country_id: int) -> None:
        self._countries = [country for country in self._countries if country.id != country_id]

    def get_product_availability_by_country(self, country_id: int, product_id: int) -> bool:
        #TODO: A join table for availability, containing country_id and product_id to determine availability (one(product) to many(countries))
        pass

    def add_product_availability_for_country(self, country_ids: list[int], product_id: int) -> None:
        pass

    def delete_all_product_availability_for_country(product_id: int) -> None:
        pass

    def update_product_availability_for_country(self, country_ids: list[int], product_id: int) -> None:
        delete_all_product_availability_for_country(product_id)
        add_product_availability_for_country(country_ids, product_id)
