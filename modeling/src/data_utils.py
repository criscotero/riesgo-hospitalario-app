import gc

import pandas as pd


def join_prefix_suffix(waves: range, suffix: str,) -> set:

    prefixes = {f"r{wave}" for wave in waves} | {f"s{wave}" for wave in waves}

    joined_variables = {f"{prefix}{suffix}" for prefix in prefixes}

    return joined_variables


def stack_df(df: pd.DataFrame, target_variables: set, selected_features_suffixes: list, rural) -> pd.DataFrame:

    # selected_features_columns = {
    #    f"{prefix}{feature}" for feature in selected_features_suffixes for prefix in {'r1', 'r2', 's1', 's2'}
    # }
    #
    # <--- VERIFY COLUMNS HAVE BEEN PROPERLY GENERATED --->
    # if (len(selected_features_columns)) == 224:
    #    print(f"All columns add up! :)")
    # else:
    #    print(f"Columns are not adding up! :(")

    # <---- BEGIN ITERATION OF EACH TARGET FOR EACH ROW ---->
    new_target = 'hospitalized'
    new_rows = []
    for row in df.itertuples(index=False):
        row_dict = row._asdict()

        for target in target_variables:
            wave = int(target[1])
            prefix = target[:2]

            new_row = {'id': row_dict['unhhidnp'], 'wave': wave}

            hospitalization_value = row_dict.get(target, None)
            new_row[new_target] = hospitalization_value

            gender_key = 'ragender' if prefix.startswith(
                'r') else f's{wave}gender'
            new_row['gender'] = row_dict.get(gender_key, None)

            if rural == True:
                hWrural_col = f'h{wave}rural'
                new_row['location'] = row_dict[hWrural_col]

            for feature in selected_features_suffixes:
                col_name = f'{prefix}{feature}'
                if col_name in row_dict:
                    new_row[feature] = row_dict[col_name]

            new_rows.append(new_row)

    stacked_df = pd.DataFrame(new_rows)
    return stacked_df


def find_non_cross_wave_columns(columns: list, waves: set[str]) -> dict:
    """
    Finds columns that are not present in all 5 waves.
    """

    suffix_to_waves = {}

    for col in columns:
        if col[0] not in {'r', 's', 'h'} or col[1] not in waves:
            continue

        wave = col[1]  # the second character is the wave number
        suffix = col[2:]  # the rest of the column name is the suffix
        suffix_to_waves.setdefault(suffix, set()).add(wave)

    missing = {}
    for suffix, waves_found in suffix_to_waves.items():
        missing_waves = waves - waves_found
        if missing_waves:
            missing[suffix] = missing_waves
    return missing


def generate_waved_columns(wave_range: tuple, column_suffix: list) -> list:
    """
    Dynamically generates waved columns from a list of column suffixes.

    Args:
        column_suffix (list): The list of column suffixes to be prefixed with waves.

    Returns:
        list: list with generated waved columns.
    """

    return [
        f'r{wave}{suffix}'
        for wave in range(wave_range[0], wave_range[1] + 1)
        for suffix in column_suffix
    ]


def categorize_columns(df: pd.DataFrame) -> dict:
    """
    Categorizes columns into those that start with a specified prefix 
    and those that do not match this pattern.
    """

    waves = {str(i) for i in range(1, 6)} | {'a'}

    rX_prefix = {f'r{wave}' for wave in waves}
    sX_prefix = {f's{wave}' for wave in waves}
    hX_prefix = {f'h{wave}' for wave in waves}

    rX_columns = [
        col for col in df.columns if col.startswith(tuple(rX_prefix))]
    sX_columns = [
        col for col in df.columns if col.startswith(tuple(sX_prefix))]
    hX_columns = [
        col for col in df.columns if col.startswith(tuple(hX_prefix))]

    sX_hX_columns = set(sX_columns) | set(hX_columns)

    non_waved_columns = [col for col in df.columns if col not in (
        rX_columns + list(sX_hX_columns))]

    return {'rX_columns': rX_columns, 'hX_columns': hX_columns, 'sX_columns': sX_columns, 'non_waved_columns': non_waved_columns}


