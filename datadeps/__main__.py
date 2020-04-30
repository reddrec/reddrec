import os
import sys
import numpy as np
import pandas as pd
import pickle
import random

# Jump up 1 dir so we can import reddrec
rel = os.path.dirname(__file__)
sys.path.append(os.path.join(rel, '..'))
from reddrec.utils import reddit_from_env
from reddrec.reddit import hot_posts, usernames, Comments

OUTPUT_DIR = 'gen'
SUBREDDITS_CSV = 'vg-subreddits.csv'
MATRIX_CSV = 'matrix.csv'

def log(msg):
    print(f'[datadeps] {msg}')

def main():
    output_dir = f'{rel}/{OUTPUT_DIR}'
    output_dir_exists = os.path.exists(output_dir)

    refetch_matrix = '-fetchNewMatrix' in sys.argv
    always_retry = refetch_matrix or '-retry' in sys.argv

    if not always_retry and output_dir_exists:
        log('Nothing to do.')
        return

    log('Generating...')

    if not output_dir_exists:
        os.makedirs(output_dir)

    subreddits = read_subreddits(f'{rel}/{SUBREDDITS_CSV}')
    write(f'{output_dir}/subreddits.pickle', subreddits)

    if refetch_matrix:
        matrix = fetch_matrix(subreddits)
        np.savetxt(f'{rel}/{MATRIX_CSV}', matrix, fmt='%d', delimiter=',')
        write(f'{output_dir}/matrix.pickle', matrix)
    else:
        write(f'{output_dir}/matrix.pickle', pd.read_csv(f'{rel}/{MATRIX_CSV}').values)

    log('Done!')

def write(path, obj):
    with open(path, 'wb') as f:
        pickle.dump(obj, f, protocol=4)

def assert_exists(path):
    if not os.path.exists(path):
        log(f'ERROR! Missing file "{path}"')
        sys.exit(1)

def read_subreddits(path):
    assert_exists(path)
    df = pd.read_csv(path)

    # Just get the subreddit column as a list of strings...
    # The `[0]` is a dirty hack and should be replaced
    return df[['subreddit']].values.reshape((1, -1)).tolist()[0]

def fetch_matrix(subreddits):
    rows = []

    reddit = reddit_from_env()
    all_users = set()

    log('fetch_matrix: find users')

    for subreddit in subreddits:
        try:
            log(f'Finding users in r/{subreddit}...')
            posts = hot_posts(reddit, subreddit, n=2)
            users = usernames(reddit, posts, up_to=5)
            all_users.update(users)
            log(f'Total user # = {len(all_users)}')
        except Exception as e:
            print(e)
            log(f'failed to find users in r/{subreddit}!')

    log('fetch_matrix: get user ratings')

    for user in all_users:
        try:
            log(f'Finding ratings for u/{user}...')
            c = Comments(reddit, user, subreddits=subreddits)
            ratings = c.fetch_ratings(n_comments=200, normalize=False)
            rows.append(ratings.astype('int32'))
        except Exception as e:
            print(e)
            log(f'failed to find ratings for u/{user}!')

    log('fetch_matrix: done')

    return np.array(rows)

if __name__ == '__main__':
    main()
