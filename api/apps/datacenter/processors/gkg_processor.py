import pandas as pd

from ..utils.utils import get_schema_headers, get_date_range_strings, get_date_url, get_date_from_string
from .graph_processor import extract_and_filter_data

class GKGProcessor():
  '''
  Creates a DataCenter.
  A DataCenter is a MongoDB instance specific to
  a client's needs, tailored to their interests and regions

  TODO: Interface with MongoDB
  '''

  def __init__(self, query=None):
    '''
    Initializes a new DataCenter populated with data
    from the specified start date (inclusive) to the end date (exclusive)

    The data will be populated by data from specified geographies, as well
    as the specified actors involved in each geographies. Geographies are defined
    by the Region class.

    If no actors are specified, all actors will be included.

    Dates should be formatted as follows:
    'YYYY MM DD'
    e.g. '2019 02 19'
    '''
  
    print('INITIALIZING DATA CENTER')

    # initialize data analysis variables
    self.total_data_count = 0
    self.relevant_data_count = 0

    # initialize the headers of the dataframe
    self.headers = get_schema_headers()

    # initialize query
    self.query = query

    # get dates to initialize the database
    init_date_strings = get_date_range_strings(query.start_date, query.end_date)
    [self.update_database(date_string) for date_string in init_date_strings]

    print('DataCenter Initialized')

    print('Logging information: log.txt')

    print('\nInformation:')
    print(f'* Total Data Count: {self.total_data_count} articles processed')
    print(f'* Relevant Information: {self.relevant_data_count} articles stored')
    print(f'* Total Percentage: {self.relevant_data_count/self.total_data_count:.0%}')

  def get_data_frame(self, date_string):
    try:
      # get data url
      url = get_date_url(date_string)

      # read in data file
      df = pd.read_csv(url, compression='zip', encoding='latin1', header=None, sep='\t')
      df.columns = self.headers
      return True, df
    except Exception as e:
      return False, None

  def update_database(self, date_string):
    '''
    Updates the database with information from a single day
    '''
    print(f'* Processing {date_string} Information...')
    success, df = self.get_data_frame(date_string)
    if not success: return False
    date = get_date_from_string(date_string)

    total_count = len(df)
    print(f'** {total_count} Rows')
    relevant_count = 0

    for ix, data in df.iterrows():
      if self.update_row(data, date): relevant_count += 1

    self.total_data_count += total_count
    self.relevant_data_count += relevant_count

    print(f'  {date_string} processed.')
    print(f'\n* {date_string} Information: ')
    print(f'** Relevant Data: {relevant_count/total_count:.0%}\n\n')
    return True

  def update_row(self, data, date):
    try:
      data = extract_and_filter_data(data, date, self.query)

      (article, actors) = data

      # update actor Graph
      if not update_graph(article, actors): return False

      return True
    except Exception as e:
      return False