def compute_proportions(df: pd.DataFrame, columns: list) -> pd.DataFrame:
    """
    Computes the count and proportion of 1s and 0s for a given list of columns.

    Args:
        df (pd.DataFrame): The DataFrame containing the columns.
        columns (list): The list of column names to analyze.

    Returns:
        pd.DataFrame: A DataFrame with counts and proportions of 1s and 0s.
    """

    return df[columns].apply(lambda col: col.value_counts(normalize=True, dropna=False))




import pandas as pd
import numpy as np
from imblearn.over_sampling import SMOTE
from sklearn.feature_selection import VarianceThreshold
from scipy.stats import chi2_contingency



def handle_missing_values(df, numeric_placeholder=-999, categorical_placeholder='Missing'):
    """
    Replace missing values in numerical and categorical columns.
    Args:
        df (pd.DataFrame): The input dataset.
        numeric_placeholder: Placeholder for missing numerical values.
        categorical_placeholder: Placeholder for missing categorical values.
    Returns:
        pd.DataFrame: The dataframe with missing values handled.
    """
    for col in df.columns:
        if df[col].dtype in ['float64', 'int64']:
            df[col] = df[col].fillna(numeric_placeholder)
        else:  # Categorical columns
            df[col] = df[col].fillna(categorical_placeholder)
    return df


def balance_data(X, y):
    """
    Balance the dataset using SMOTE.
    Args:
        X (pd.DataFrame): Features dataframe.
        y (pd.Series): Target variable.
    Returns:
        tuple: Balanced features (X) and target (y).
    """
    smote = SMOTE(random_state=42)
    X_balanced, y_balanced = smote.fit_resample(X, y)
    return X_balanced, y_balanced


def filter_by_age(df, age_column='r5agey', age_threshold=50):
    """
    Filter rows by age threshold.
    Args:
        df (pd.DataFrame): The input dataset.
        age_column (str): The column containing age data.
        age_threshold (int): The minimum age to include.
    Returns:
        pd.DataFrame: Filtered dataset.
    """
    return df[df[age_column] >= age_threshold]



def remove_low_variability(df, threshold=0.01):
    """
    Remove features with low variance after ensuring all columns are numeric.
    Args:
        df (pd.DataFrame): Input dataframe.
        threshold (float): Variance threshold.
    Returns:
        pd.DataFrame: Dataframe with low-variance features removed.
    """
    # Ensure all columns are numeric
    df_numeric = df.select_dtypes(include=['number'])

    # Apply VarianceThreshold
    selector = VarianceThreshold(threshold=threshold)
    df_filtered = selector.fit_transform(df_numeric)

    # Return filtered DataFrame with selected columns
    return pd.DataFrame(df_filtered, columns=df_numeric.columns[selector.get_support()])


def handle_categorical_cardinality(df, max_cardinality=100, min_cardinality=2):
    """
    Remove categorical features with very high or very low cardinality.
    Args:
        df (pd.DataFrame): Input dataframe.
        max_cardinality (int): Maximum allowed unique values.
        min_cardinality (int): Minimum allowed unique values.
    Returns:
        pd.DataFrame: Dataframe with filtered categorical variables.
    """
    for col in df.select_dtypes(include=['object']).columns:
        unique_values = df[col].nunique()
        if unique_values > max_cardinality or unique_values < min_cardinality:
            df = df.drop(columns=[col])
    return df


def calculate_v_cramer(df, categorical_columns):
    """
    Calculate V Cramer correlation for categorical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        categorical_columns (list): List of categorical column names.
    Returns:
        pd.DataFrame: Correlation matrix for categorical variables.
    """
    def v_cramer(confusion_matrix):
        chi2 = chi2_contingency(confusion_matrix)[0]
        n = confusion_matrix.sum()
        phi2 = chi2 / n
        r, k = confusion_matrix.shape
        return np.sqrt(phi2 / min(k - 1, r - 1))

    corr_matrix = pd.DataFrame(index=categorical_columns, columns=categorical_columns)
    for col1 in categorical_columns:
        for col2 in categorical_columns:
            if col1 == col2:
                corr_matrix.loc[col1, col2] = 1.0
            else:
                confusion_matrix = pd.crosstab(df[col1], df[col2])
                corr_matrix.loc[col1, col2] = v_cramer(confusion_matrix)
    return corr_matrix


