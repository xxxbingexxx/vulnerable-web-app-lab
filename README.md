# Vulnerable Web App Lab
### SQL Injection, XSS, and Authentication Flaws

* **Zhibin Wang**
  * [LinkedIn](https://www.linkedin.com/in/zhibin-wang-396318397)
  * [GitHub](https://github.com/xxxbingexxx)

This project demonstrates three core web security vulnerabilities 
by building a deliberately vulnerable web application from scratch. 
For each vulnerability, the project covers the attack, the 
underlying reason it works, and the secure fix with explanation.

The goal was not to build a polished web app — it was to deeply 
understand how real attacks work in practice and be able to 
explain both the vulnerabilities and defenses clearly.

## What You'll Find
- `main` branch — vulnerable implementation
- `secured` branch — fixed implementation  
- `/docs` — tutorial-style documentation explaining each 
  vulnerability, how it was demonstrated, and how it was fixed

## Vulnerabilities Demonstrated

### 1. SQL Injection
* **What it is:** An attack that manipulates a database query by 
  injecting special characters into user input fields, allowing 
  attackers to bypass authentication or extract unauthorized data.
* **How we demonstrated it:** Built a login system using string 
  concatenation, then bypassed it using `admin'--` to eliminate 
  the password check and `' OR '1'='1'--` to log in without 
  any credentials.
* **The fix:** Parameterized queries. Query structure and user 
  input are sent to the database separately. Input can never 
  change the query's logic no matter what it contains.

### 2. Cross-Site Scripting (XSS)
* **What it is:** An attack where malicious scripts are injected 
  into a website and executed in other users' browsers. Unlike 
  SQL Injection, XSS attacks the browser, not the database.
* **How we demonstrated it:** Disabled Jinja2's auto-escaping 
  with `| safe`, then posted `<script>alert('hacked')</script>` 
  as a comment. The script executed in every visitor's browser.
* **The fix:** Remove `| safe` and let Jinja2 auto-escape user 
  input. Special characters are converted to harmless text before 
  the browser ever sees them.

### 3. Weak Authentication
* **What it is:** Storing passwords in plaintext means any 
  database breach immediately exposes every user's password. 
  Combined with password reuse, one leaked database can 
  compromise accounts across multiple websites.
* **How we demonstrated it:** Stored `password123` in plaintext, 
  then showed it was directly readable with a simple database query.
* **The fix:** bcrypt hashing. Passwords are transformed before 
  storage using salting and slow computation, making rainbow table 
  and brute force attacks impractical.