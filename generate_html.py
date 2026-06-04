#!/usr/bin/env python3
"""
Converts Ultimate_Java_Placement_Handbook.md to Ultimate_Java_Placement_Review_File.html
preserving the exact same design, sidebar, mermaid support, and styling.
"""

import re
import html
import os

# --- Read markdown file ---
md_path = os.path.join(os.path.dirname(__file__), 'Ultimate_Java_Placement_Handbook.md')
with open(md_path, 'r', encoding='utf-8') as f:
    md_text = f.read()

# ─────────────────────────────────────────────────────────────
# Helper: slugify heading text to id
# ─────────────────────────────────────────────────────────────
_id_counters = {}

def slugify(text):
    text = re.sub(r'[^\w\s-]', '', text, flags=re.UNICODE)
    text = text.strip().lower()
    text = re.sub(r'[\s]+', '-', text)
    text = re.sub(r'[^a-z0-9\-]', '', text)
    text = re.sub(r'-+', '-', text).strip('-')
    if text in _id_counters:
        _id_counters[text] += 1
        return f"{text}_{_id_counters[text]}"
    _id_counters[text] = 0
    return text

def escape(text):
    return html.escape(text)

# ─────────────────────────────────────────────────────────────
# Line-by-line markdown → HTML converter
# ─────────────────────────────────────────────────────────────

def inline_md(text):
    """Convert inline markdown (bold, italic, code, links) to HTML."""
    # Escape HTML first but preserve existing entities
    text = text.replace('&', '&amp;').replace('<', '&lt;').replace('>', '&gt;')
    # Code spans (backtick)
    text = re.sub(r'`([^`]+?)`', lambda m: f'<code>{m.group(1)}</code>', text)
    # Bold+italic ***
    text = re.sub(r'\*\*\*(.+?)\*\*\*', r'<strong><em>\1</em></strong>', text)
    # Bold **
    text = re.sub(r'\*\*(.+?)\*\*', r'<strong>\1</strong>', text)
    # Italic *
    text = re.sub(r'\*([^*\n]+?)\*', r'<em>\1</em>', text)
    # Italic _
    text = re.sub(r'_([^_\n]+?)_', r'<em>\1</em>', text)
    # Links [text](url)
    text = re.sub(r'\[([^\]]+)\]\(([^)]+)\)', r'<a href="\2">\1</a>', text)
    # Strikethrough ~~
    text = re.sub(r'~~(.+?)~~', r'<del>\1</del>', text)
    return text


