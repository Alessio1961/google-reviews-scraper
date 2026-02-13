"""
Google Maps Reviews Scraper
Modulo per lo scraping delle recensioni da Google Maps
"""

import time
from typing import List, Dict, Optional
from playwright.sync_api import sync_playwright, Page, TimeoutError as PlaywrightTimeout


class Review:
    """Rappresenta una recensione di Google Maps"""
    
    def __init__(self, reviewer_name: str, stars: int, text: str, date: str,
                 owner_response: str = "", response_date: str = ""):
        self.reviewer_name = reviewer_name
        self.stars = stars
        self.text = text
        self.date = date
        self.owner_response = owner_response
        self.response_date = response_date
    
    def to_dict(self) -> Dict:
        """Converte la recensione in dizionario"""
        return {
            'reviewer_name': self.reviewer_name,
            'stars': self.stars,
            'text': self.text,
            'date': self.date,
            'owner_response': self.owner_response,
            'response_date': self.response_date
        }


class GoogleReviewsScraper:
    """Scraper per recensioni di Google Maps"""
    
    def __init__(self, url: str, stars_filter: Optional[int] = None):
        self.url = url
        self.stars_filter = stars_filter
        self.reviews: List[Review] = []
    
    def _scroll_reviews(self, page: Page, reviews_container) -> None:
        """Scrolla il contenitore delle recensioni per caricarle tutte"""
        print("🔄 Caricamento recensioni in corso...")
        
        last_height = 0
        no_change_count = 0
        max_no_change = 3
        
        while no_change_count < max_no_change:
            try:
                # Scrolla fino in fondo al contenitore
                page.evaluate("""(element) => {
                    element.scrollTop = element.scrollHeight;
                }""", reviews_container)
                
                time.sleep(2)
                
                # Controlla se ci sono nuove recensioni
                current_height = page.evaluate("(element) => element.scrollHeight", reviews_container)
                
                if current_height == last_height:
                    no_change_count += 1
                else:
                    no_change_count = 0
                    last_height = current_height
                
                # Mostra progresso
                review_elements = reviews_container.query_selector_all('[data-review-id]')
                print(f"   Recensioni caricate: {len(review_elements)}", end='\r')
                
            except Exception as e:
                print(f"\n⚠️  Errore durante lo scroll: {e}")
                break
        
        print()  # Nuova linea dopo il progresso
    
    def _extract_stars(self, review_element) -> int:
        """Estrae il numero di stelle da una recensione"""
        try:
            # Cerca l'attributo aria-label con "stelle" o "star"
            stars_element = review_element.query_selector('[role="img"]')
            if stars_element:
                aria_label = stars_element.get_attribute('aria-label')
                if aria_label:
                    # Estrae il numero dalle varie lingue (es: "5 stelle", "5 stars")
                    for i in range(1, 6):
                        if str(i) in aria_label:
                            return i
        except:
            pass
        return 0
    
    def _click_more_buttons(self, page: Page) -> None:
        """Clicca su tutti i pulsanti 'Altro' per espandere i testi completi"""
        try:
            more_buttons = page.query_selector_all('button[aria-label*="Altro"], button.w8nwRe')
            print(f"🔍 Espansione di {len(more_buttons)} recensioni lunghe...")
            
            for button in more_buttons:
                try:
                    if button.is_visible():
                        button.click()
                        time.sleep(0.1)
                except:
                    continue
        except Exception as e:
            print(f"⚠️  Errore durante l'espansione: {e}")
    
    def _extract_review_data(self, review_element) -> Optional[Review]:
        """Estrae i dati da un singolo elemento recensione"""
        try:
            # Nome recensore
            reviewer_name = ""
            name_element = review_element.query_selector('.d4r55')
            if name_element:
                reviewer_name = name_element.inner_text().strip()
            
            # Stelle
            stars = self._extract_stars(review_element)
            
            # Testo recensione
            text = ""
            text_element = review_element.query_selector('.wiI7pd, .MyEned')
            if text_element:
                text = text_element.inner_text().strip()
            
            # Data
            date = ""
            date_element = review_element.query_selector('.rsqaWe')
            if date_element:
                date = date_element.inner_text().strip()
            
            # Risposta proprietario
            owner_response = ""
            response_date = ""
            response_element = review_element.query_selector('.CDe7pd')
            if response_element:
                response_text_element = response_element.query_selector('.wiI7pd')
                if response_text_element:
                    owner_response = response_text_element.inner_text().strip()
                
                response_date_element = response_element.query_selector('.rsqaWe')
                if response_date_element:
                    response_date = response_date_element.inner_text().strip()
            
            return Review(
                reviewer_name=reviewer_name,
                stars=stars,
                text=text,
                date=date,
                owner_response=owner_response,
                response_date=response_date
            )
        except Exception as e:
            print(f"⚠️  Errore nell'estrazione recensione: {e}")
            return None
    
    def scrape(self) -> List[Review]:
        """Esegue lo scraping delle recensioni"""
        print(f"🚀 Avvio scraping da: {self.url}")
        if self.stars_filter:
            print(f"⭐ Filtro stelle: {self.stars_filter}")
        
        with sync_playwright() as p:
            # Avvia browser
            browser = p.chromium.launch(headless=True)
            context = browser.new_context(
                user_agent='Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
            )
            page = context.new_page()
            
            try:
                # Naviga alla pagina
                print("🌐 Caricamento pagina Google Maps...")
                page.goto(self.url, wait_until='networkidle', timeout=30000)
                time.sleep(3)
                
                # Trova e clicca sul tab delle recensioni
                try:
                    reviews_tab = page.wait_for_selector(
                        'button[aria-label*="Recensioni"], button.hh2c6',
                        timeout=10000
                    )
                    if reviews_tab:
                        reviews_tab.click()
                        time.sleep(2)
                except PlaywrightTimeout:
                    print("⚠️  Tab recensioni non trovato, continuo comunque...")
                
                # Trova il contenitore scrollabile delle recensioni
                reviews_container = page.wait_for_selector(
                    '.m6QErb[aria-label*="Recensioni"], .m6QErb.DxyBCb',
                    timeout=10000
                )
                
                if not reviews_container:
                    print("❌ Contenitore recensioni non trovato")
                    return []
                
                # Scrolla per caricare tutte le recensioni
                self._scroll_reviews(page, reviews_container)
                
                # Espandi tutti i testi completi
                self._click_more_buttons(page)
                time.sleep(1)
                
                # Estrai tutte le recensioni
                print("📊 Estrazione dati recensioni...")
                review_elements = reviews_container.query_selector_all('[data-review-id]')
                
                for i, review_element in enumerate(review_elements, 1):
                    review = self._extract_review_data(review_element)
                    
                    if review:
                        # Applica filtro stelle se specificato
                        if self.stars_filter is None or review.stars == self.stars_filter:
                            self.reviews.append(review)
                    
                    # Mostra progresso
                    if i % 10 == 0:
                        print(f"   Processate: {i}/{len(review_elements)}", end='\r')
                
                print(f"\n✅ Estrazione completata: {len(self.reviews)} recensioni trovate")
                
            except Exception as e:
                print(f"❌ Errore durante lo scraping: {e}")
                import traceback
                traceback.print_exc()
            finally:
                browser.close()
        
        return self.reviews
    
    def get_reviews_as_dicts(self) -> List[Dict]:
        """Restituisce le recensioni come lista di dizionari"""
        return [review.to_dict() for review in self.reviews]
