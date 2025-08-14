"""
Mock data service for testing the bot
"""
from datetime import datetime
from typing import List

class CargoListing:
    def __init__(self, id: str, origin: str, destination: str, cargo_type: str, 
                 weight: str = None, price: str = None, contact: str = None, 
                 description: str = None):
        self.id = id
        self.origin = origin
        self.destination = destination
        self.cargo_type = cargo_type
        self.weight = weight
        self.price = price
        self.contact = contact
        self.description = description
        self.date_posted = datetime.now()

class DataService:
    """Simple data service for demo purposes"""
    
    def __init__(self):
        self._cargo_listings = [
            CargoListing("1", "Toshkent", "Samarqand", "Oziq-ovqat", "5 tonna", "2 000 000 so'm", "+998901234567", "Tez yetkazish kerak"),
            CargoListing("2", "Buxoro", "Nukus", "Qurilish materiallari", "10 tonna", "3 500 000 so'm", "+998907654321", "Poyezd stantsiyasiga yetkazish"),
            CargoListing("3", "Andijon", "Toshkent", "Meva-sabzavot", "3 tonna", "1 500 000 so'm", "+998909876543", "Sovuq transport kerak"),
        ]
    
    async def get_cargo_listings(self) -> List[CargoListing]:
        """Get all cargo listings"""
        return self._cargo_listings
    
    async def search_cargo(self, query: str) -> List[CargoListing]:
        """Search cargo listings by query"""
        if not query:
            return self._cargo_listings
        
        query = query.lower()
        results = []
        
        for listing in self._cargo_listings:
            if (query in listing.origin.lower() or 
                query in listing.destination.lower() or 
                query in listing.cargo_type.lower()):
                results.append(listing)
        
        return results

# Global instance
data_service = DataService()
