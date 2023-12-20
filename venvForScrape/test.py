import re

# The regular expression pattern to match email addresses
pattern = r"[a-zA-Z0-9\.\-+_]+@[a-zA-Z0-9\.\-+_]+\.[a-z]+"

# The text you want to search for email addresses in
text = """<p>Orders Over $200 require a signature upon delivery as a protection against lost or stolen packages. If you are unable to sign for your package please let us know (CS@loversstores.com<span> </span>or <span>1.844.988.0027</span>).</p>
<p>Orders Over $200 require a signature upon delivery as a protection against lost or stolen packages. If you are unable to sign for your package please let us know (CS@loversstores.com<span> </span>or <span>1.844.988.0027</span>).</p>
<p>If you purchased online or are unable to visit one of our stores; exchanges for the same item<span> </span><strong>or equal value</strong><span> </span>can be processed by contacting Customer Care at <span>1.844.988.0027</span> or by emailing <span><span style="text-decoration:underline;color:#2b00ff;">CS@loversstores.com</span></span>. Unworn lingerie items with the manufacturers tags still attached may be exchanged for size.<span> </span><strong>No cash refunds, balances will be applied to a gift card for future purchases.</strong></p>
<p>If you purchased online or are unable to visit one of our stores; exchanges for the same item<span> </span><strong>or equal value</strong><span> </span>can be processed by contacting Customer Care at <span>1.844.988.0027</span> or by emailing <span><span style="text-decoration:underline;color:#2b00ff;">CS@loversstores.com</span></span>. Unworn lingerie items with the manufacturers tags still attached may be exchanged for size.<span> </span><strong>No cash refunds, balances will be applied to a gift card for future purchases.</strong></p>"""

# Find all matches of the pattern in the text
matches = re.findall(pattern, text)
print("test")
# Print the matches
for match in matches:
    print(match)