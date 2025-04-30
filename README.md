# 📚 Dictionary Web Application  

A user-managed glossary system with authentication, term management, and text translation features. Built with Python (Flask/Django) and SQLite.  

---

## ✨ Features  

### 🔐 **User Authentication**  
- Registration & login via username/password.  
- Session-based access control.  

### 📝 **Term Management**  
- **Add/Delete**: Users can create and remove their own terms.  
- **Global View**: Alphabetized list of all terms from all users.  
- **Ownership**: Only term creators can delete their entries.  

### 🔤 **Text Translator**  
- Detects dictionary terms in input text.  
- Appends definitions in brackets (e.g., "normis (person with mainstream interests)").  

---

## 🖥️ Pages & Routes  
| Page            | Description                                  | Access          |  
|-----------------|--------------------------------------------|----------------|  
| `/login`        | User login/registration                    | Public         |  
| `/terms`        | Alphabetized list of all terms             | Authenticated  |  
| `/my-terms`     | User’s terms (+ add/delete buttons)        | Owner only     |  
| `/translator`   | Text input field with translation output   | Authenticated  |  

---

## 🛠️ Technical Stack  
- **Backend**: Python (Flask/Django)  
- **Database**: SQLite (`users`, `terms` tables)  
- **Templates**: HTML/Jinja2 (or frontend framework)  

### 📂 Database Schema  
```sql
-- Users table
CREATE TABLE users (
    id INTEGER PRIMARY KEY,
    username TEXT UNIQUE NOT NULL,
    password_hash TEXT NOT NULL
);

-- Terms table
CREATE TABLE terms (
    id INTEGER PRIMARY KEY,
    term TEXT NOT NULL,
    definition TEXT NOT NULL,
    user_id INTEGER NOT NULL,
    FOREIGN KEY (user_id) REFERENCES users (id)
);
