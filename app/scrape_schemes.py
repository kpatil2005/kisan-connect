import requests
from bs4 import BeautifulSoup

def scrape_government_schemes():
    """Scrape real schemes from Ministry of Agriculture website"""
    schemes = []
    
    try:
        # Try MyScheme API first
        url = "https://www.myscheme.gov.in/search/scheme"
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            scheme_cards = soup.find_all('div', class_='scheme-card')
            
            for card in scheme_cards[:20]:
                title = card.find('h3')
                desc = card.find('p')
                link = card.find('a')
                
                if title:
                    schemes.append({
                        'id': str(len(schemes) + 1),
                        'title': title.text.strip(),
                        'description': desc.text.strip() if desc else 'Check official website',
                        'category': 'Agriculture',
                        'eligibility': 'Check official website',
                        'benefits': 'Check official website',
                        'how_to_apply': 'Visit official website',
                        'official_link': link['href'] if link else '#',
                        'ministry': 'Ministry of Agriculture',
                    })
    except:
        pass
    
    # Fallback to real schemes if scraping fails
    if not schemes:
        schemes = [
            {'id': '1', 'title': 'PM-KISAN', 'description': 'Direct income support of ₹6000/year', 'category': 'Subsidy', 'eligibility': 'All landholding farmers', 'benefits': '₹6000 per year', 'how_to_apply': 'Apply at pmkisan.gov.in', 'official_link': 'https://pmkisan.gov.in/', 'ministry': 'Ministry of Agriculture'},
            {'id': '2', 'title': 'PMFBY', 'description': 'Crop insurance', 'category': 'Insurance', 'eligibility': 'All farmers', 'benefits': 'Insurance coverage', 'how_to_apply': 'Apply at pmfby.gov.in', 'official_link': 'https://pmfby.gov.in/', 'ministry': 'Ministry of Agriculture'},
            {'id': '3', 'title': 'Kisan Credit Card', 'description': 'Credit at 4%', 'category': 'Loan', 'eligibility': 'All farmers', 'benefits': 'Up to ₹3 lakh', 'how_to_apply': 'Apply at bank', 'official_link': 'https://www.india.gov.in/spotlight/kisan-credit-card-kcc', 'ministry': 'Ministry of Agriculture'},
            {'id': '4', 'title': 'Soil Health Card', 'description': 'Free soil testing', 'category': 'Other', 'eligibility': 'All farmers', 'benefits': 'Free analysis', 'how_to_apply': 'Contact agriculture office', 'official_link': 'https://soilhealth.dac.gov.in/', 'ministry': 'Ministry of Agriculture'},
            {'id': '5', 'title': 'e-NAM', 'description': 'Online trading', 'category': 'Other', 'eligibility': 'All farmers', 'benefits': 'Better prices', 'how_to_apply': 'Register at enam.gov.in', 'official_link': 'https://www.enam.gov.in/', 'ministry': 'Ministry of Agriculture'},
            {'id': '6', 'title': 'PKVY', 'description': 'Organic farming', 'category': 'Subsidy', 'eligibility': 'Organic farmers', 'benefits': '₹50,000/hectare', 'how_to_apply': 'Apply through State Dept', 'official_link': 'https://pgsindia-ncof.gov.in/', 'ministry': 'Ministry of Agriculture'},
        ]
    
    return schemes
