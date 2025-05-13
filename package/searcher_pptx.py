import os
from pptx import Presentation

def search_pptx_keywords(folder_path, keywords, case_sensitive=False, save_to_txt=False):
    """
    Search for keywords in all PPTX files within a specified folder.

    :param folder_path: str, the directory containing PPTX files
    :param keywords: list, the list of keywords to search for
    :param case_sensitive: bool, whether the search should be case-sensitive
    :param save_to_txt: bool, whether to save results to a TXT file
    :return: list, containing (filename, slide number, keyword, text snippet)
    """
    results = []

    # Convert keywords to lowercase if case-insensitive search is enabled
    if not case_sensitive:
        keywords = [kw.lower() for kw in keywords]

    for filename in os.listdir(folder_path):
        if filename.endswith(".pptx"):
            file_path = os.path.join(folder_path, filename)
            
            # Ensure the file exists before opening
            if not os.path.exists(file_path):
                print(f"File not found or not downloaded: {file_path}")
                continue

            try:
                presentation = Presentation(file_path)
            except Exception as e:
                print(f"Could not read {filename}. Possible corrupted file: {e}")
                continue  # Skip this file and proceed to the next one

            for i, slide in enumerate(presentation.slides):
                for shape in slide.shapes:
                    if hasattr(shape, "text"):
                        text = shape.text
                        text_lower = text.lower() if not case_sensitive else text  # Convert text if needed

                        for keyword in keywords:
                            if keyword in text_lower:
                                results.append((filename, i + 1, keyword, text[:50]))  # Store first 50 chars
                                print(f"Match found: {filename} | Slide {i+1} | Keyword: {keyword}")

    # Save results to TXT if enabled
    if save_to_txt and results:
        txt_path = os.path.join(folder_path, "search_results.txt")
        with open(txt_path, "w", encoding="utf-8") as f:
            for result in results:
                f.write(f"{result[0]} - Slide {result[1]} - Keyword: {result[2]} - Text: {result[3]}\n")
        print(f"Search results saved to: {txt_path}")

    return results