def filter_alive_respondents(df, status_column='r5iwstat', alive_value='1.Resp, alive'):
    """
    Filter the dataset to include only alive respondents based on the R5IWSTAT variable.

    Args:
        df (pd.DataFrame): Input dataset.
        status_column (str): Column name indicating respondent's status (default is 'R5IWSTAT').
        alive_value (int): Value in the status column that represents 'alive' (default is 1).

    Returns:
        pd.DataFrame: Filtered dataset containing only alive respondents.
    """
    # Filter rows where the status column equals the alive value
    filtered_df = df[df[status_column] == alive_value]
    return filtered_df



def analyze_and_handle_missing_values(df, threshold=30):
    """
    Analyze missing values, visualize them, and drop columns exceeding the threshold.

    Args:
        df (pd.DataFrame): Input dataframe.
        threshold (int): Percentage threshold for dropping columns (default: 30).

    Returns:
        pd.DataFrame: Dataframe after dropping columns with excessive missing values.
    """
    # Calculate the percentage of missing values
    missing_percentage = (df.isnull().sum() / len(df)) * 100

    # Visualize missing data
    plt.figure(figsize=(10, 6))
    missing_percentage.sort_values(ascending=False).plot(kind='bar', color='skyblue')
    plt.title("Percentage of Missing Values by Column", fontsize=16)
    plt.xlabel("Columns", fontsize=12)
    plt.ylabel("Percentage of Missing Values", fontsize=12)
    plt.xticks(rotation=45)
    plt.show()

    # Drop columns exceeding the threshold
    columns_to_drop = missing_percentage[missing_percentage > threshold].index
    print(f"Columns dropped (>{threshold}% missing): {list(columns_to_drop)}")

    df = df.drop(columns=columns_to_drop)
    return df


import matplotlib.pyplot as plt

def remove_columns_with_missing_values(df, missing_values_threshold=30, visualize=True):
    """
    Analyze missing values, optionally visualize them, and drop columns exceeding the threshold.

    Args:
        df (pd.DataFrame): Input dataframe.
        missing_values_threshold (int): Percentage threshold for dropping columns (default: 30).
        visualize (bool): Whether to visualize the missing data (default: True).

    Returns:
        pd.DataFrame: Dataframe after dropping columns with excessive missing values.
    """
    # Calculate the percentage of missing values
    missing_percentage = (df.isnull().sum() / len(df)) * 100

    if visualize:
        # Visualize missing data with highlighting for columns exceeding the threshold
        plt.figure(figsize=(10, 6))
        colors = ['red' if val > missing_values_threshold else 'skyblue' for val in missing_percentage]
        missing_percentage.sort_values(ascending=False).plot(kind='bar', color=colors)
        plt.axhline(y=missing_values_threshold, color='gray', linestyle='--', linewidth=1.5, label=f'Threshold ({missing_values_threshold}%)')
        plt.title("Percentage of Missing Values by Column", fontsize=16)
        plt.xlabel("Columns", fontsize=12)
        plt.ylabel("Percentage of Missing Values", fontsize=12)
        plt.xticks(rotation=45, ha='right')
        plt.legend()
        plt.show()

    # Identify and drop columns exceeding the threshold
    columns_to_drop = missing_percentage[missing_percentage > missing_values_threshold].index
    print(f"Dropping {len(columns_to_drop)} columns (>{missing_values_threshold}% missing): {list(columns_to_drop)}")

    # Drop the columns
    filtered_df = df.drop(columns=columns_to_drop)

    # Print updated shape
    print(f"Updated dataframe shape: {filtered_df.shape}")

    return filtered_df