def md_to_html(md_text):
    """Convert full markdown to HTML body content."""
    lines = md_text.split('\n')
    html_parts = []
    
    i = 0
    in_code_block = False
    code_lang = ''
    code_lines = []
    in_table = False
    table_lines = []
    in_blockquote = False
    blockquote_lines = []
    in_list = False
    list_items = []
    list_type = None  # 'ul' or 'ol'
    in_paragraph = False
    para_lines = []
    
    def flush_paragraph():
        nonlocal in_paragraph, para_lines
        if in_paragraph and para_lines:
            content = inline_md(' '.join(para_lines).strip())
            html_parts.append(f'<p>{content}</p>')
        in_paragraph = False
        para_lines = []

    def flush_list():
        nonlocal in_list, list_items, list_type
        if in_list and list_items:
            tag = list_type
            html_parts.append(f'<{tag}>')
            for item in list_items:
                html_parts.append(f'<li>{inline_md(item)}</li>')
            html_parts.append(f'</{tag}>')
        in_list = False
        list_items = []
        list_type = None

    def flush_blockquote():
        nonlocal in_blockquote, blockquote_lines
        if in_blockquote and blockquote_lines:
            # Detect GitHub-style alerts: > [!NOTE], > [!TIP], > [!CAUTION], > [!WARNING], > [!IMPORTANT]
            first = blockquote_lines[0].strip()
            alert_match = re.match(r'\[!(NOTE|TIP|CAUTION|WARNING|IMPORTANT)\]', first, re.IGNORECASE)
            if alert_match:
                alert_type = alert_match.group(1).lower()
                icons = {'note': '📝', 'tip': '💡', 'caution': '🚫', 'warning': '⚠️', 'important': '❗'}
                icon = icons.get(alert_type, '📌')
                body_lines = blockquote_lines[1:]
                content = inline_md(' '.join(l.strip() for l in body_lines).strip())
                html_parts.append(
                    f'<div class="alert alert-{alert_type}">'
                    f'<div class="alert-header">{icon} {alert_type.upper()}</div>'
                    f'<p>{content}</p>'
                    f'</div>'
                )
            else:
                content = inline_md('<br>'.join(l.strip() for l in blockquote_lines))
                html_parts.append(f'<blockquote><p>{content}</p></blockquote>')
        in_blockquote = False
        blockquote_lines = []

    def flush_table():
        nonlocal in_table, table_lines
        if in_table and table_lines:
            html_parts.append('<table>')
            for idx, row in enumerate(table_lines):
                # Skip separator rows (---|--- etc)
                if re.match(r'^[\s|:\-]+$', row):
                    continue
                cols = [c.strip() for c in row.strip('|').split('|')]
                tag = 'th' if idx == 0 else 'td'
                html_parts.append('<tr>')
                for col in cols:
                    html_parts.append(f'<{tag}>{inline_md(col)}</{tag}>')
                html_parts.append('</tr>')
            html_parts.append('</table>')
        in_table = False
        table_lines = []

    def flush_code():
        nonlocal in_code_block, code_lines, code_lang
        lang_class = f' class="language-{code_lang}"' if code_lang else ''
        # Escape HTML in code
        code_content = html.escape('\n'.join(code_lines))
        html_parts.append(
            f'<div class="code-header"><button class="copy-btn" onclick="copyCode(this)">Copy</button></div>'
            f'<pre><code{lang_class}>{code_content}\n</code></pre>'
        )
        in_code_block = False
        code_lines = []
        code_lang = ''

    while i < len(lines):
        line = lines[i]
        raw = line

        # ── Code fence ──────────────────────────────────────────────
        if line.startswith('```'):
            flush_paragraph()
            flush_list()
            flush_blockquote()
            flush_table()
            if not in_code_block:
                in_code_block = True
                code_lang = line[3:].strip()
            else:
                flush_code()
            i += 1
            continue

        if in_code_block:
            code_lines.append(raw)
            i += 1
            continue

        # ── Horizontal rule ─────────────────────────────────────────
        if re.match(r'^---+$', line.strip()) or re.match(r'^===+$', line.strip()):
            flush_paragraph()
            flush_list()
            flush_blockquote()
            flush_table()
            html_parts.append('<hr/>')
            i += 1
            continue

        # ── Headings ────────────────────────────────────────────────
        heading_match = re.match(r'^(#{1,6})\s+(.*)', line)
        if heading_match:
            flush_paragraph()
            flush_list()
            flush_blockquote()
            flush_table()
            level = len(heading_match.group(1))
            text = heading_match.group(2).strip()
            slug = slugify(re.sub(r'[^\w\s]', '', text))
            html_parts.append(f'<h{level} id="{slug}">{inline_md(text)}</h{level}>')
            i += 1
            continue

        # ── Blockquote ──────────────────────────────────────────────
        if line.startswith('>'):
            flush_paragraph()
            flush_list()
            flush_table()
            content = line[1:].lstrip()
            if not in_blockquote:
                in_blockquote = True
                blockquote_lines = []
            # Detect the alert marker line
            if content.strip().startswith('[!'):
                blockquote_lines.append(content.strip())
            else:
                blockquote_lines.append(content)
            i += 1
            continue
        else:
            if in_blockquote:
                flush_blockquote()

        # ── Table row ───────────────────────────────────────────────
        if line.strip().startswith('|') and '|' in line.strip()[1:]:
            flush_paragraph()
            flush_list()
            if not in_table:
                in_table = True
                table_lines = []
            table_lines.append(line.strip())
            i += 1
            continue
        else:
            if in_table:
                flush_table()

        # ── Unordered list ──────────────────────────────────────────
        ul_match = re.match(r'^(\s*)[-*+]\s+(.*)', line)
        if ul_match:
            flush_paragraph()
            flush_blockquote()
            flush_table()
            if not in_list or list_type != 'ul':
                flush_list()
                in_list = True
                list_type = 'ul'
            list_items.append(ul_match.group(2))
            i += 1
            continue

        # ── Ordered list ────────────────────────────────────────────
        ol_match = re.match(r'^\d+\.\s+(.*)', line)
        if ol_match:
            flush_paragraph()
            flush_blockquote()
            flush_table()
            if not in_list or list_type != 'ol':
                flush_list()
                in_list = True
                list_type = 'ol'
            list_items.append(ol_match.group(1))
            i += 1
            continue

        # ── Empty line ──────────────────────────────────────────────
        if not line.strip():
            flush_paragraph()
            flush_list()
            flush_blockquote()
            flush_table()
            i += 1
            continue

        # ── Paragraph ───────────────────────────────────────────────
        # Flush list/blockquote if we hit normal text
        if in_list:
            flush_list()
        if in_blockquote:
            flush_blockquote()
        if in_table:
            flush_table()
        in_paragraph = True
        para_lines.append(line.strip())
        i += 1

    # Flush any remaining
    flush_paragraph()
    flush_list()
    flush_blockquote()
    flush_table()
    if in_code_block:
        flush_code()

    return '\n'.join(html_parts)


