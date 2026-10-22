import os
import re

all_issues = []
for root, dirs, files in os.walk('src'):
    for file in files:
        if file.endswith('.pine'):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Check shorttitle
            for i, line in enumerate(lines[:15], 1):
                if 'shorttitle' in line:
                    m = re.search(r'shorttitle\s*=\s*"([^"]+)"', line)
                    if m and len(m.group(1)) > 10:
                        all_issues.append((file, i, f'SHORTTITLE_TOO_LONG: "{m.group(1)}" ({len(m.group(1))} chars > 10)'))
            
            # Check line continuation issues
            for i in range(len(lines) - 1):
                raw = lines[i].split('//')[0].rstrip()
                if not raw:
                    continue
                next_line = lines[i+1]
                next_code = next_line.split('//')[0].rstrip()
                if not next_code.strip():
                    continue
                next_indent = len(next_line) - len(next_line.lstrip(' '))
                
                # Check if raw ends with continuation operator and is not a function definition (=>)
                if not raw.endswith('=>') and raw.endswith(('+', '-', '*', '/', '?', ':', 'and', 'or', '==', '!=', '<', '>', '<=', '>=', '=', ':=', ',')):
                    if next_indent % 4 == 0 and next_indent > 0:
                        all_issues.append((file, i+2, f'BAD_CONTINUATION_MULTIPLE_OF_4 ({next_indent} spaces): {next_code.strip()[:60]}'))
                    elif next_indent == 0:
                        all_issues.append((file, i+2, f'BAD_CONTINUATION_ZERO_INDENT: {next_code.strip()[:60]}'))

for issue in all_issues:
    print(f'{issue[0]}:{issue[1]}: {issue[2]}')