def cramers_v(x, y):
    """
    Calculate Cramér's V statistic for categorical association.
    Args:
        x (pd.Series): First categorical variable.
        y (pd.Series): Second categorical variable.
    Returns:
        float: Cramér's V statistic.
    """
    # Ensure inputs are strings
    x, y = x.astype(str), y.astype(str)

    contingency_table = pd.crosstab(x, y)
    if contingency_table.size == 0:  # Handle empty tables
        return np.nan

    chi2 = chi2_contingency(contingency_table)[0]
    n = contingency_table.sum().sum()
    phi2 = chi2 / n
    r, k = contingency_table.shape

    # Handle cases where min(k-1, r-1) is 0
    if min(k - 1, r - 1) == 0:
        return np.nan

    return np.sqrt(phi2 / min(k - 1, r - 1))


def cramers_v_matrix(df):
    """
    Create a Cramér's V correlation matrix for all categorical variables.
    Args:
        df (pd.DataFrame): Dataframe containing categorical variables.
    Returns:
        pd.DataFrame: Cramér's V correlation matrix.
    """
    # Automatically filter categorical columns
    categorical_columns = df.select_dtypes(include=['object', 'category']).columns

    # Ensure all categorical columns are strings
    df = df[categorical_columns].astype(str)

    cramers_matrix = pd.DataFrame(index=categorical_columns, columns=categorical_columns)

    for col1 in categorical_columns:
        for col2 in categorical_columns:
            if col1 == col2:
                cramers_matrix.loc[col1, col2] = 1.0
            else:
                cramers_matrix.loc[col1, col2] = cramers_v(df[col1], df[col2])

    return cramers_matrix.astype(float)


def remove_redundant_features_cramers(df, cramers_matrix, threshold=0.8, target_column='r5hosp1y'):
    """
    Use a precomputed Cramér's V matrix to identify and remove redundant categorical features,
    ensuring the target variable is not removed.

    Args:
        df (pd.DataFrame): Dataframe containing categorical variables.
        cramers_matrix (pd.DataFrame): Precomputed Cramér's V correlation matrix.
        threshold (float): Threshold for Cramér's V to consider redundancy.
        target_column (str): The target variable that must not be removed.

    Returns:
        pd.DataFrame: Dataframe with redundant features removed.
    """
    # Identify redundant variables
    redundant_vars = set()
    for col1 in cramers_matrix.columns:
        for col2 in cramers_matrix.columns:
            if col1 != col2 and cramers_matrix.loc[col1, col2] > threshold:
                # Ensure the target variable is not added to redundant features
                if col2 != target_column:
                    redundant_vars.add(col2)

    # Drop redundant variables while preserving the target variable
    reduced_df = df.drop(columns=redundant_vars, errors='ignore')
    print(f"Removed {len(redundant_vars)} redundant features: {redundant_vars}")
    return reduced_df




def handle_all_missing_as_category(df, target_column='r5hosp1y', missing_label='Missing', numerical_fill_value=-1):
    """
    Treat missing values (NaN) in all columns as an additional category for categorical columns
    and assign a default value (-1) for numerical columns, excluding the target column.

    Args:
        df (pd.DataFrame): The input dataset.
        target_column (str): The column to exclude from missing value handling.
        missing_label (str): The label to replace missing values with in categorical columns (default: 'Missing').
        numerical_fill_value (int or float): The value to replace missing values with in numerical columns (default: -1).

    Returns:
        pd.DataFrame: The dataset with missing values handled appropriately.
    """
    df = df.copy()

    for col in df.columns:
        if col == target_column:
            # Skip the target column
            continue
        if df[col].dtype.name == 'category' or df[col].dtype == object:
            # Handle categorical columns
            if df[col].dtype.name == 'category':
                # Add the missing label to the categories if the column is categorical
                df[col] = df[col].cat.add_categories([missing_label])
            # Replace missing values with the missing label
            df[col] = df[col].fillna(missing_label)
        elif pd.api.types.is_numeric_dtype(df[col]):
            # Handle numerical columns
            df[col] = df[col].fillna(numerical_fill_value)

    return df



