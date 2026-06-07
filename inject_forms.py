import os
import re

TEMPLATE_DIR = 'templates'

modified_count = 0
for root, dirs, files in os.walk(TEMPLATE_DIR):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r') as f:
                content = f.read()
            
            # Simple heuristic: inject if <form> is present and no csrf_token exists
            if '<form' in content.lower() and 'name="csrf_token"' not in content:
                content = re.sub(
                    r'(<form[^>]*>)', 
                    r'\1\n    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>', 
                    content, 
                    flags=re.IGNORECASE
                )
                with open(filepath, 'w') as f:
                    f.write(content)
                modified_count += 1
                print(f"Injected CSRF form into {filepath}")

print(f"Done. Modified {modified_count} HTML files containing forms.")
