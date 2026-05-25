import os
import re

TEMPLATE_DIR = 'templates'

# 1. Add meta tag to base.html
base_files = ['templates/base.html', 'templates/admin/base.html']
for bp in base_files:
    if os.path.exists(bp):
        with open(bp, 'r') as f:
            content = f.read()
        if 'name="csrf-token"' not in content:
            # Find <head> and inject
            content = content.replace('<head>', '<head>\n    <meta name="csrf-token" content="{{ csrf_token() }}">')
            with open(bp, 'w') as f:
                f.write(content)
            print(f"Added CSRF meta tag to {bp}")

# 2. Add hidden inputs to all POST forms
form_regex = re.compile(r'(<form[^>]*method=["\']POST["\'][^>]*>)', re.IGNORECASE)
for root, dirs, files in os.walk(TEMPLATE_DIR):
    for name in files:
        if name.endswith('.html'):
            filepath = os.path.join(root, name)
            with open(filepath, 'r') as f:
                content = f.read()
            
            if form_regex.search(content) and 'csrf_token()' not in content:
                # Add hidden input right after form opening tag
                content = form_regex.sub(r'\1\n    <input type="hidden" name="csrf_token" value="{{ csrf_token() }}"/>', content)
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Injected CSRF form token into {filepath}")

# 3. Add CSRF token header to fetch calls
# We need to look for headers: { ... } in fetch calls and add 'X-CSRFToken'
fetch_headers_regex = re.compile(r'headers:\s*\{([^}]*)\}', re.IGNORECASE)

def inject_fetch_csrf(match):
    headers_content = match.group(1)
    if 'X-CSRFToken' not in headers_content:
        # Add the token
        if headers_content.strip() == '':
            return 'headers: {\n                "X-CSRFToken": document.querySelector(\'meta[name="csrf-token"]\')?.getAttribute(\'content\')\n            }'
        else:
            return f'headers: {{{headers_content}, \n                "X-CSRFToken": document.querySelector(\'meta[name="csrf-token"]\')?.getAttribute(\'content\')}}'
    return match.group(0)

for root, dirs, files in os.walk(TEMPLATE_DIR):
    for name in files:
        if name.endswith('.html') or name.endswith('.js'):
            filepath = os.path.join(root, name)
            with open(filepath, 'r') as f:
                content = f.read()
            
            if 'fetch(' in content and 'headers:' in content and 'X-CSRFToken' not in content:
                content = fetch_headers_regex.sub(inject_fetch_csrf, content)
                with open(filepath, 'w') as f:
                    f.write(content)
                print(f"Injected CSRF header into fetch calls in {filepath}")

print("CSRF Injection complete.")