# ─────────────────────────────────────────────────────────────
# Build TOC from headings
# ─────────────────────────────────────────────────────────────

def build_toc(md_text):
    """Build sidebar navigation HTML from headings."""
    headings = []
    in_code = False
    for line in md_text.split('\n'):
        if line.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r'^(#{1,3})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            clean = re.sub(r'[^\w\s]', '', text)
            slug = slugify(clean)
            headings.append((level, text, slug))

    # Reset slug counter to get consistent ids
    toc_html = []
    i = 0
    while i < len(headings):
        level, text, slug = headings[i]
        if level == 1:
            # Start H1 group
            toc_html.append(f'<li class="toc-h1"><a href="#{slug}">{escape(text)}</a>')
            # Collect H2 children
            children = []
            j = i + 1
            while j < len(headings) and headings[j][0] > 1:
                if headings[j][0] == 2:
                    children.append(headings[j])
                j += 1
            if children:
                toc_html.append('<ul class="nav-sublinks">')
                for _, ct, cs in children:
                    toc_html.append(f'<li class="toc-h2"><a href="#{cs}">{escape(ct)}</a></li>')
                toc_html.append('</ul>')
            toc_html.append('</li>')
            # Skip to next H1
            i = j
        else:
            i += 1
    return ''.join(toc_html)


# ─────────────────────────────────────────────────────────────
# Main: generate full HTML
# ─────────────────────────────────────────────────────────────

print("Converting Markdown to HTML...")
content_html = md_to_html(md_text)

# Build TOC (reset slug counter first so it matches content IDs)
_id_counters.clear()
# Re-slug for TOC must use a fresh pass - build toc using a separate fresh slugify
toc_heading_slugs = {}
_toc_id_counters = {}

def toc_slugify(text):
    text = re.sub(r'[^\w\s-]', '', text, flags=re.UNICODE)
    text = text.strip().lower()
    text = re.sub(r'[\s]+', '-', text)
    text = re.sub(r'[^a-z0-9\-]', '', text)
    text = re.sub(r'-+', '-', text).strip('-')
    if text in _toc_id_counters:
        _toc_id_counters[text] += 1
        return f"{text}_{_toc_id_counters[text]}"
    _toc_id_counters[text] = 0
    return text

def build_toc_v2(md_text):
    headings = []
    in_code = False
    for line in md_text.split('\n'):
        if line.startswith('```'):
            in_code = not in_code
            continue
        if in_code:
            continue
        m = re.match(r'^(#{1,3})\s+(.*)', line)
        if m:
            level = len(m.group(1))
            text = m.group(2).strip()
            clean = re.sub(r'[^\w\s]', '', text)
            slug = toc_slugify(clean)
            headings.append((level, text, slug))

    toc_html = []
    i = 0
    while i < len(headings):
        level, text, slug = headings[i]
        if level == 1:
            toc_html.append(f'<li class="toc-h1"><a href="#{slug}">{escape(text)}</a>')
            children = []
            j = i + 1
            while j < len(headings) and headings[j][0] > 1:
                if headings[j][0] == 2:
                    children.append(headings[j])
                j += 1
            if children:
                toc_html.append('<ul class="nav-sublinks">')
                for _, ct, cs in children:
                    toc_html.append(f'<li class="toc-h2"><a href="#{cs}">{escape(ct)}</a></li>')
                toc_html.append('</ul>')
            toc_html.append('</li>')
            i = j
        else:
            i += 1
    return ''.join(toc_html)

