import pandas as pd
import os

# Specify the folder containing all CSV files
folder_path = r"C:\Users\nouri\Documents\Over_releases\resultsRQ1&RQ2&RQ3\new approach\Version22\furthur_analysis\7_projects_Results\pytorch\CSV_files"

# List of features (rows) to extract
selected_features = [
    'CommitMessageSentimentsPositive_count', 
    'CommitMessageSentimentsPositive_mean',
    'CommitMessageSentimentsPositive_stdev',
    'CommitMessageSentimentsNegative_count',
    'CommitMessageSentimentsNegative_mean',
    'CommitMessageSentimentsNegative_stdev',
    'PRCountNegativeComments_count',
    'PRCountNegativeComments_mean',
    'PRCountNegativeComments_stdev',
    'IssueCountNegativeComments_count',
    'IssueCountNegativeComments_mean',
    'IssueCountNegativeComments_stdev'
]

# List to store extracted DataFrames
dataframes = []

# Check if the directory exists
if not os.path.exists(folder_path):
    print(f"❌ Error: The specified folder does not exist: {folder_path}")
else:
    # Loop through all CSV files in the folder
    for file in os.listdir(folder_path):
        if file.endswith(".csv"):  # Ensure it's a CSV file
            file_path = os.path.join(folder_path, file)
            
            try:
                # Load the CSV file
                df = pd.read_csv(file_path, header=None)

                # Transpose the data so rows become columns
                df_transposed = df.T

                # Set the first row as the header
                df_transposed.columns = df_transposed.iloc[0]

                # Remove the first row (now redundant)
                df_transposed = df_transposed[1:]

                # Find which features exist in the current file
                available_features = [col for col in selected_features if col in df_transposed.columns]

                if available_features:
                    # Extract only the required features
                    df_selected = df_transposed[available_features].copy()

                    # Add a column to track the source file
                    df_selected["Source_File"] = file

                    # Append to the list
                    dataframes.append(df_selected)
                else:
                    print(f"⚠️ Warning: No matching rows found in {file}")
            except Exception as e:
                print(f"❌ Error reading {file}: {e}")

    # Combine all extracted data into a single DataFrame
    if dataframes:
        final_df = pd.concat(dataframes, ignore_index=True)

        # Save the final result to a new CSV file
        output_file = os.path.join(folder_path, "extracted_sentiment_features.csv")
        final_df.to_csv(output_file, index=False)

        print(f"✅ Extraction complete! Data saved to: {output_file}")
    else:
        print("❌ No valid data extracted from the CSV files.")
