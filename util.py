from tabulate import tabulate


def print_df_sample(df, rows=10):
    print(tabulate(df.iloc[0:rows], headers='keys', tablefmt='github'))


def print_df(df):
    print(tabulate(df, headers='keys', tablefmt='github'))


def to_csv(dataframe, file_name):
    dataframe.to_csv(file_name + ".csv", ";", encoding="latin")