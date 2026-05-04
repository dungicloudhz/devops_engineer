import glob

for filepath in glob.glob("*.html"):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
        
    old_str = """  <div class="sb-progress">
    <div class="sb-progress-label"><span>Tiến độ đọc</span><span id="prog-pct">0%</span></div>
    <div class="sb-progress-bar"><div class="sb-progress-fill" id="prog-fill"></div></div>

  <div class="sb-section">
    <div class="sb-section-label">📚 Series DevOps</div>"""
    
    new_str = """  <div class="sb-progress">
    <div class="sb-progress-label"><span>Tiến độ đọc</span><span id="prog-pct">0%</span></div>
    <div class="sb-progress-bar"><div class="sb-progress-fill" id="prog-fill"></div></div>
  </div>

  <div class="sb-section">
    <div class="sb-section-label">📚 Series DevOps</div>"""
    
    if old_str in content:
        print(f"Fixing {filepath}")
        content = content.replace(old_str, new_str)
        # Also need to remove the stray </div> after the new sb-section
        # The stray </div> is right before the NEXT <div class="sb-section">
        # Let's just find the first `  </div>\n\n  <div class="sb-section">`
        # Wait, the structure was:
        # <div class="sb-section"> ... </div> \n  </div> \n\n  <div class="sb-section">
        
        # We can find `  </div>\n  </div>\n\n  <div class="sb-section">`
        # and replace with `  </div>\n\n  <div class="sb-section">`
        
        content = content.replace('  </div>\n  </div>\n\n  <div class="sb-section">', '  </div>\n\n  <div class="sb-section">')
        
        # What if it's right before <div class="sb-footer">?
        content = content.replace('  </div>\n  </div>\n\n  <div class="sb-footer">', '  </div>\n\n  <div class="sb-footer">')

        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(content)
