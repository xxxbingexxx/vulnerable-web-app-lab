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
- Step 1: SQL Injection → gain database access
- Step 2: Read plaintext passwords → attack other websites

This combination is called **credential stuffing**, one of the 
most common attacks on the internet today.

## The Fix — Password Hashing with bcrypt
The fix is hashing passwords before storing them. Hashing is a one-way mathematical transformation that converts a plaintext password into a fixed-length string of characters. Unlike encryption, it cannot be reversed. There is no key that converts the hash back to the original password.
```
Plaintext:  password123
Hashed:     $2b$12$2AXz./71pBLQ0DWzxphoweDDxPOgKF9gI7Vym9aUTFMB8RCjEZzzu
```

The app never stores or compares plaintext passwords, only hashes.

**Login flow with hashing:**
```
User enters password
        ↓
App hashes the input
        ↓
App compares hash to stored hash
        ↓
Match → login succeeds
No match → login fails
```

## What is bcrypt and Why is it Special?
bcrypt is a password hashing algorithm designed specifically for 
storing passwords securely. It has two properties that make it 
better than simple hashing:

**1. Salting**

bcrypt adds random data (a salt) to each password before hashing.
This means two identical passwords produce completely different hashes:
```
password123 + salt1 → $2b$12$Ny6xWEQXbLMYAgr9QejfO...
password123 + salt2 → $2b$12$PQSgtXopBAaCBHQ7bRtdf...
```
This defeats rainbow table attacks. Pre-computed tables of 
common password hashes become useless because every hash is unique.

What makes bcrypt clever is that the salt is stored inside the 
hash itself. Every bcrypt hash contains four pieces of information:
```
$2b$12$Ny6xWEQXbLMYAgr9QejfOeD737IfCrG6cWWU7pKVx.P4LvLjGVuA.
|   |  |___________________|____________________________|
|   |        salt (22 chars)       hash
|   cost factor (12 = 2¹² = 4,096 rounds)
algorithm version (2b = bcrypt)
```
This means `bcrypt.checkpw()` never needs to be told the salt. 
It reads it directly from the stored hash:
```
User types:        password123
bcrypt extracts:   salt from stored hash
bcrypt computes:   hash(password123 + extracted salt)
bcrypt compares:   computed hash == stored hash
Result:            match → login succeeds
```
The plaintext password is never stored or compared directly. Only hashes ever touch the database.

**2. Slow Computation**

bcrypt is deliberately slow to compute. The cost factor (12 in 
our case) means 2¹² = 4096 rounds of hashing. This makes 
brute force attacks impractical. An attacker trying millions 
of passwords would need years instead of seconds.

## Vulnerable vs Secure
```
Vulnerable database:
[(1, 'admin', 'password123')]  ← immediately readable
Secure database:
[(1, 'admin', '$2b$12$2AXz...')]  ← impractical to crack
```

## Key Takeaway
> "Never store plaintext passwords. Hash them with bcrypt. 
> Salting defeats rainbow tables, slow computation defeats 
> brute force, and one-way hashing means even developers 
> can't read user passwords."