def extract_wave_data(df, wave_number):
    """
    Extract variables from a specific wave based on the second character of their names.
    Section 1.4 of the harmonized MHAS documentation (version C.2) explains that the second character
    of any variable refers to the particular wave the variable is encoding.

    Parameters:
    - df: DataFrame
    - wave_number: int or str, wave identifier (1, 2, 3, 4, 5; the character 'a' denotes a cross-wave variable)

    Returns:
    - DataFrame with columns for the specified wave.
    """
    # Select variables from a specific wave
    specific_wave_columns = [col for col in df.columns if len(
        col) > 1 and col[1] == str(wave_number)]

    # Select cross-wave variables
    cross_wave = [col for col in df.columns if len(col) > 1 and col[1] == 'a']

    # Combine specific and common variables
    wave_columns = list(set(specific_wave_columns + cross_wave))

    return df[wave_columns]


def extract_respondent_data(df):
    """
    Extract variables from respondent.
    Section 1.4 of the harmonized MHAS documentation (version C.2) explains that the first character
    of any variable refers to the particular individual referred to by the variable.

    Parameters:
    - df: DataFrame

    Returns:
    - DataFrame with columns for respondent.
    """
    return df[[col for col in df.columns if col.startswith('r')]]


def remove_missing_values(df, column_name):
    """
    Remove all rows matching missing values from a specified column

    Parameters:
    - df: DataFrame
    - column_name: name of column to search for missing values

    Returns:
    - DataFrame with no missing values for the specified column.
    """

    df = df[df[column_name].notna()]

    return df


def missing_value_ratio(df, ratio):
    """
    Identify variables with the specified missing value ratio

    Parameters:
    - df: DataFrame
    - ratio: proportion of missing values

    Returns:
    - List of columns with a ratio equal to or higher than the one specified by the user.
    """

    # Identify categorical columns
    # categorical_columns = df.select_dtypes(
    # include=['object', 'category']).columns

    # Identify and store columns with the specified missing value ratio
    columns_matching_missing_value_ratio = [
        col for col in df.columns
        if df[col].isnull().mean() > ratio
    ]

    print(f"Variables with a missing value ratio higher than {ratio}: {columns_matching_missing_value_ratio}")
    print(f"Count of variables with a missing ratio higher than {ratio}: {len(columns_matching_missing_value_ratio)}")

    return columns_matching_missing_value_ratio




def save_categorical_features_with_values(df: pd.DataFrame, file_name: str):
    """
    Saves the unique values of categorical features in a DataFrame to a text file.

    Parameters:
        df (pd.DataFrame): The input DataFrame.
        file_name (str): The name of the text file to save the output.
    """
    try:
        # Select only categorical columns
        categorical_cols = df.select_dtypes(include=['object']).columns
        file_path = os.path.join(DATASET_ROOT_PATH, file_name)
        # Open the file for writing
        with open(file_path, 'w') as f:
            for column in df.columns:
                # Get the unique values of the column
                unique_values = df[column].unique()
                # Limit the number of values shown for readability
                unique_values_preview = unique_values[:10]  # Show up to 10 values
                # Write the feature name and unique values to the file
                f.write(f"{column}: {list(unique_values_preview)}\n\n")

        print(f"Categorical features with their unique values have been saved to '{file_name}'")
    except Exception as e:
        print(f"An error occurred: {e}")





import matplotlib.pyplot as plt
import seaborn as sns

def plot_missing_values(df):
    """
    Plot the percentage of missing values for each column in the dataset.
    Args:
        df (pd.DataFrame): Input dataframe.
    """
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    missing_percentage = missing_percentage[missing_percentage > 0].sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=missing_percentage.values, y=missing_percentage.index, palette="viridis")
    plt.title("Percentage of Missing Values by Column", fontsize=16)
    plt.xlabel("Percentage of Missing Values", fontsize=12)
    plt.ylabel("Columns", fontsize=12)
    plt.show()

