#!/usr/bin/env python3
"""
📰 NEWS AGGREGATOR ELITE v3.1 (Fixed)
-----------------------------
> Multithreaded Scraper
> Termux Optimized
> Direct Browser Integration
> Cyberpunk UI
> Instagram: @krpankajchaudhary
"""

import requests
from bs4 import BeautifulSoup
import json
import csv
from datetime import datetime
import time
import os
import sys
import re
import concurrent.futures
import shutil

# --- CONFIG & STYLING ---
try:
    term_width = shutil.get_terminal_size().columns
except:
    term_width = 80

class C:
    # Cyberpunk Color Palette
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    END = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    BG_BLACK = '\033[40m'
    W = '\033[97m'  # Added White Color

def clear_screen():
    os.system('clear' if os.name != 'nt' else 'cls')

def print_center(text, color=C.CYAN):
    padding = max(0, (term_width - len(text)) // 2)
    print(f"{color}{' ' * padding}{text}{C.END}")

def banner():
    clear_screen()
    print(f"{C.CYAN}═" * term_width)
    print_center("⚡ NEWS NEXUS PRO v3.1 ⚡", C.HEADER + C.BOLD)
    print_center("Global Intel Aggregator | Termux Edition", C.BLUE)
    print(f"{C.CYAN}═" * term_width + C.END)

# --- NETWORK CORE ---

def get_headers():
    return {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9',
        'Referer': 'https://google.com'
    }

# --- SCRAPERS (OPTIMIZED) ---

def scrape_source(func, name):
    try:
        return func()
    except Exception as e:
        return []

def scrape_toi():
    articles = []
    try:
        url = "https://timesofindia.indiatimes.com/india"
        resp = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        for item in soup.select('.news-item, .brief-news, figcaption')[:12]:
            link_tag = item.find('a')
            if link_tag and link_tag.get('href'):
                title = link_tag.get_text(strip=True)
                if len(title) > 15:
                    url = link_tag['href']
                    if not url.startswith('http'): url = 'https://timesofindia.indiatimes.com' + url
                    articles.append({'title': title, 'source': 'TOI', 'url': url, 'cat': 'India'})
    except: pass
    return articles

def scrape_hindu():
    articles = []
    try:
        url = "https://www.thehindu.com/news/"
        resp = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        for item in soup.select('.element, .story-card')[:12]:
            title_tag = item.select_one('h3 a, h2 a, .title a')
            if title_tag:
                title = title_tag.get_text(strip=True)
                url = title_tag['href']
                if not url.startswith('http'): url = 'https://www.thehindu.com' + url
                articles.append({'title': title, 'source': 'The Hindu', 'url': url, 'cat': 'News'})
    except: pass
    return articles

def scrape_techcrunch():
    articles = []
    try:
        url = "https://techcrunch.com/"
        resp = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        for item in soup.select('.post-block__title a')[:12]:
            title = item.get_text(strip=True)
            url = item['href']
            articles.append({'title': title, 'source': 'TechCrunch', 'url': url, 'cat': 'Tech'})
    except: pass
    return articles

def scrape_bbc():
    articles = []
    try:
        url = "https://www.bbc.com/news"
        resp = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        for item in soup.select('[data-testid="card-text-wrapper"], h2')[:12]:
            link = item.find_parent('a') if item.name != 'a' else item
            if not link: link = item.find('a')
            
            if link:
                title = item.get_text(strip=True)
                url = link.get('href')
                if url and not url.startswith('http'): url = 'https://www.bbc.com' + url
                if len(title) > 10:
                    articles.append({'title': title, 'source': 'BBC', 'url': url, 'cat': 'Global'})
    except: pass
    return articles

def scrape_hacker_news():
    articles = []
    try:
        url = "https://news.ycombinator.com/"
        resp = requests.get(url, headers=get_headers(), timeout=10)
        soup = BeautifulSoup(resp.text, 'html.parser')
        
        for item in soup.select('.titleline > a')[:15]:
            title = item.get_text(strip=True)
            url = item['href']
            articles.append({'title': title, 'source': 'HackerNews', 'url': url, 'cat': 'Tech'})
    except: pass
    return articles

# --- UTILITIES ---

def open_url_in_termux(url):
    """Opens URL in Android Default Browser"""
    try:
        os.system(f'termux-open-url "{url}"')
    except:
        try:
            os.system(f'xdg-open "{url}"')
        except:
            print(f"{C.FAIL}Could not open browser. Copy link manually.{C.END}")

def clean_articles(articles):
    seen = set()
    unique = []
    for a in articles:
        key = ''.join(filter(str.isalnum, a['title'].lower()))[:30]
        if key not in seen and len(a['title']) > 15:
            seen.add(key)
            unique.append(a)
    return unique

# --- MAIN UI FLOW ---

def load_data_concurrently():
    print(f"\n{C.WARNING}[*] Initializing Satellite Uplinks...{C.END}")
    
    tasks = {
        'Times of India': scrape_toi,
        'The Hindu': scrape_hindu,
        'TechCrunch': scrape_techcrunch,
        'BBC News': scrape_bbc,
        'Hacker News': scrape_hacker_news
    }
    
    all_articles = []
    total_tasks = len(tasks)
    completed = 0
    
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_source = {executor.submit(func): name for name, func in tasks.items()}
        
        for future in concurrent.futures.as_completed(future_to_source):
            source_name = future_to_source[future]
            try:
                data = future.result()
                all_articles.extend(data)
                completed += 1
                
                bar_len = 20
                filled = int(bar_len * completed / total_tasks)
                bar = '█' * filled + '░' * (bar_len - filled)
                sys.stdout.write(f"\r{C.GREEN} :: FETCHING :: [{bar}] {source_name} ({len(data)}){C.END}")
                sys.stdout.flush()
                
            except Exception as exc:
                pass
    
    print(f"\n\n{C.GREEN}[+] Data Stream Complete. Processing...{C.END}")
    time.sleep(0.5)
    return clean_articles(all_articles)

def display_list(articles):
    banner()
    if not articles:
        print_center("No data found. Check internet connection.", C.FAIL)
        return

    print(f"{C.BG_BLACK} ID  | SOURCE       | HEADLINE (Total: {len(articles)}){C.END}")
    print(f"{C.CYAN}─" * term_width + C.END)

    for i, a in enumerate(articles):
        idx = str(i+1).zfill(2)
        source = a['source'][:10].ljust(10)
        
        # Smart Truncate to fit screen
        max_title_len = term_width - 20 
        title = a['title'][:max_title_len]
        if len(a['title']) > max_title_len: title += "..."
        
        # Color Logic
        color = C.W if i % 2 == 0 else C.CYAN  # FIXED HERE
        if "Tech" in a['source']: color = C.GREEN
        
        print(f"{C.WARNING} {idx}  {C.BLUE}{source} {C.END} {color}{title}{C.END}")

def main_menu():
    articles = load_data_concurrently()
    
    while True:
        display_list(articles[:40])
        print(f"\n{C.CYAN}─" * term_width + C.END)
        print(f"{C.BOLD}COMMANDS:{C.END}")
        print(f"[#] Enter ID to open (e.g., 5)")
        print(f"[s] Search  [r] Refresh  [x] Exit")
        
        choice = input(f"\n{C.GREEN}root@news-nexus~# {C.END}").lower().strip()
        
        if choice == 'x':
            print(f"\n{C.FAIL}System Shutdown.{C.END}")
            sys.exit()
            
        elif choice == 'r':
            articles = load_data_concurrently()
            
        elif choice == 's':
            query = input(f"{C.WARNING}Search Query: {C.END}").lower()
            filtered = [a for a in articles if query in a['title'].lower()]
            print(f"\n{C.GREEN}Found {len(filtered)} results:{C.END}")
            for i, a in enumerate(filtered):
                print(f"{i+1}. {a['title']} ({a['source']})")
            input(f"\n{C.BLUE}Press Enter to return...{C.END}")
            
        elif choice.isdigit():
            idx = int(choice) - 1
            if 0 <= idx < len(articles):
                target = articles[idx]
                print(f"\n{C.GREEN}[+] Opening: {target['title']}{C.END}")
                open_url_in_termux(target['url'])
                time.sleep(1)
            else:
                print(f"{C.FAIL}Invalid ID{C.END}")
                time.sleep(1)

if __name__ == "__main__":
    try:
        main_menu()
    except KeyboardInterrupt:
        print(f"\n{C.FAIL}Force Exit.{C.END}")
