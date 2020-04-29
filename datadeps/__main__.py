import pandas
import os
import sys
import pickle

OUTPUT_DIR = 'gen'
SUBREDDITS_CSV = 'vg-subreddits.csv'
MATRIX_CSV = 'seeding/out/matrix.csv'

def main():
    rel = f'./{sys.argv[0]}'
    output_dir = f'{rel}/{OUTPUT_DIR}'
    output_dir_exists = os.path.exists(output_dir)

    always_retry = len(sys.argv) > 1 and sys.argv[1] == '-retry'

    if not always_retry and output_dir_exists:
        print('mkdatadeps: Nothing to do.')
        return

    print('mkdatadeps: Generating...')

    if not output_dir_exists:
        os.makedirs(output_dir)

    write(f'{output_dir}/subreddits.pickle', read_subreddits(f'{rel}/{SUBREDDITS_CSV}'))
    write(f'{output_dir}/matrix.pickle', read_matrix(f'{rel}/{MATRIX_CSV}'))

    print('mkdatadeps: Done!')

def write(path, obj):
    with open(path, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def assert_exists(path):
    if not os.path.exists(path):
        print(f'mkdatadeps: ERROR! Missing file "{path}"')
        sys.exit(1)

def read_subreddits(path):
    assert_exists(path)
    df = pandas.read_csv(path)

    # Just get the subreddit column as a list of strings...
    # The `[0]` is a dirty hack and should be replaced
    return df[['subreddit']].values.reshape((1, -1)).tolist()[0]

def read_matrix(path):
    assert_exists(path)
    df = pandas.read_csv(path)
    return df.values

if __name__ == '__main__':
    main()
