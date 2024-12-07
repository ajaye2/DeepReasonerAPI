import requests
from typing import Dict, Any, Optional
from urllib.parse import urljoin

class DeepReasonerClient:
    """Client for interacting with the DeepReasoner API."""
    
    def __init__(
        self, 
        api_key: str,
        base_url: str = "https://deepreasoner.azure-api.net",
        api_version: str = "/",
        timeout: int = 30
    ):
        """
        Initialize the DeepReasoner API client.
        
        Args:
            api_key (str): The API key for authentication
            base_url (str): Base URL for the API
            api_version (str): API version path
            timeout (int): Request timeout in seconds
        """
        self.base_url = base_url.rstrip('/')
        self.api_version = api_version.strip('/')
        self.timeout = timeout
        self.session = requests.Session()
        self.session.headers.update({
            'Api-Subscription-Key': f'{api_key}',
            'Content-Type': 'application/json',
        })

    def _build_url(self, endpoint: str) -> str:
        """Construct the full URL for an API endpoint."""
        if self.api_version:
            return urljoin(f"{self.base_url}/{self.api_version}/", endpoint.lstrip('/'))
        return urljoin(f"{self.base_url}/", endpoint.lstrip('/'))

    def _make_request(
        self,
        method: str,
        endpoint: str,
        params: Optional[Dict[str, Any]] = None,
        json_data: Optional[Dict[str, Any]] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """
        Make an HTTP request to the API.
        
        Args:
            method (str): HTTP method (GET, POST, etc.)
            endpoint (str): API endpoint
            params (dict, optional): Query parameters
            json_data (dict, optional): JSON body data
            **kwargs: Additional arguments to pass to requests
            
        Returns:
            dict: API response data
            
        Raises:
            requests.exceptions.RequestException: If the request fails
        """
        url = self._build_url(endpoint)
        
        response = self.session.request(
            method=method,
            url=url,
            params=params,
            json=json_data,
            timeout=self.timeout,
            **kwargs
        )
        
        response.raise_for_status()
        return response.json()

    def get(self, endpoint: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """Make a GET request to the API."""
        return self._make_request('GET', endpoint, params=params)

    def post(self, endpoint: str, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a POST request to the API."""
        return self._make_request('POST', endpoint, json_data=json_data)

    def put(self, endpoint: str, json_data: Dict[str, Any]) -> Dict[str, Any]:
        """Make a PUT request to the API."""
        return self._make_request('PUT', endpoint, json_data=json_data)

    def delete(self, endpoint: str) -> Dict[str, Any]:
        """Make a DELETE request to the API."""
        return self._make_request('DELETE', endpoint)

    def check_health(self) -> Dict[str, Any]:
        """Check the health of the API."""
        return self.get('/')

    # Add specific API methods here, for example:
    def reason(self, 
                     prompt: str, 
                     reasoning_algorithm: str,
                     temperature: float = 0.7
                     ) -> Dict[str, Any]:
        """
        Reason about text using the DeepReasoner API.
        
        Args:
            prompt (str): The prompt to reason about
            reasoning_algorithm (str): The reasoning algorithm to use
            temperature (float): The temperature for the reasoning algorithm
            
        Returns:
            dict: Reasoning results
        """
        return self.post('/reason', {'prompt': prompt, 'temperature': temperature, 'algorithm': reasoning_algorithm}) 