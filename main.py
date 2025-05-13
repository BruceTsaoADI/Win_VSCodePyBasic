import package.searcher_pptx as searcher_pptx

# Define the folder containing PPTX files
pptx_folder = r"C:\Users\btsao\OneDrive - Analog Devices, Inc\Documents\BruceTsao\02_Document\ADI\WeeklyReport"

# Get keywords from user input
keywords = input("Enter keywords to search (comma-separated): ").split(",")
keywords = [kw.strip() for kw in keywords]  # Remove extra spaces

# Ask user if search should be case-sensitive
case_sensitive = input("Enable case-sensitive search? (y/n): ").lower() == "y"

# Ask user if results should be saved to TXT
save_txt = input("Save results to TXT file? (y/n): ").lower() == "y"

# Perform the search
results = searcher_pptx.search_pptx_keywords(pptx_folder, keywords, case_sensitive=case_sensitive, save_to_txt=save_txt)

# Display results
if results:
    print("\nSearch results:")
    for result in results:
        print(f"{result[0]} - Slide {result[1]} - Keyword: {result[2]}")
else:
    print("No matches found.")