def plot_class_distribution(target):
    """
    Plot the distribution of the target variable to visualize class imbalance.
    Args:
        target (pd.Series): Target variable.
    """
    class_counts = target.value_counts()

    plt.figure(figsize=(8, 5))
    sns.barplot(x=class_counts.index, y=class_counts.values, palette="coolwarm")
    plt.title("Class Distribution of Target Variable", fontsize=16)
    plt.xlabel("Classes", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.show()

    print(f"Class Distribution:\n{class_counts}")
    print(f"Class Ratios:\n{class_counts / class_counts.sum() * 100}")


def plot_numerical_distributions(df, numeric_columns):
    """
    Plot the distributions of numerical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        numeric_columns (list): List of numerical column names.
    """
    for col in numeric_columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col].dropna(), kde=True, bins=30, color="skyblue")
        plt.title(f"Distribution of {col}", fontsize=16)
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.show()


def plot_categorical_distributions(df, categorical_columns):
    """
    Plot the distributions of categorical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        categorical_columns (list): List of categorical column names.
    """
    for col in categorical_columns:
        plt.figure(figsize=(8, 5))
        sns.countplot(x=df[col], order=df[col].value_counts().index, palette="muted")
        plt.title(f"Distribution of {col}", fontsize=16)
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Count", fontsize=12)
        plt.xticks(rotation=45)
        plt.show()


def plot_correlation_matrix(df, numeric_columns):
    """
    Plot a heatmap of correlations between numerical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        numeric_columns (list): List of numerical column names.
    """
    corr_matrix = df[numeric_columns].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title("Correlation Matrix", fontsize=16)
    plt.show()


def plot_v_cramer_matrix(df, categorical_columns):
    """
    Plot a heatmap of V Cramer correlations between categorical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        categorical_columns (list): List of categorical column names.
    """
    corr_matrix = calculate_v_cramer(df, categorical_columns)

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix.astype(float), annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title("V Cramer Correlation Matrix", fontsize=16)
    plt.show()


def plot_categorical_cardinality(df, categorical_columns):
    """
    Plot the cardinality (number of unique values) of categorical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        categorical_columns (list): List of categorical column names.
    """
    cardinality = {col: df[col].nunique() for col in categorical_columns}
    cardinality = pd.Series(cardinality).sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=cardinality.values, y=cardinality.index, palette="cool")
    plt.title("Cardinality of Categorical Variables", fontsize=16)
    plt.xlabel("Number of Unique Values", fontsize=12)
    plt.ylabel("Variables", fontsize=12)
    plt.show()



import matplotlib.pyplot as plt
import seaborn as sns

def plot_missing_values(df):
    """
    Plot the percentage of missing values for each column in the dataset.
    Args:
        df (pd.DataFrame): Input dataframe.
    """
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    missing_percentage = missing_percentage[missing_percentage > 0].sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=missing_percentage.values, y=missing_percentage.index, palette="viridis")
    plt.title("Percentage of Missing Values by Column", fontsize=16)
    plt.xlabel("Percentage of Missing Values", fontsize=12)
    plt.ylabel("Columns", fontsize=12)
    plt.show()

def plot_class_distribution(target):
    """
    Plot the distribution of the target variable to visualize class imbalance.
    Args:
        target (pd.Series): Target variable.
    """
    class_counts = target.value_counts()

    plt.figure(figsize=(8, 5))
    sns.barplot(x=class_counts.index, y=class_counts.values, palette="coolwarm")
    plt.title("Class Distribution of Target Variable", fontsize=16)
    plt.xlabel("Classes", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.show()

    print(f"Class Distribution:\n{class_counts}")
    print(f"Class Ratios:\n{class_counts / class_counts.sum() * 100}")


def plot_numerical_distributions(df, numeric_columns):
    """
    Plot the distributions of numerical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        numeric_columns (list): List of numerical column names.
    """
    for col in numeric_columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col].dropna(), kde=True, bins=30, color="skyblue")
        plt.title(f"Distribution of {col}", fontsize=16)
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.show()


def plot_categorical_distributions(df, categorical_columns):
    """
    Plot the distributions of categorical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        categorical_columns (list): List of categorical column names.
    """
    for col in categorical_columns:
        plt.figure(figsize=(8, 5))
        sns.countplot(x=df[col], order=df[col].value_counts().index, palette="muted")
        plt.title(f"Distribution of {col}", fontsize=16)
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Count", fontsize=12)
        plt.xticks(rotation=45)
        plt.show()


