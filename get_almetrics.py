from pyaltmetric import Altmetric
import pandas as pd
import argparse
from time import sleep
from datetime import datetime
from os import path

now = datetime.now()
journals = []
added_on = []
months_since_addition = []
almetrics_score = []
cited_by_tweets = []
readers_counts = []
almetrics_links = []

def get_months_delta(article):
    num_months = (now.year - article.added_on.year) * 12 + (now.month - article.added_on.month)
    
    if num_months == 0:
        return 1 
    else: 
        return num_months
    
def get_single_article_info(DOI):
    altmetric_object = Altmetric()
    article = altmetric_object.article_from_doi(DOI)
    if article is not None:
        print('Title:', article.title)
        authors = ', '.join(article.raw_dictionary['authors'])
        print('Authors:', authors)
        print('added_on:', article.added_on.strftime('%d/%m/%Y'))
        print('Months since addition:', get_months_delta(article))
        print('Cited by tweets:', article.cited_by_tweeters_count)
        print('Almetrics readers:', article.readers_count)
        print('Almetrics link:', article.altmetric_details_url)
    else:
        print('Could not find article with this DOI')
    

def get_articles_info(csv_file, doi_key):
    altmetric_object = Altmetric()
    fname, ext = path.splitext(csv_file)
    dataframe = pd.read_csv(csv_file, index_col=0)
    
    assert doi_key in dataframe.columns, f'Column name {doi_key} not found'
    
    for i in dataframe[doi_key]:
        article = altmetric_object.article_from_doi(str(i).strip())
    
        if article is not None:
            journals.append(article.journal)
            added_on.append(article.added_on.strftime('%d/%m/%Y'))
            months_since_addition.append(get_months_delta(article))
            almetrics_score.append(article.score)
            cited_by_tweets.append(article.cited_by_tweeters_count)
            readers_counts.append(article.readers_count)
            almetrics_links.append(article.altmetric_details_url)
        else:
            print(f'DOI: {i} not found, leaving blank')
            journals.append('')
            added_on.append('')
            months_since_addition.append('')
            almetrics_score.append('')
            cited_by_tweets.append('')
            readers_counts.append('')
            almetrics_links.append('')
    
        sleep(0.1)
    
    article_dict = {
        'journals' : journals,
        'impact factor' : '',
        'added on' : added_on,
        'months since addition' : months_since_addition,
        'number of citations' : '',
        'citations per month' : '',
        'almetrics score' : almetrics_score,
        'cited by tweets' : cited_by_tweets,
        'readers counts' : readers_counts,
        'almetrics link' : almetrics_links
    }

    for k,v in article_dict.items():
        dataframe[k] = v

    dataframe.to_csv(f'{fname}_processed.csv')
    
    return article_dict

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('-d', '--DOI', help='Article DOI for')
    parser.add_argument('-c', '--csv', help='Input csv file containing DOI column')
    parser.add_argument('-l', '--DOI_col', help='Column name containing DOI links')

    args = parser.parse_args()

    if args.csv is not None:
        assert args.DOI_col is not None, 'Column name containing DOI links must be provided'
        info = get_articles_info(args.csv, args.DOI_col)
    elif args.DOI is not None:
        get_single_article_info(args.DOI)
    else:
        raise ValueError('Must provide --DOI or --csv, use -h for help')

if __name__ == "__main__":
    main()
