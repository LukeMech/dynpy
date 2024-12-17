
import os
import tomllib
import re
from pathlib import Path

def generate_docs():
    # Get base paths
    script_dir = Path(__file__).parent
    template_dir = script_dir.parent/'templates'
    output_dir = script_dir.parent
    
    # Load TOML strings
    strings_file = template_dir/'strings.toml'
    # Open the file and load the TOML data
    with open(strings_file, 'rb') as f:
        strings = tomllib.load(f)
    
    # Process all files in templates directory
    for template_file in template_dir.rglob('*.md'):

        with open(template_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        # For every language
        for lang in strings["variables"]["languages"]:
            lang_content = content
            for var in re.findall(r'\+\+(\w+)\+\+', content):
                if var in strings.keys():
                    if "columns" in strings[var]:   
                        continue # TODO: Table generator
                    else: lang_content = lang_content.replace(f'++{var}++', strings[var][lang])

            lang_output = output_dir / f'{template_file.stem}_{lang}.md'
            with open(lang_output, 'w', encoding='utf-8') as f:
                f.write(lang_content)
            
if __name__ == '__main__':
    generate_docs()