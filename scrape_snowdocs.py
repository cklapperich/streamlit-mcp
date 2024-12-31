import requests
from bs4 import BeautifulSoup
import os
import time
from urllib.parse import urljoin, urlparse
import json
from concurrent.futures import ThreadPoolExecutor

class SnowflakeDocsScraper:
    def __init__(self, base_url='https://docs.snowflake.com'):
        self.base_url = base_url
        self.visited_urls = set()  # Track visited URLs
        self.queued_urls = set()   # Track URLs in queue to prevent duplicates
        self.failed_urls = set()
        self.domain = 'docs.snowflake.com'  # Strict domain matching
        
        # Create directory for saving pages
        self.output_dir = 'snowflake_docs'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Common headers to mimic a browser
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8',
            'Accept-Language': 'en-US,en;q=0.5',
        }

    def is_valid_url(self, url):
        """Check if URL is valid for scraping."""
        parsed = urlparse(url)
        
        # Check if URL is already visited or queued
        if url in self.visited_urls or url in self.queued_urls:
            return False
            
        # Ensure URL is from the correct domain
        if parsed.netloc != self.domain:
            return False
            
        # Skip release notes
        if '/release-notes/' in parsed.path:
            return False
            
        # Skip non-HTML content and anchors
        if (url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip')) or 
            '#' in url):
            return False
        
        split_paths = parsed.path.split('/')

        lang = 'en'
        if len(split_paths)>1:
            lang = split_paths[1]

        if len(lang)==2 and lang!='en':
            return False

        return True

    def save_page(self, url, content):
        """Save the page content to a file."""
        try:
            # Create a file path from the URL
            parsed = urlparse(url)
            path_parts = parsed.path.strip('/').split('/')
            
            # Create nested directories if needed
            current_dir = self.output_dir
            for part in path_parts[:-1]:
                current_dir = os.path.join(current_dir, part)
                os.makedirs(current_dir, exist_ok=True)
            
            # Save the content
            filename = path_parts[-1] if path_parts else 'index'
            if not filename.endswith('.html'):
                filename += '.html'
            
            filepath = os.path.join(current_dir, filename)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return filepath
        except Exception as e:
            print(f"Error saving {url}: {str(e)}")
            return None

    def extract_links(self, soup, base_url):
        """Extract all valid links from the page."""
        links = set()
        for a_tag in soup.find_all('a', href=True):
            href = a_tag['href']
            full_url = urljoin(base_url, href)
            if self.is_valid_url(full_url):
                links.add(full_url)
                # Mark URL as queued immediately to prevent duplicates
                self.queued_urls.add(full_url)
        return links

    def scrape_page(self, url):
        """Scrape a single page and return its links."""
        try:
            # Add delay to be respectful
            time.sleep(1)
            
            response = requests.get(url, headers=self.headers, timeout=10)
            response.raise_for_status()
            
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Save the page
            saved_path = self.save_page(url, response.text)
            if saved_path:
                print(f"Successfully saved: {url} -> {saved_path}")
            
            # Extract and return links
            return self.extract_links(soup, url)
            
        except Exception as e:
            print(f"Error scraping {url}: {str(e)}")
            self.failed_urls.add(url)
            return set()

    def scrape_all(self, max_pages=None, max_workers=5):
        """
        Scrape all documentation pages starting from the base URL.
        
        Args:
            max_pages: Maximum number of pages to scrape (None for unlimited)
            max_workers: Number of concurrent threads
        """
        to_visit = {self.base_url}
        self.queued_urls.add(self.base_url)  # Mark initial URL as queued
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            while to_visit and (max_pages is None or len(self.visited_urls) < max_pages):
                # Get next batch of URLs to process
                current_batch = set()
                while len(current_batch) < max_workers and to_visit:
                    current_batch.add(to_visit.pop())
                
                if not current_batch:
                    break
                
                # Process current batch
                future_to_url = {
                    executor.submit(self.scrape_page, url): url 
                    for url in current_batch
                }
                
                # Handle results
                for future in future_to_url:
                    url = future_to_url[future]
                    try:
                        new_links = future.result()
                        self.visited_urls.add(url)
                        # Add new links to visit (they're already marked as queued)
                        to_visit.update(new_links)
                    except Exception as e:
                        print(f"Error processing {url}: {str(e)}")
                        self.failed_urls.add(url)

        # Save statistics
        stats = {
            'total_pages_scraped': len(self.visited_urls),
            'failed_urls': list(self.failed_urls),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(os.path.join(self.output_dir, 'scraping_stats.json'), 'w') as f:
            json.dump(stats, f, indent=2)
            
        print(f"\nScraping completed!")
        print(f"Total pages scraped: {len(self.visited_urls)}")
        print(f"Failed URLs: {len(self.failed_urls)}")

if __name__ == '__main__':
    scraper = SnowflakeDocsScraper()
    # Optionally limit the number of pages to scrape
    scraper.scrape_all(max_pages=None, max_workers=5)