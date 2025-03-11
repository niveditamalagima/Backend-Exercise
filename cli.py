import argparse
import csv
import logging
from get_papers_list.fetch import fetch_papers

def setup_logger(debug: bool):
    """Set up logging based on debug flag."""
    logging.basicConfig(level=logging.DEBUG if debug else logging.INFO)

def save_to_csv(papers, file_name: str):
    """Save the list of papers to a CSV file."""
    keys = papers[0].keys()
    with open(file_name, mode='w', newline='') as file:
        writer = csv.DictWriter(file, fieldnames=keys)
        writer.writeheader()
        writer.writerows(papers)

def main():
    parser = argparse.ArgumentParser(description="Fetch PubMed papers.")
    parser.add_argument("query", type=str, help="The query string for PubMed.")
    parser.add_argument("-d", "--debug", action="store_true", help="Enable debug logging.")
    parser.add_argument("-f", "--file", type=str, help="Output file to save results.")
    
    args = parser.parse_args()
    
    setup_logger(args.debug)
    
    # Fetch papers from PubMed
    papers = fetch_papers(args.query)
    
    # If results are found, save or display them
    if papers:
        if args.file:
            save_to_csv(papers, args.file)
            logging.info(f"Results saved to {args.file}")
        else:
            for paper in papers:
                print(paper)
    else:
        logging.warning("No papers found for the query.")

if __name__ == "__main__":
    main()