toc_html = build_toc_v2(md_text)

full_html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>The Ultimate Java Placement Review File</title>
    <meta name="description" content="Complete Java Placement Handbook - Comprehensive guide for technical interviews covering Java fundamentals, OOP, Collections, Multithreading, Design Patterns and more.">
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Outfit:wght@400;500;600;700&family=Fira+Code:wght@400;500&display=swap" rel="stylesheet">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/styles/vs2015.min.css">
    <style>
        :root {{
            --bg-color: #f8fafc;
            --surface-color: #ffffff;
            --text-color: #334155;
            --text-heading: #0f172a;
            --primary: #2563eb;
            --primary-hover: #1d4ed8;
            --border-color: #e2e8f0;
            --sidebar-bg: #0f172a;
            --sidebar-text: #94a3b8;
            --sidebar-text-hover: #f8fafc;
            --code-bg: #1e1e1e;
        }}
        [data-theme="dark"] {{
            --bg-color: #0f172a;
            --surface-color: #1e293b;
            --text-color: #cbd5e1;
            --text-heading: #f8fafc;
            --primary: #3b82f6;
            --primary-hover: #60a5fa;
            --border-color: #334155;
            --sidebar-bg: #020617;
            --sidebar-text: #64748b;
            --sidebar-text-hover: #cbd5e1;
        }}
        * {{ box-sizing: border-box; margin: 0; padding: 0; }}
        body {{
            font-family: 'Inter', sans-serif;
            background-color: var(--bg-color);
            color: var(--text-color);
            line-height: 1.6;
            display: flex;
        }}
        .sidebar {{
            width: 280px;
            height: 100vh;
            background-color: var(--sidebar-bg);
            color: var(--sidebar-text);
            position: fixed;
            top: 0;
            left: 0;
            overflow-y: auto;
            border-right: 1px solid var(--border-color);
            z-index: 100;
            transition: all 0.3s ease;
        }}
        .sidebar-brand {{
            padding: 24px;
            font-family: 'Outfit', sans-serif;
            font-size: 1.25rem;
            font-weight: 700;
            color: #ffffff;
            border-bottom: 1px solid #1e293b;
        }}
        .nav-links {{ list-style: none; padding: 16px 0; }}
        .nav-links a {{
            display: block;
            padding: 8px 24px;
            color: var(--sidebar-text);
            text-decoration: none;
            font-size: 0.875rem;
            font-weight: 500;
            transition: all 0.2s ease;
        }}
        .nav-links a:hover, .nav-links li.active > a {{
            color: var(--sidebar-text-hover);
            background-color: #1e293b;
        }}
        .nav-sublinks {{ list-style: none; padding-left: 12px; display: none; }}
        .toc-h1:hover .nav-sublinks, .toc-h1.active .nav-sublinks {{ display: block; }}
        .nav-sublinks a {{ padding: 6px 24px; font-size: 0.775rem; opacity: 0.8; }}
        .content-wrapper {{
            margin-left: 280px;
            width: calc(100% - 280px);
            padding: 40px 60px;
            background-color: var(--bg-color);
            min-height: 100vh;
            transition: all 0.3s ease;
        }}
        .container {{
            max-width: 1000px;
            margin: 0 auto;
            background-color: var(--surface-color);
            padding: 50px;
            border-radius: 12px;
            box-shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            border: 1px solid var(--border-color);
        }}
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Outfit', sans-serif;
            color: var(--text-heading);
            font-weight: 700;
            margin-top: 1.5em;
            margin-bottom: 0.5em;
            line-height: 1.25;
        }}
        h1 {{
            font-size: 2.25rem;
            border-bottom: 2px solid var(--border-color);
            padding-bottom: 12px;
            margin-top: 2em;
        }}
        h2 {{
            font-size: 1.75rem;
            border-bottom: 1px solid var(--border-color);
            padding-bottom: 8px;
        }}
        h3 {{ font-size: 1.35rem; }}
        h4 {{ font-size: 1.1rem; }}
        p, ul, ol, blockquote, pre {{ margin-bottom: 1.25em; }}
        li {{ margin-left: 24px; }}
        hr {{ border: 0; height: 1px; background-color: var(--border-color); margin: 40px 0; }}
        code {{
            font-family: 'Fira Code', monospace;
            font-size: 0.875em;
            background-color: #f1f5f9;
            color: #0f172a;
            padding: 2px 6px;
            border-radius: 4px;
        }}
        [data-theme="dark"] code {{ background-color: #334155; color: #f8fafc; }}
        pre code {{ background-color: transparent !important; color: inherit !important; padding: 0; font-size: 0.9em; }}
        pre {{
            background-color: var(--code-bg);
            color: #f8fafc;
            border-radius: 8px;
            padding: 20px;
            overflow-x: auto;
            border: 1px solid #334155;
            position: relative;
        }}
        .code-header {{ display: flex; justify-content: flex-end; margin-bottom: -15px; padding-right: 10px; }}
        .copy-btn {{
            background: transparent;
            border: 1px solid #475569;
            color: #94a3b8;
            padding: 4px 8px;
            font-size: 0.75rem;
            border-radius: 4px;
            cursor: pointer;
            transition: all 0.2s ease;
            z-index: 10;
        }}
        .copy-btn:hover {{ background-color: #334155; color: #f8fafc; }}
        table {{ width: 100%; border-collapse: collapse; margin: 24px 0; font-size: 0.9rem; }}
        th, td {{ padding: 12px 16px; border: 1px solid var(--border-color); text-align: left; }}
        th {{ background-color: #1e293b; color: #ffffff; font-weight: 600; }}
        [data-theme="dark"] th {{ background-color: #0f172a; }}
        tr:nth-child(even) {{ background-color: #f8fafc; }}
        [data-theme="dark"] tr:nth-child(even) {{ background-color: #1e293b; }}
        .alert {{ padding: 16px 20px; margin: 24px 0; border-left: 4px solid; border-radius: 4px; font-size: 0.95rem; }}
        .alert-header {{ font-family: 'Outfit', sans-serif; font-weight: 700; margin-bottom: 8px; text-transform: uppercase; font-size: 0.8rem; letter-spacing: 0.05em; }}
        .alert-note {{ background-color: #eff6ff; border-color: #2563eb; color: #1e40af; }}
        [data-theme="dark"] .alert-note {{ background-color: #172554; color: #dbeafe; }}
        .alert-tip {{ background-color: #ecfdf5; border-color: #059669; color: #065f46; }}
        [data-theme="dark"] .alert-tip {{ background-color: #022c22; color: #a7f3d0; }}
        .alert-important {{ background-color: #faf5ff; border-color: #8b5cf6; color: #5b21b6; }}
        [data-theme="dark"] .alert-important {{ background-color: #2e1065; color: #e9d5ff; }}
        .alert-warning {{ background-color: #fffbeb; border-color: #d97706; color: #92400e; }}
        [data-theme="dark"] .alert-warning {{ background-color: #451a03; color: #fef3c7; }}
        .alert-caution {{ background-color: #fff1f2; border-color: #e11d48; color: #9f1239; }}
        [data-theme="dark"] .alert-caution {{ background-color: #4c0519; color: #ffe4e6; }}
        .header-controls {{ position: fixed; top: 20px; right: 20px; display: flex; gap: 12px; z-index: 1000; }}
        .control-btn {{
            background-color: var(--surface-color);
            border: 1px solid var(--border-color);
            color: var(--text-color);
            padding: 8px 16px;
            border-radius: 6px;
            cursor: pointer;
            font-size: 0.875rem;
            font-weight: 500;
            display: flex;
            align-items: center;
            gap: 6px;
            box-shadow: 0 1px 3px 0 rgb(0 0 0 / 0.1);
            transition: all 0.2s ease;
        }}
        .control-btn:hover {{ background-color: var(--border-color); }}
        .mermaid {{
            background: white !important;
            padding: 20px;
            border-radius: 8px;
            border: 1px solid var(--border-color);
            margin: 20px 0;
            display: flex;
            justify-content: center;
        }}
        blockquote {{
            border-left: 4px solid var(--primary);
            padding: 12px 20px;
            margin: 20px 0;
            background-color: #f8fafc;
            border-radius: 0 4px 4px 0;
        }}
        [data-theme="dark"] blockquote {{ background-color: #1e293b; }}
        @media print {{
            .sidebar, .header-controls, .code-header, .copy-btn {{ display: none !important; }}
            .content-wrapper {{ margin-left: 0 !important; width: 100% !important; padding: 0 !important; }}
            .container {{ box-shadow: none !important; border: none !important; padding: 0 !important; max-width: 100% !important; }}
            body {{ background-color: #ffffff !important; color: #000000 !important; }}
            h1, h2, h3, h4, h5, h6 {{ page-break-after: avoid; color: #000000 !important; }}
            pre {{ page-break-inside: avoid; background-color: #f8fafc !important; color: #000000 !important; border: 1px solid #cbd5e1 !important; }}
            code {{ background-color: #f1f5f9 !important; color: #000000 !important; }}
            tr {{ page-break-inside: avoid !important; }}
            .alert {{ page-break-inside: avoid; background-color: #f8fafc !important; border-left-width: 6px !important; }}
        }}
    </style>
    <script type="module">
        import mermaid from 'https://cdn.jsdelivr.net/npm/mermaid@10/dist/mermaid.esm.min.mjs';
        window.mermaid = mermaid;
    </script>
</head>
<body>
    <div class="header-controls">
        <button class="control-btn" id="theme-toggle">🌓 Toggle Theme</button>
        <button class="control-btn" id="print-btn" onclick="window.print()">🖨️ Export / Print</button>
    </div>
    <div class="sidebar">
        <div class="sidebar-brand">Java Handbook</div>
        <ul class="nav-links">
{toc_html}
        </ul>
    </div>
    <div class="content-wrapper">
        <div class="container">
{content_html}
        </div>
    </div>
    <script src="https://cdnjs.cloudflare.com/ajax/libs/highlight.js/11.9.0/highlight.min.js"></script>
    <script>
        // Theme toggle
        const themeToggle = document.getElementById('theme-toggle');
        const savedTheme = localStorage.getItem('theme') || 'light';
        if (savedTheme === 'dark') document.documentElement.setAttribute('data-theme', 'dark');
        themeToggle.addEventListener('click', () => {{
            const isDark = document.documentElement.getAttribute('data-theme') === 'dark';
            document.documentElement.setAttribute('data-theme', isDark ? 'light' : 'dark');
            localStorage.setItem('theme', isDark ? 'light' : 'dark');
        }});

        // Highlight.js for non-mermaid code blocks
        document.addEventListener('DOMContentLoaded', () => {{
            document.querySelectorAll('pre code:not(.language-mermaid)').forEach(block => {{
                hljs.highlightElement(block);
            }});
        }});

        // Mermaid rendering
        document.addEventListener('DOMContentLoaded', async () => {{
            if (window.mermaid) {{
                window.mermaid.initialize({{ startOnLoad: false, theme: 'default' }});
                const mermaidBlocks = document.querySelectorAll('code.language-mermaid');
                for (const block of mermaidBlocks) {{
                    const pre = block.parentElement;
                    const div = document.createElement('div');
                    div.className = 'mermaid';
                    div.textContent = block.textContent;
                    pre.replaceWith(div);
                }}
                await window.mermaid.run();
            }}
        }});

        // Copy code button
        function copyCode(btn) {{
            const code = btn.closest('.code-header').nextElementSibling.querySelector('code');
            navigator.clipboard.writeText(code.textContent).then(() => {{
                btn.textContent = 'Copied!';
                setTimeout(() => btn.textContent = 'Copy', 2000);
            }});
        }}
        window.copyCode = copyCode;

        // Sidebar active highlighting on scroll
        const headings = document.querySelectorAll('h1[id], h2[id]');
        const observer = new IntersectionObserver(entries => {{
            entries.forEach(entry => {{
                if (entry.isIntersecting) {{
                    document.querySelectorAll('.nav-links li').forEach(li => li.classList.remove('active'));
                    const link = document.querySelector(`.nav-links a[href="#${{entry.target.id}}"]`);
                    if (link) link.closest('li.toc-h1, li.toc-h2')?.classList.add('active');
                }}
            }});
        }}, {{ rootMargin: '0px 0px -70% 0px' }});
        headings.forEach(h => observer.observe(h));
    </script>
</body>
</html>'''

out_path = os.path.join(os.path.dirname(__file__), 'Ultimate_Java_Placement_Review_File.html')
with open(out_path, 'w', encoding='utf-8') as f:
    f.write(full_html)

print(f"Done! HTML file written to: {out_path}")
print(f"   Lines: {len(full_html.splitlines())}")
print(f"   Size: {len(full_html.encode('utf-8')) / 1024:.1f} KB")
