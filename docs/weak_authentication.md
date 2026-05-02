# Weak Authentication

> **Project Status:**
> - [x] Vulnerability demonstrated
> - [x] Fix implemented (see Day 6)

---

## What is Weak Authentication?
Weak authentication occurs when passwords are stored in plaintext 
in the database. Any attacker who gains database access — through 
SQL Injection or any other method — can immediately read every 
user's password without any additional effort.

This is dangerous beyond just the compromised application because 
people reuse passwords across multiple sites. One leaked database 
becomes a key to every other account that user owns.

## Why is Plaintext Storage Dangerous?
Consider what our database currently contains:

```python
[(1, 'admin', 'password123')]
```

Any attacker with database access sees passwords immediately.
Combined with SQL Injection, this creates a two-step attack:
Step 1: SQL Injection → gain database access
Step 2: Read plaintext passwords → attack other websites

This combination is called **credential stuffing** — one of the 
most common attacks on the internet today.

## The Fix — Password Hashing with bcrypt
The fix is hashing passwords before storing them. Hashing is a 
one-way transformation — unlike encryption, it cannot be reversed.
Plaintext:  password123
Hashed:     $2b$12$2AXz./71pBLQ0DWzxphoweDDxPOgKF9gI7Vym9aUTFMB8RCjEZzzu

The app never stores or compares plaintext passwords — only hashes.

**Login flow with hashing:**
User enters password
↓
App hashes the input
↓
App compares hash to stored hash
↓
Match → login succeeds
No match → login fails

## What is bcrypt and Why is it Special?
bcrypt is a password hashing algorithm designed specifically for 
storing passwords securely. It has two properties that make it 
better than simple hashing:

**1. Salting**
bcrypt adds random data (a salt) to each password before hashing.
This means two identical passwords produce completely different hashes:
password123 → 2b$12
Ny6xWEQXbLMYAgr9QejfO...
password123 → 2b$12
PQSgtXopBAaCBHQ7bRtdf...

This defeats rainbow table attacks — pre-computed tables of 
common password hashes become useless because every hash is unique.

**2. Slow Computation**
bcrypt is deliberately slow to compute. The cost factor (12 in 
our case) means 2¹² = 4096 rounds of hashing. This makes 
brute force attacks impractical — an attacker trying millions 
of passwords would need years instead of seconds.

## Vulnerable vs Secure
Vulnerable database:
[(1, 'admin', 'password123')]  ← immediately readable
Secure database:
[(1, 'admin', '$2b$12$2AXz...')]  ← impractical to crack

## Key Takeaway
> "Never store plaintext passwords. Hash them with bcrypt — 
> salting defeats rainbow tables, slow computation defeats 
> brute force, and one-way hashing means even developers 
> can't read user passwords."
