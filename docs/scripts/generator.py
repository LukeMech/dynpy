
import tomllib
import re
from pathlib import Path

def generate_table(strings, var, lang):
    """
    Generate a Markdown-styled table for the given variable from TOML strings.

    Args:
        strings (dict): The loaded TOML data.
        var (str): The variable name (key) in the TOML data.
        lang (str): The language key (e.g., "en", "pl").

    Returns:
        str: A Markdown-styled table as a string.
    """
    table_data = strings[var]
    columns = table_data["columns"]
    rows = table_data["rows"]

    # Generate the Markdown table header based on the language
    header = []
    for col in range(1, columns + 1):
        lang_key = f"{col}_{lang}"
        col_key = str(col)
        if lang_key in table_data:
            header.append(table_data[lang_key])
        elif col_key in table_data:
            header.append(table_data[col_key])
        else:
            header.append(f"Column {col}")  # Fallback for missing headers

    # Create header and separator for Markdown
    header_row = "| " + " | ".join(header) + " |"
    separator_row = "| " + " | ".join(["---"] * columns) + " |"

    # Generate the rows
    md_rows = []
    for row in rows:
        row_data = []
        for col in range(1, columns + 1):
            col_key = str(col)
            lang_key = f"{col}_{lang}"
            # Prioritize language-specific key, fallback to base key
            if lang_key in row:
                row_data.append(row[lang_key])
            elif col_key in row:
                row_data.append(row[col_key])
            else:
                row_data.append("")  # Empty cell
        md_rows.append("| " + " | ".join(row_data) + " |")

    # Combine header, separator, and rows into the full table
    return "\n".join([header_row, separator_row] + md_rows)

def generate_docs():
    # Get base paths
    script_dir = Path(__file__).parent
    template_dir = script_dir.parent/'templates'
    
    # Load TOML strings
    strings_file = template_dir/'strings.toml'
    # Open the file and load the TOML data
    with open(strings_file, 'rb') as f:
        strings = tomllib.load(f)
    
    # Process all files in templates directory
    for template_file in template_dir.rglob('*.md'):

        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
            file_path = script_dir.parent
        
        # For every language
        for lang in strings["variables"]["languages"]:
            lang_content = content
            for var in re.findall(r'\+\+(\w+)\+\+', content):
                if var in strings.keys():
                    if "columns" in strings[var]:  
                        # Call table generator
                        table_md = generate_table(strings, var, lang)
                        lang_content = lang_content.replace(f'++{var}++', table_md)
                    else: 
                        # Just replace with a proper string
                        lang_content = lang_content.replace(f'++{var}++', strings[var][lang].replace("\n", " ").strip())
                elif var in strings["variables"]:
                    # Replace with a variable
                    lang_content = lang_content.replace(f'++{var}++', strings["variables"][var].replace("\n", " ").strip())

            lang_output = file_path / lang / template_file.relative_to(template_dir).parent
            lang_output.mkdir(parents=True, exist_ok=True)
            lang_output = lang_output / f'{template_file.stem}.md'

            with open(lang_output, 'w', encoding='utf-8') as f:
                f.write(lang_content)
            
if __name__ == '__main__':
    generate_docs()