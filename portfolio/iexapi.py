from django.conf import settings
import requests



IEX_TOKEN_PROD="pk_1a377aa6e6084f44a5dab630c1faec47"
IEX_TOKEN_TEST="Tpk_eee555b376514b31a382376fe44bac4a"
PROD_URL = "https://cloud.iexapis.com/v1"
TEST_URL = "https://sandbox.iexapis.com/stable"

class IEXAPI():
    def __init__(self):
        self.token = IEX_TOKEN_PROD
        self.prefix = PROD_URL
        self.session = requests.Session()
        
    def get_company_quote(self,symbol):
        """
        Get realtime or delayed qoute for defined symbol
        Returns: JSON
        """
        end_point = f"/stock/{symbol}/quote"
        url = self.prefix + end_point+"?token="+self.token
        response = self.session.get(url)
        data = response.json()
        return data
    
    def get_quote_field(self,symbol,field):
        """
        Get only Last price defined symbol
        Returns: JSON
        """
        end_point = f"/stock/{symbol}/quote/{field}"
        url = self.prefix + end_point+"?token="+self.token
        response = self.session.get(url)
        data = response.json()
        return data
    
    def get_previous_day(self,symbol):
        """
        Get insider transactions for defined symbol
        Returns: JSON
        """
        end_point = f"/stock/{symbol}/previous"
        url = self.prefix + end_point+"?token="+self.token
        response = self.session.get(url)
        data = response.json()
        return data
    
    def get_company_profile(self,symbol):
        """
        Get realtime or delayed qoute for defined symbol
        Returns: JSON
        """
        end_point = f"/stock/{symbol}/company"
        url = self.prefix + end_point+"?token="+self.token
        response = self.session.get(url)
        data = response.json()
        return data
    
    def get_list(self, list):
        """
        Get realtime or delayed most active symbols
        list option = (mostactive, gainers,
        losers,iexvolume,iexpercent,premarket_losers,
        postmarket_loseres, premaeket_gainers,postmarket_gainers)
        Returns: JSON
        """
        end_point = f"/stock/market/list/{list}"
        url = self.prefix + end_point+"?token="+self.token
        response = self.session.get(url)
        data = response.json()
        return data
    
    
    def get_basic_stats(self,symbol):
        """
        Get basic stats for defined symbol
        Returns: JSON
        """
        end_point = f"/stock/{symbol}/stats"
        url = self.prefix + end_point+"?token="+self.token
        response = self.session.get(url)
        data = response.json()
        return data
    
    def get_advanced_stats(self,symbol):
        """
        Get advanced stats for defined symbol
        Returns: JSON
        """
        end_point = f"/stock/{symbol}/advanced-stats"
        url = self.prefix + end_point+"?token="+self.token
        response = self.session.get(url)
        data = response.json()
        return data
    
    def get_insider_trans(self,symbol):
        """
        Get insider transactions for defined symbol
        Returns: JSON
        """
        end_point = f"/stock/{symbol}/insider-transactions"
        url = self.prefix + end_point+"?token="+self.token
        response = self.session.get(url)
        data = response.json()
        return data
    
    def get_dividends(self,symbol):
        """
        Get insider transactions for defined symbol
        Returns: JSON
        """
        end_point = f"/stock/{symbol}/dividends/5y"
        url = self.prefix + end_point+"?token="+self.token
        response = self.session.get(url)
        data = response.json()
        return data
    
    def get_last_only(self,symbol):
        """
        Get only Last price defined symbol
        Returns: JSON
        """
        end_point = f"/stock/{symbol}/price"
        url = self.prefix + end_point+"?token="+self.token
        response = self.session.get(url)
        data = response.json()
        return data
    
    def get_sector_performance(self):
        """
        Get only Last price defined symbol
        Returns: JSON
        """
        end_point = f"/stock/market/sector-performance"
        url = self.prefix + end_point+"?token="+self.token
        response = self.session.get(url)
        data = response.json()
        return data
    
    
    def get_company_logo(self,symbol):
        """
        Get url of company symbol
        Returns: JSON
        """
        end_point = f"/stock/{symbol}/logo"
        url = self.prefix + end_point+"?token="+self.token
        response = self.session.get(url)
        data = response.json()
        return data
    
    def get_company_last_news(self,symbol):
        """
        Get url of company symbol
        Returns: JSON
        """
        end_point = f"/data/core/news/{symbol}"
        url = self.prefix + end_point+"?limit=5&token="+self.token
        response = self.session.get(url)
        data = response.json()
        return data
    
    