def plot_correlation_matrix(df, numeric_columns):
    """
    Plot a heatmap of correlations between numerical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        numeric_columns (list): List of numerical column names.
    """
    corr_matrix = df[numeric_columns].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title("Correlation Matrix", fontsize=16)
    plt.show()


def plot_v_cramer_matrix(df, categorical_columns):
    """
    Plot a heatmap of V Cramer correlations between categorical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        categorical_columns (list): List of categorical column names.
    """
    corr_matrix = calculate_v_cramer(df, categorical_columns)

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix.astype(float), annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title("V Cramer Correlation Matrix", fontsize=16)
    plt.show()


def plot_categorical_cardinality(df, categorical_columns):
    """
    Plot the cardinality (number of unique values) of categorical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        categorical_columns (list): List of categorical column names.
    """
    cardinality = {col: df[col].nunique() for col in categorical_columns}
    cardinality = pd.Series(cardinality).sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=cardinality.values, y=cardinality.index, palette="cool")
    plt.title("Cardinality of Categorical Variables", fontsize=16)
    plt.xlabel("Number of Unique Values", fontsize=12)
    plt.ylabel("Variables", fontsize=12)
    plt.show()



import matplotlib.pyplot as plt
import seaborn as sns

def plot_missing_values(df):
    """
    Plot the percentage of missing values for each column in the dataset.
    Args:
        df (pd.DataFrame): Input dataframe.
    """
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    missing_percentage = missing_percentage[missing_percentage > 0].sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=missing_percentage.values, y=missing_percentage.index, palette="viridis")
    plt.title("Percentage of Missing Values by Column", fontsize=16)
    plt.xlabel("Percentage of Missing Values", fontsize=12)
    plt.ylabel("Columns", fontsize=12)
    plt.show()

def plot_class_distribution(target):
    """
    Plot the distribution of the target variable to visualize class imbalance.
    Args:
        target (pd.Series): Target variable.
    """
    class_counts = target.value_counts()

    plt.figure(figsize=(8, 5))
    sns.barplot(x=class_counts.index, y=class_counts.values, palette="coolwarm")
    plt.title("Class Distribution of Target Variable", fontsize=16)
    plt.xlabel("Classes", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.show()

    print(f"Class Distribution:\n{class_counts}")
    print(f"Class Ratios:\n{class_counts / class_counts.sum() * 100}")


def plot_numerical_distributions(df, numeric_columns):
    """
    Plot the distributions of numerical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        numeric_columns (list): List of numerical column names.
    """
    for col in numeric_columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col].dropna(), kde=True, bins=30, color="skyblue")
        plt.title(f"Distribution of {col}", fontsize=16)
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.show()


def plot_categorical_distributions(df, categorical_columns):
    """
    Plot the distributions of categorical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        categorical_columns (list): List of categorical column names.
    """
    for col in categorical_columns:
        plt.figure(figsize=(8, 5))
        sns.countplot(x=df[col], order=df[col].value_counts().index, palette="muted")
        plt.title(f"Distribution of {col}", fontsize=16)
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Count", fontsize=12)
        plt.xticks(rotation=45)
        plt.show()


def plot_correlation_matrix(df, numeric_columns):
    """
    Plot a heatmap of correlations between numerical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        numeric_columns (list): List of numerical column names.
    """
    corr_matrix = df[numeric_columns].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title("Correlation Matrix", fontsize=16)
    plt.show()


def plot_v_cramer_matrix(df, categorical_columns):
    """
    Plot a heatmap of V Cramer correlations between categorical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        categorical_columns (list): List of categorical column names.
    """
    corr_matrix = calculate_v_cramer(df, categorical_columns)

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix.astype(float), annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title("V Cramer Correlation Matrix", fontsize=16)
    plt.show()


