# SQL Injection

## What is SQL Injection?
SQL Injection is an attack that manipulates a database query by 
injecting special characters into user input fields. Instead of 
providing a normal username or password, an attacker inserts SQL 
syntax that changes the logic of the query itself — bypassing 
authentication or extracting unauthorized data.

## Why Does It Work?
SQL Injection works because of one core mistake: user input is 
directly concatenated into a SQL query string. The database 
receives one combined string and cannot distinguish between the 
developer's intended code and the attacker's injected input. 
It simply executes whatever it receives.

Example of vulnerable code:
```python
query = "SELECT * FROM users WHERE username = '" + username + "' AND password = '" + password + "'"
```

## Demonstrations

### Attack 1 — Login Bypass (Known Username)
**Input:** `admin'--`

**Query produced:**
```sql
SELECT * FROM users WHERE username = 'admin'--' AND password = 'anything'
```

**What happened:**
- The single quote `'` closed the username string early
- The double dash `--` commented out the rest of the query
- The password check was completely eliminated
- Result: logged in as admin without knowing the password

### Attack 2 — Login Bypass (No Username Needed)
**Input:** `' OR '1'='1'--`

**Query produced:**
```sql
SELECT * FROM users WHERE username = '' OR '1'='1'--' AND password = 'anything'
```

**What happened:**
- The single quote `'` closed the username string early
- `OR '1'='1'` is always true, so every row matches
- The double dash `--` commented out the password check
- Result: database returned all users, logged in as the first one

## The Fix — Parameterized Queries
The correct fix is parameterized queries, also called prepared 
statements. Instead of concatenating user input into the query 
string, the query structure is sent to the database separately 
from the data.

```python
# Vulnerable
query = "SELECT * FROM users WHERE username = '" + username + "'"

# Secure
query = "SELECT * FROM users WHERE username = ?"
cursor.execute(query, (username,))
```

The database compiles the query structure first, then inserts 
the user input as pure data. Even if someone types `admin'--`, 
it is treated as a literal string, never as SQL code.

**Why not just sanitize input?**
Input sanitization tries to detect and remove dangerous 
characters. But attackers are creative. They find encodings 
and edge cases that bypass filters. Parameterized queries 
eliminate the problem entirely by never allowing user input 
to become code.

## Key Takeaway
> "The database can't tell the difference between developer 
> code and attacker input, unless you keep them separate."