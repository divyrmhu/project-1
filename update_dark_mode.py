import os
import re

files = [
    r'c:\Users\DIVYANSH\Desktop\project-1\index.html',
    r'c:\Users\DIVYANSH\Desktop\project-1\datastructure.html',
    r'c:\Users\DIVYANSH\Desktop\project-1\electronics.html'
]

# Tailwind config script to be added right after the tailwind script
head_injection = """
    <script>
        tailwind.config = {
            darkMode: 'class',
            theme: {
                extend: {}
            }
        }
    </script>
    <script>
        if (localStorage.getItem('theme') === 'light') {
            document.documentElement.classList.remove('dark');
        } else {
            document.documentElement.classList.add('dark');
        }

        function toggleTheme() {
            if (document.documentElement.classList.contains('dark')) {
                document.documentElement.classList.remove('dark');
                localStorage.setItem('theme', 'light');
            } else {
                document.documentElement.classList.add('dark');
                localStorage.setItem('theme', 'dark');
            }
        }
    </script>
"""

class_replacements = {
    r'bg-slate-50(?![\w-])': r'bg-slate-50 dark:bg-slate-900',
    r'text-slate-800(?![\w-])': r'text-slate-800 dark:text-slate-200',
    r'bg-white(?![\w-])': r'bg-white dark:bg-slate-800',
    r'border-slate-200(?![\w-])': r'border-slate-200 dark:border-slate-700',
    r'border-slate-100(?![\w-])': r'border-slate-100 dark:border-slate-700',
    r'text-slate-500(?![\w-])': r'text-slate-500 dark:text-slate-400',
    r'bg-slate-100(?![\w-])': r'bg-slate-100 dark:bg-slate-700',
    r'text-slate-900(?![\w-])': r'text-slate-900 dark:text-slate-100',
    r'text-slate-400(?![\w-])': r'text-slate-400 dark:text-slate-500',
    r'text-slate-700(?![\w-])': r'text-slate-700 dark:text-slate-300',

    r'bg-blue-50(?![\w-])': r'bg-blue-50 dark:bg-blue-900/30',
    r'bg-emerald-50(?![\w-])': r'bg-emerald-50 dark:bg-emerald-900/30',
    r'bg-purple-50(?![\w-])': r'bg-purple-50 dark:bg-purple-900/30',
    r'bg-amber-50(?![\w-])': r'bg-amber-50 dark:bg-amber-900/30',
    r'bg-teal-50(?![\w-])': r'bg-teal-50 dark:bg-teal-900/30',
    r'bg-indigo-50(?![\w-])': r'bg-indigo-50 dark:bg-indigo-900/30',

    r'text-blue-600(?![\w-])': r'text-blue-600 dark:text-blue-400',
    r'text-emerald-600(?![\w-])': r'text-emerald-600 dark:text-emerald-400',
    r'text-purple-600(?![\w-])': r'text-purple-600 dark:text-purple-400',
    r'text-amber-600(?![\w-])': r'text-amber-600 dark:text-amber-400',
    r'text-teal-600(?![\w-])': r'text-teal-600 dark:text-teal-400',
    r'text-indigo-600(?![\w-])': r'text-indigo-600 dark:text-indigo-400',

    r'text-teal-700(?![\w-])': r'text-teal-700 dark:text-teal-300',
    r'text-indigo-700(?![\w-])': r'text-indigo-700 dark:text-indigo-300',
    r'text-indigo-800(?![\w-])': r'text-indigo-800 dark:text-indigo-200',
    
    r'border-blue-100(?![\w-])': r'border-blue-100 dark:border-blue-800',
    r'border-blue-200(?![\w-])': r'border-blue-200 dark:border-blue-700',
    r'border-teal-200(?![\w-])': r'border-teal-200 dark:border-teal-700',
    r'border-teal-100(?![\w-])': r'border-teal-100 dark:border-teal-800',
    
    r'text-teal-800(?![\w-])': r'text-teal-800 dark:text-teal-200',
    r'bg-[#1e293b](?![\w-])': r'bg-[#1e293b] dark:bg-[#0f172a]',
    r'border\s*(?!-)': r'border dark:border-slate-700 ',
}

for filepath in files:
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Apply class replacements
    for pattern, replacement in class_replacements.items():
        # Using regex effectively, only replace if not already containing dark variant
        content = re.sub(pattern + r'(?!\s*dark:)', replacement, content)

    # 1. Add <html lang="en" class="dark">
    content = re.sub(r'<html lang="en">', '<html lang="en" class="dark">', content)
    content = re.sub(r'<html lang="en" class="dark"\s+class="dark">', '<html lang="en" class="dark">', content)

    # 2. Inject Tailwind Config
    if "tailwind.config" not in content:
        content = re.sub(r'</head>', head_injection + '\n</head>', content)

    # 3. Add styles for trace-table in dark mode (optional, but good for table backgrounds)
    if 'trace-table th' in content:
        style_addition = '''
        .dark .trace-table th { background-color: #1e293b; color: #cbd5e1; }
        .dark .trace-table tr:nth-child(even) { background-color: #0f172a; }
        .dark .trace-table td { border-color: #334155; }
        .dark .trace-table th { border-color: #334155; }
        '''
        if '.dark .trace-table th' not in content:
            content = re.sub(r'</style>', style_addition + '\n    </style>', content)

    # 4. Inject Toggle Button
    toggle_btn_index = """
    <div class="fixed top-4 right-4 z-50">
        <button onclick="toggleTheme()" class="p-2 bg-slate-200 dark:bg-slate-700 rounded-full text-slate-800 dark:text-slate-200 shadow hover:bg-slate-300 dark:hover:bg-slate-600 transition-colors">
            🌓
        </button>
    </div>
    """
    toggle_btn_header = """
            <button onclick="toggleTheme()" class="absolute top-4 right-4 inline-flex items-center gap-2 bg-white/20 hover:bg-white/30 text-white px-4 py-2 rounded-lg backdrop-blur-sm transition-all duration-200 text-sm font-semibold">
                🌓 Toggle Dark
            </button>
    """

    if "toggleTheme()" not in content:
        if "index.html" in filepath:
            content = re.sub(r'<body[^>]*>', lambda m: m.group(0) + toggle_btn_index, content)
        else:
            # find <header class="..."> and insert button
            content = re.sub(r'(<header[^>]*>)', lambda m: m.group(1) + toggle_btn_header, content)
            
    # Remove any extra border dark:border-slate-700 dark:border-slate-700
    content = re.sub(r'dark:border-slate-700\s*dark:border-slate-700', 'dark:border-slate-700', content)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)

print("Done processing files")
