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

            # Check duplicate title arguments in plot, plotshape, plotchar
            content = ''.join(lines)
            for m in re.finditer(r'(?:^|[^a-zA-Z0-9_.])(plot|plotshape|plotchar)\s*\(([^;]+?)\)', content):
                fn = m.group(1)
                args_str = m.group(2)
                args = []
                cur = []
                depth = 0
                in_str = False
                quote_char = ''
                for c in args_str:
                    if c in ('"', "'"):
                        if not in_str:
                            in_str = True
                            quote_char = c
                        elif quote_char == c:
                            in_str = False
                    elif c == '(' and not in_str:
                        depth += 1
                    elif c == ')' and not in_str:
                        depth -= 1
                    elif c == ',' and depth == 0 and not in_str:
                        args.append(''.join(cur).strip())
                        cur = []
                        continue
                    cur.append(c)
                if cur:
                    args.append(''.join(cur).strip())
                
                # In plot(): series, title, color, ...
                # In plotshape(): series, title, style, ...
                # In plotchar(): series, title, char, ...
                # If args[1] is a string literal (not starting with param_name=), that is positional title!
                has_pos_title = len(args) > 1 and not ('=' in args[1].split('?')[0]) and (args[1].startswith('"') or args[1].startswith("'"))
                has_kw_title = any(re.match(r'^title\s*=', a) for a in args)
                if has_pos_title and has_kw_title:
                    all_issues.append((file, 0, f'DUPLICATE_TITLE_PARAM: {fn} has both positional "{args[1]}" and keyword title'))

for issue in all_issues:
    print(f'{issue[0]}:{issue[1]}: {issue[2]}')
