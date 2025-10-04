import os
import re
import requests
import logging
from bs4 import BeautifulSoup
from typing import Dict, List, Optional
from collections import Counter
from urllib.parse import urljoin

logger = logging.getLogger(__name__)


class BrandService:
    """Production-grade service for extracting branding elements from websites"""

    def __init__(self):
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def _extract_logo(self, soup: BeautifulSoup, base_url: str) -> Optional[str]:
        """Try to find the company logo"""
        selectors = [
            'img[alt*="logo" i]',
            'img[class*="logo" i]',
            'img[id*="logo" i]',
            '.logo img',
            '#logo img'
        ]

        for selector in selectors:
            img = soup.select_one(selector)
            if img and img.get('src'):
                return urljoin(base_url, img['src'])

        return None

    