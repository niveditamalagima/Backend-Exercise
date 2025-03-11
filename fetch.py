import pandas as pd
from Bio import Entrez
from typing import List, Optional, Dict

# Set your email as per PubMed's request
Entrez.email = "your_email@example.com"

def fetch_papers(query: str, max_results: int = 100) -> List[Dict]:
    """
    Fetch papers from PubMed based on the query provided.

    Args:
    query (str): The search query to pass to PubMed.
    max_results (int): Maximum number of results to fetch.

    Returns:
    List[Dict]: A list of dictionaries containing paper details.
    """
    handle = Entrez.esearch(db="pubmed", term=query, retmax=max_results)
    record = Entrez.read(handle)
    ids = record["IdList"]
    
    papers = []
    
    if ids:
        handle = Entrez.efetch(db="pubmed", id=ids, retmode="xml")
        records = Entrez.read(handle)
        
        for article in records["PubmedArticle"]:
            paper_data = extract_paper_details(article)
            papers.append(paper_data)
    
    return papers

def extract_paper_details(article) -> Dict:
    """
    Extract relevant details from a PubMed article.

    Args:
    article: The PubMed article object.

    Returns:
    Dict: A dictionary containing paper details.
    """
    title = article["MedlineCitation"]["Article"]["ArticleTitle"]
    pub_date = article["MedlineCitation"]["Article"]["Journal"]["JournalIssue"]["PubDate"]
    pub_date_str = f"{pub_date.get('Year', '')}-{pub_date.get('Month', '')}"
    
    authors = article["MedlineCitation"]["Article"]["AuthorList"]
    non_academic_authors = []
    companies = []
    corresponding_email = None
    
    for author in authors:
        if "Affiliation" in author:
            affiliation = author["Affiliation"]
            if "company" in affiliation.lower():  # Simplified check for companies
                companies.append(affiliation)
            else:
                non_academic_authors.append(f"{author['LastName']}, {author['ForeName']}")
        if "AuthorAffiliation" in author and "corresponding" in author.get("AuthorAffiliation", "").lower():
            corresponding_email = article["MedlineCitation"]["Article"]["AuthorList"][0].get("Email", None)

    return {
        "PubmedID": article["MedlineCitation"]["PMID"],
        "Title": title,
        "PublicationDate": pub_date_str,
        "NonAcademicAuthors": "; ".join(non_academic_authors),
        "CompanyAffiliations": "; ".join(companies),
        "CorrespondingAuthorEmail": corresponding_email or "N/A"
    }