def plot_categorical_cardinality(df, categorical_columns):
    """
    Plot the cardinality (number of unique values) of categorical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        categorical_columns (list): List of categorical column names.
    """
    cardinality = {col: df[col].nunique() for col in categorical_columns}
    cardinality = pd.Series(cardinality).sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=cardinality.values, y=cardinality.index, palette="cool")
    plt.title("Cardinality of Categorical Variables", fontsize=16)
    plt.xlabel("Number of Unique Values", fontsize=12)
    plt.ylabel("Variables", fontsize=12)
    plt.show()



import matplotlib.pyplot as plt
import seaborn as sns

def plot_missing_values(df):
    """
    Plot the percentage of missing values for each column in the dataset.
    Args:
        df (pd.DataFrame): Input dataframe.
    """
    missing_percentage = (df.isnull().sum() / len(df)) * 100
    missing_percentage = missing_percentage[missing_percentage > 0].sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=missing_percentage.values, y=missing_percentage.index, palette="viridis")
    plt.title("Percentage of Missing Values by Column", fontsize=16)
    plt.xlabel("Percentage of Missing Values", fontsize=12)
    plt.ylabel("Columns", fontsize=12)
    plt.show()

def plot_class_distribution(target):
    """
    Plot the distribution of the target variable to visualize class imbalance.
    Args:
        target (pd.Series): Target variable.
    """
    class_counts = target.value_counts()

    plt.figure(figsize=(8, 5))
    sns.barplot(x=class_counts.index, y=class_counts.values, palette="coolwarm")
    plt.title("Class Distribution of Target Variable", fontsize=16)
    plt.xlabel("Classes", fontsize=12)
    plt.ylabel("Frequency", fontsize=12)
    plt.show()

    print(f"Class Distribution:\n{class_counts}")
    print(f"Class Ratios:\n{class_counts / class_counts.sum() * 100}")


def plot_numerical_distributions(df, numeric_columns):
    """
    Plot the distributions of numerical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        numeric_columns (list): List of numerical column names.
    """
    for col in numeric_columns:
        plt.figure(figsize=(8, 5))
        sns.histplot(df[col].dropna(), kde=True, bins=30, color="skyblue")
        plt.title(f"Distribution of {col}", fontsize=16)
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Frequency", fontsize=12)
        plt.show()


def plot_categorical_distributions(df, categorical_columns):
    """
    Plot the distributions of categorical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        categorical_columns (list): List of categorical column names.
    """
    for col in categorical_columns:
        plt.figure(figsize=(8, 5))
        sns.countplot(x=df[col], order=df[col].value_counts().index, palette="muted")
        plt.title(f"Distribution of {col}", fontsize=16)
        plt.xlabel(col, fontsize=12)
        plt.ylabel("Count", fontsize=12)
        plt.xticks(rotation=45)
        plt.show()


def plot_correlation_matrix(df, numeric_columns):
    """
    Plot a heatmap of correlations between numerical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        numeric_columns (list): List of numerical column names.
    """
    corr_matrix = df[numeric_columns].corr()

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix, annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title("Correlation Matrix", fontsize=16)
    plt.show()


def plot_v_cramer_matrix(df, categorical_columns):
    """
    Plot a heatmap of V Cramer correlations between categorical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        categorical_columns (list): List of categorical column names.
    """
    corr_matrix = calculate_v_cramer(df, categorical_columns)

    plt.figure(figsize=(10, 8))
    sns.heatmap(corr_matrix.astype(float), annot=True, fmt=".2f", cmap="coolwarm", square=True)
    plt.title("V Cramer Correlation Matrix", fontsize=16)
    plt.show()


def plot_categorical_cardinality(df, categorical_columns):
    """
    Plot the cardinality (number of unique values) of categorical variables.
    Args:
        df (pd.DataFrame): Input dataframe.
        categorical_columns (list): List of categorical column names.
    """
    cardinality = {col: df[col].nunique() for col in categorical_columns}
    cardinality = pd.Series(cardinality).sort_values(ascending=False)

    plt.figure(figsize=(10, 6))
    sns.barplot(x=cardinality.values, y=cardinality.index, palette="cool")
    plt.title("Cardinality of Categorical Variables", fontsize=16)
    plt.xlabel("Number of Unique Values", fontsize=12)
    plt.ylabel("Variables", fontsize=12)
    plt.show()



