import requests
from bs4 import BeautifulSoup
import os
from urllib.parse import urljoin, urlparse
import json
import time
import html2text

class SnowflakeDocsScraper:
    def __init__(self, base_url='https://docs.snowflake.com/en', max_depth=4):
        self.base_url = base_url
        self.visited_urls = set()
        self.queued_urls = set()
        self.failed_urls = set()
        self.domain = 'docs.snowflake.com'
        self.max_depth = max_depth
        # Create directory for saving pages
        self.output_dir = 'snowflake_docs'
        os.makedirs(self.output_dir, exist_ok=True)
        
        # Initialize HTML to Markdown converter
        self.html_converter = html2text.HTML2Text()
        self.html_converter.ignore_links = False
        self.html_converter.ignore_images = False
        self.html_converter.ignore_tables = False
        
        # Headers
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        }

    def get_url_depth(self, url):
        """Calculate depth of URL relative to base URL."""
        parsed = urlparse(url)
        path_parts = parsed.path.strip('/').split('/')
        
        # Find the 'en' part and calculate depth after it
        try:
            en_index = path_parts.index('en')
            depth = len(path_parts) - (en_index + 1)
            return max(0, depth)  # Root is depth 0
        except ValueError:
            return 0

    def is_valid_url(self, url, current_depth):
        """Check if URL is valid for scraping with depth check."""
        parsed = urlparse(url)
        
        # Check if URL is already visited or queued
        if url in self.visited_urls or url in self.queued_urls:
            return False
            
        # Ensure URL is from the correct domain
        if parsed.netloc != self.domain:
            return False
        
        # Check depth
        if current_depth > 2:
            return False

        # languauage check
        split_paths = parsed.path.split('/')
        lang = 'en'
        if len(split_paths)>1:
            lang = split_paths[1]
        if len(lang)==2 and lang!='en':
            return False
        
        # Skip unwanted sections
        skip_patterns = [
            '/release-notes/',
            '/sql-reference/',
            '/archive/',
            '/other-resources/',
            '/icons/',
            '/images/',
            '/css/',
            '/js/',
            '/feedback/'
        ]
        
        if any(pattern in parsed.path for pattern in skip_patterns):
            return False
            
        # Skip non-HTML content and anchors
        if (url.endswith(('.png', '.jpg', '.jpeg', '.gif', '.pdf', '.zip', '.js', '.css')) or 
            '#' in url):
            return False
            
        return True

    def extract_main_content(self, soup, url):
        """Extract content from Snowflake's dynamic page structure."""
        try:
            # Look for the Next.js data script
            next_data = soup.find('script', {'id': '__NEXT_DATA__'})
            if next_data:
                data = json.loads(next_data.string)
                # Extract content from the pageProps
                if 'props' in data and 'pageProps' in data['props']:
                    content = data['props']['pageProps'].get('content', '')
                    if content:
                        # Parse the content as HTML
                        content_soup = BeautifulSoup(content, 'html.parser')
                        # Convert to markdown
                        markdown = self.html_converter.handle(str(content_soup))
                        return markdown

            # Fallback to traditional content extraction
            main_content = soup.find('main') or soup.find('article')
            if main_content:
                # Remove unwanted elements
                for element in main_content.find_all(['script', 'style', 'nav', 'footer']):
                    element.decompose()
                return self.html_converter.handle(str(main_content))

            print(f"Warning: No content found for {url}")
            return None

        except Exception as e:
            print(f"Error extracting content from {url}: {str(e)}")
            return None
        
    def save_page(self, url, content):
        """Save the page content to a markdown file."""
        try:
            parsed = urlparse(url)
            path_parts = parsed.path.strip('/').split('/')
            
            if 'en' in path_parts:
                en_index = path_parts.index('en')
                path_parts = path_parts[en_index + 1:]
            
            current_dir = self.output_dir
            for part in path_parts[:-1]:
                current_dir = os.path.join(current_dir, part)
                os.makedirs(current_dir, exist_ok=True)
            
            filename = path_parts[-1] if path_parts else 'index'
            filename = filename.replace('.html', '')
            filepath = os.path.join(current_dir, filename + '.md')
            
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
                
            return filepath
        except Exception as e:
            print(f"Error saving {url}: {str(e)}")
            return None

    def scrape_all(self):
        """Scrape documentation pages up to depth 2."""
        to_visit = [(self.base_url, 0)]  # (url, depth) pairs
        self.queued_urls.add(self.base_url)
        
        while to_visit:
            url, depth = to_visit.pop(0)
            
            try:
                print(f"Scraping: {url} (depth {depth})")
                time.sleep(1)  # Rate limiting
                
                response = requests.get(url, headers=self.headers, timeout=10)
                response.raise_for_status()
                
                soup = BeautifulSoup(response.text, 'html.parser')
                content = self.extract_main_content(soup, url)
                
                if content:
                    saved_path = self.save_page(url, content)
                    if saved_path:
                        print(f"Saved to: {saved_path}")
                        # Print first line for debugging
                        with open(saved_path, 'r', encoding='utf-8') as f:
                            print(f"First line: {f.readline().strip()}")
                
                # Find new links if not at max depth
                if depth < 2:
                    for a_tag in soup.find_all('a', href=True):
                        href = a_tag['href']
                        full_url = urljoin(url, href)
                        if self.is_valid_url(full_url, depth + 1):
                            to_visit.append((full_url, depth + 1))
                            self.queued_urls.add(full_url)
                
                self.visited_urls.add(url)
                
            except Exception as e:
                print(f"Error processing {url}: {str(e)}")
                self.failed_urls.add(url)

        stats = {
            'total_pages_scraped': len(self.visited_urls),
            'pages_by_depth': {
                '0': sum(1 for url in self.visited_urls if self.get_url_depth(url) == 0),
                '1': sum(1 for url in self.visited_urls if self.get_url_depth(url) == 1),
                '2': sum(1 for url in self.visited_urls if self.get_url_depth(url) == 2),
            },
            'failed_urls': list(self.failed_urls),
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
        }
        
        with open(os.path.join(self.output_dir, 'scraping_stats.json'), 'w') as f:
            json.dump(stats, f, indent=2)

        print(f"\nScraping completed!")
        print(f"Total pages scraped: {len(self.visited_urls)}")
        for depth, count in stats['pages_by_depth'].items():
            print(f"Depth {depth}: {count} pages")
        print(f"Failed URLs: {len(self.failed_urls)}")

if __name__ == '__main__':
    scraper = SnowflakeDocsScraper(max_depth=4)
    scraper.scrape_all()