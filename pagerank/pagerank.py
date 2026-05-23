import os
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """
    probabilities = {}
    pages = list(corpus.keys())
    num_pages = len(pages)
    
    # Get the links from the current page
    links = corpus[page]
    
    # If page has no links, treat as linking to all pages (including itself)
    if len(links) == 0:
        # Each page gets equal probability from random choice
        for p in pages:
            probabilities[p] = 1 / num_pages
    else:
        # Calculate probabilities
        for p in pages:
            # Probability from random jump (1 - damping_factor) / N
            random_prob = (1 - damping_factor) / num_pages
            
            # Probability from following a link: damping_factor / num_links if page links to p
            if p in links:
                link_prob = damping_factor / len(links)
            else:
                link_prob = 0
            
            probabilities[p] = random_prob + link_prob
    
    return probabilities


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    # Initialize counts for each page
    counts = {page: 0 for page in corpus}
    pages = list(corpus.keys())
    
    # First sample: choose a page at random
    current_page = random.choice(pages)
    counts[current_page] += 1
    
    # Generate remaining n-1 samples
    for _ in range(1, n):
        # Get transition probabilities for current page
        probabilities = transition_model(corpus, current_page, damping_factor)
        
        # Choose next page based on transition probabilities
        current_page = random.choices(
            list(probabilities.keys()),
            weights=list(probabilities.values())
        )[0]
        
        counts[current_page] += 1
    
    # Calculate PageRank as proportion of samples
    pagerank = {page: count / n for page, count in counts.items()}
    
    return pagerank


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    num_pages = len(corpus)
    pages = list(corpus.keys())
    
    # Initialize ranks to 1/N
    ranks = {page: 1 / num_pages for page in pages}
    
    # Build reverse link map: which pages link to each page
    # Also handle pages with no links (they link to all pages)
    links_to = {page: set() for page in pages}
    for page in pages:
        for link in corpus[page]:
            links_to[link].add(page)
    
    # Iterate until convergence
    while True:
        new_ranks = {}
        max_diff = 0
        
        for page in pages:
            # Calculate new PageRank for this page
            # PR(page) = (1 - d) / N + d * sum(PR(i) / NumLinks(i) for i linking to page)
            
            # Sum contributions from all pages that link to this page
            # Include pages with no links (they link to all pages)
            summation = 0
            for linking_page in pages:
                # If linking_page has no links, it links to all pages
                if len(corpus[linking_page]) == 0:
                    # This page contributes 1/N to every page
                    summation += damping_factor * ranks[linking_page] / num_pages
                elif page in corpus[linking_page]:
                    # This page links to our page
                    summation += damping_factor * ranks[linking_page] / len(corpus[linking_page])
            
            new_rank = (1 - damping_factor) / num_pages + summation
            new_ranks[page] = new_rank
            
            # Track maximum change
            diff = abs(new_ranks[page] - ranks[page])
            max_diff = max(max_diff, diff)
        
        # Check for convergence
        if max_diff <= 0.001:
            return new_ranks
        
        ranks = new_ranks


if __name__ == "__main__":
    main()
