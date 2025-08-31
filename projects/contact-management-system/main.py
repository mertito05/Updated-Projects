import sqlite3
import json
from datetime import datetime
import csv
import re
from typing import List, Dict, Optional

class ContactManager:
    def __init__(self, db_name='contacts.db'):
        self.db_name = db_name
        self.init_db()
    
    def init_db(self):
        """Initialize the database"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # Create contacts table
        c.execute('''CREATE TABLE IF NOT EXISTS contacts
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      first_name TEXT NOT NULL,
                      last_name TEXT NOT NULL,
                      email TEXT UNIQUE,
                      phone TEXT,
                      address TEXT,
                      company TEXT,
                      title TEXT,
                      notes TEXT,
                      created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                      updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)''')
        
        # Create tags table
        c.execute('''CREATE TABLE IF NOT EXISTS tags
                     (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      name TEXT UNIQUE NOT NULL)''')
        
        # Create contact_tags junction table
        c.execute('''CREATE TABLE IF NOT EXISTS contact_tags
                     (contact_id INTEGER,
                      tag_id INTEGER,
                      PRIMARY KEY (contact_id, tag_id),
                      FOREIGN KEY (contact_id) REFERENCES contacts (id),
                      FOREIGN KEY (tag_id) REFERENCES tags (id))''')
        
        conn.commit()
        conn.close()
    
    def validate_email(self, email: str) -> bool:
        """Validate email format"""
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, email) is not None
    
    def validate_phone(self, phone: str) -> bool:
        """Validate phone number format"""
        # Basic validation - allow various formats
        pattern = r'^[\d\s\-\+\(\)\.]{10,20}$'
        return re.match(pattern, phone) is not None
    
    def add_contact(self, first_name: str, last_name: str, email: str = None, 
                   phone: str = None, address: str = None, company: str = None, 
                   title: str = None, notes: str = None) -> Optional[int]:
        """Add a new contact"""
        if not first_name or not last_name:
            print("First name and last name are required")
            return None
        
        if email and not self.validate_email(email):
            print("Invalid email format")
            return None
        
        if phone and not self.validate_phone(phone):
            print("Invalid phone format")
            return None
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        try:
            c.execute('''INSERT INTO contacts 
                         (first_name, last_name, email, phone, address, company, title, notes)
                         VALUES (?, ?, ?, ?, ?, ?, ?, ?)''',
                      (first_name, last_name, email, phone, address, company, title, notes))
            
            contact_id = c.lastrowid
            conn.commit()
            print(f"Contact added successfully (ID: {contact_id})")
            return contact_id
            
        except sqlite3.IntegrityError:
            print("Email already exists in database")
            return None
        finally:
            conn.close()
    
    def update_contact(self, contact_id: int, **kwargs) -> bool:
        """Update contact information"""
        if not kwargs:
            print("No fields to update")
            return False
        
        allowed_fields = ['first_name', 'last_name', 'email', 'phone', 
                         'address', 'company', 'title', 'notes']
        update_fields = []
        update_values = []
        
        for field, value in kwargs.items():
            if field in allowed_fields:
                if field == 'email' and value and not self.validate_email(value):
                    print("Invalid email format")
                    return False
                if field == 'phone' and value and not self.validate_phone(value):
                    print("Invalid phone format")
                    return False
                
                update_fields.append(f"{field} = ?")
                update_values.append(value)
        
        if not update_fields:
            print("No valid fields to update")
            return False
        
        update_values.append(contact_id)
        update_values.append(datetime.now().isoformat())
        
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        try:
            query = f'''UPDATE contacts 
                       SET {', '.join(update_fields)}, updated_at = ?
                       WHERE id = ?'''
            c.execute(query, update_values)
            
            if c.rowcount == 0:
                print("Contact not found")
                return False
            
            conn.commit()
            print("Contact updated successfully")
            return True
            
        except sqlite3.IntegrityError:
            print("Email already exists in database")
            return False
        finally:
            conn.close()
    
    def delete_contact(self, contact_id: int) -> bool:
        """Delete a contact"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        # First delete associated tags
        c.execute('DELETE FROM contact_tags WHERE contact_id = ?', (contact_id,))
        
        # Then delete the contact
        c.execute('DELETE FROM contacts WHERE id = ?', (contact_id,))
        
        if c.rowcount == 0:
            print("Contact not found")
            conn.close()
            return False
        
        conn.commit()
        conn.close()
        print("Contact deleted successfully")
        return True
    
    def search_contacts(self, search_term: str = None, tag: str = None) -> List[Dict]:
        """Search contacts by name, email, or tag"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        query = '''SELECT c.*, GROUP_CONCAT(t.name, ', ') as tags
                   FROM contacts c
                   LEFT JOIN contact_tags ct ON c.id = ct.contact_id
                   LEFT JOIN tags t ON ct.tag_id = t.id'''
        
        conditions = []
        params = []
        
        if search_term:
            conditions.append('''(c.first_name LIKE ? OR c.last_name LIKE ? 
                                OR c.email LIKE ? OR c.company LIKE ?)''')
            search_pattern = f'%{search_term}%'
            params.extend([search_pattern, search_pattern, search_pattern, search_pattern])
        
        if tag:
            conditions.append('t.name = ?')
            params.append(tag)
        
        if conditions:
            query += ' WHERE ' + ' AND '.join(conditions)
        
        query += ' GROUP BY c.id ORDER BY c.last_name, c.first_name'
        
        c.execute(query, params)
        contacts = []
        
        for row in c.fetchall():
            contact = {
                'id': row[0],
                'first_name': row[1],
                'last_name': row[2],
                'email': row[3],
                'phone': row[4],
                'address': row[5],
                'company': row[6],
                'title': row[7],
                'notes': row[8],
                'created_at': row[9],
                'updated_at': row[10],
                'tags': row[11] if row[11] else ''
            }
            contacts.append(contact)
        
        conn.close()
        return contacts
    
    def get_contact(self, contact_id: int) -> Optional[Dict]:
        """Get a specific contact by ID"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        c.execute('''SELECT c.*, GROUP_CONCAT(t.name, ', ') as tags
                     FROM contacts c
                     LEFT JOIN contact_tags ct ON c.id = ct.contact_id
                     LEFT JOIN tags t ON ct.tag_id = t.id
                     WHERE c.id = ?
                     GROUP BY c.id''', (contact_id,))
        
        row = c.fetchone()
        conn.close()
        
        if not row:
            return None
        
        return {
            'id': row[0],
            'first_name': row[1],
            'last_name': row[2],
            'email': row[3],
            'phone': row[4],
            'address': row[5],
            'company': row[6],
            'title': row[7],
            'notes': row[8],
            'created_at': row[9],
            'updated_at': row[10],
            'tags': row[11] if row[11] else ''
        }
    
    def add_tag(self, contact_id: int, tag_name: str) -> bool:
        """Add a tag to a contact"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        try:
            # First, get or create the tag
            c.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
            tag_row = c.fetchone()
            
            if tag_row:
                tag_id = tag_row[0]
            else:
                c.execute('INSERT INTO tags (name) VALUES (?)', (tag_name,))
                tag_id = c.lastrowid
            
            # Check if the contact-tag relationship already exists
            c.execute('SELECT 1 FROM contact_tags WHERE contact_id = ? AND tag_id = ?', 
                      (contact_id, tag_id))
            if c.fetchone():
                print("Tag already assigned to contact")
                conn.close()
                return False
            
            # Add the relationship
            c.execute('INSERT INTO contact_tags (contact_id, tag_id) VALUES (?, ?)', 
                      (contact_id, tag_id))
            
            conn.commit()
            print(f"Tag '{tag_name}' added to contact")
            return True
            
        except sqlite3.IntegrityError:
            print("Invalid contact ID")
            return False
        finally:
            conn.close()
    
    def remove_tag(self, contact_id: int, tag_name: str) -> bool:
        """Remove a tag from a contact"""
        conn = sqlite3.connect(self.db_name)
        c = conn.cursor()
        
        try:
            # Get the tag ID
            c.execute('SELECT id FROM tags WHERE name = ?', (tag_name,))
            tag_row = c.fetchone()
            
            if not tag_row:
                print("Tag not found")
                return False
            
            tag_id = tag_row[0]
            
            # Remove the relationship
            c.execute('DELETE FROM contact_tags WHERE contact_id = ? AND tag_id = ?', 
                      (contact_id, tag_id))
            
            if c.rowcount == 0:
                print("Tag not assigned to contact")
                return False
            
            conn.commit()
            print(f"Tag '{tag_name}' removed from contact")
            return True
            
        finally:
            conn.close()
    
    def export_contacts(self, filename: str = 'contacts_export.csv'):
        """Export all contacts to CSV"""
        contacts = self.search_contacts()
        
        if not contacts:
            print("No contacts to export")
            return False
        
        try:
            with open(filename, 'w', newline='', encoding='utf-8') as csvfile:
                fieldnames = ['id', 'first_name', 'last_name', 'email', 'phone', 
                             'address', 'company', 'title', 'notes', 'tags']
                writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
                
                writer.writeheader()
                for contact in contacts:
                    writer.writerow(contact)
            
            print(f"Contacts exported to {filename}")
            return True
            
        except Exception as e:
            print(f"Error exporting contacts: {e}")
            return False
    
    def import_contacts(self, filename: str):
        """Import contacts from CSV"""
        try:
            with open(filename, 'r', encoding='utf-8') as csvfile:
                reader = csv.DictReader(csvfile)
                imported_count = 0
                
                for row in reader:
                    # Skip rows without required fields
                    if not row.get('first_name') or not row.get('last_name'):
                        continue
                    
                    contact_id = self.add_contact(
                        first_name=row.get('first_name', ''),
                        last_name=row.get('last_name', ''),
                        email=row.get('email'),
                        phone=row.get('phone'),
                        address=row.get('address'),
                        company=row.get('company'),
                        title=row.get('title'),
                        notes=row.get('notes')
                    )
                    
                    if contact_id:
                        imported_count += 1
                        # Add tags if specified
                        tags = row.get('tags', '').split(',')
                        for tag in tags:
                            tag = tag.strip()
                            if tag:
                                self.add_tag(contact_id, tag)
                
                print(f"Imported {imported_count} contacts")
                return True
                
        except FileNotFoundError:
            print("File not found")
            return False
        except Exception as e:
            print(f"Error importing contacts: {e}")
            return False

def display_contact(contact: Dict):
    """Display a contact in a formatted way"""
    print(f"\n=== {contact['first_name']} {contact['last_name']} ===")
    print(f"ID: {contact['id']}")
    if contact['email']:
        print(f"Email: {contact['email']}")
    if contact['phone']:
        print(f"Phone: {contact['phone']}")
    if contact['company']:
        print(f"Company: {contact['company']}")
    if contact['title']:
        print(f"Title: {contact['title']}")
    if contact['address']:
        print(f"Address: {contact['address']}")
    if contact['notes']:
        print(f"Notes: {contact['notes']}")
    if contact['tags']:
        print(f"Tags: {contact['tags']}")
    print(f"Created: {contact['created_at']}")
    print(f"Updated: {contact['updated_at']}")

def main():
    """Main function"""
    manager = ContactManager()
    
    while True:
        print("\n=== Contact Management System ===")
        print("1. Add Contact")
        print("2. Update Contact")
        print("3. Delete Contact")
        print("4. Search Contacts")
        print("5. View Contact Details")
        print("6. Add Tag to Contact")
        print("7. Remove Tag from Contact")
        print("8. Export Contacts")
        print("9. Import Contacts")
        print("10. Exit")
        
        choice = input("\nEnter your choice (1-10): ").strip()
        
        if choice == "1":
            print("\nAdd New Contact")
            first_name = input("First Name: ").strip()
            last_name = input("Last Name: ").strip()
            email = input("Email (optional): ").strip() or None
            phone = input("Phone (optional): ").strip() or None
            address = input("Address (optional): ").strip() or None
            company = input("Company (optional): ").strip() or None
            title = input("Title (optional): ").strip() or None
            notes = input("Notes (optional): ").strip() or None
            
            manager.add_contact(first_name, last_name, email, phone, address, company, title, notes)
        
        elif choice == "2":
            contact_id = input("Enter Contact ID to update: ").strip()
            if not contact_id.isdigit():
                print("Invalid contact ID")
                continue
            
            contact = manager.get_contact(int(contact_id))
            if not contact:
                print("Contact not found")
                continue
            
            print("\nLeave field blank to keep current value")
            updates = {}
            
            first_name = input(f"First Name ({contact['first_name']}): ").strip()
            if first_name: updates['first_name'] = first_name
            
            last_name = input(f"Last Name ({contact['last_name']}): ").strip()
            if last_name: updates['last_name'] = last_name
            
            email = input(f"Email ({contact['email'] or 'None'}): ").strip()
            if email: updates['email'] = email
            
            phone = input(f"Phone ({contact['phone'] or 'None'}): ").strip()
            if phone: updates['phone'] = phone
            
            address = input(f"Address ({contact['address'] or 'None'}): ").strip()
            if address: updates['address'] = address
            
            company = input(f"Company ({contact['company'] or 'None'}): ").strip()
            if company: updates['company'] = company
            
            title = input(f"Title ({contact['title'] or 'None'}): ").strip()
            if title: updates['title'] = title
            
            notes = input(f"Notes ({contact['notes'] or 'None'}): ").strip()
            if notes: updates['notes'] = notes
            
            if updates:
                manager.update_contact(int(contact_id), **updates)
            else:
                print("No changes made")
        
        elif choice == "3":
            contact_id = input("Enter Contact ID to delete: ").strip()
            if not contact_id.isdigit():
                print("Invalid contact ID")
                continue
            
            confirm = input("Are you sure? (y/n): ").strip().lower()
            if confirm == 'y':
                manager.delete_contact(int(contact_id))
        
        elif choice == "4":
            search_term = input("Search term (leave blank for all): ").strip() or None
            tag = input("Filter by tag (leave blank for all): ").strip() or None
            
            contacts = manager.search_contacts(search_term, tag)
            
            if not contacts:
                print("No contacts found")
                continue
            
            print(f"\nFound {len(contacts)} contacts:")
            for contact in contacts:
                print(f"{contact['id']}: {contact['first_name']} {contact['last_name']} "
                      f"({contact['email'] or 'No email'}) - Tags: {contact['tags']}")
        
        elif choice == "5":
            contact_id = input("Enter Contact ID: ").strip()
            if not contact_id.isdigit():
                print("Invalid contact ID")
                continue
            
            contact = manager.get_contact(int(contact_id))
            if contact:
                display_contact(contact)
            else:
                print("Contact not found")
        
        elif choice == "6":
            contact_id = input("Enter Contact ID: ").strip()
            if not contact_id.isdigit():
                print("Invalid contact ID")
                continue
            
            tag_name = input("Enter tag name: ").strip()
            if tag_name:
                manager.add_tag(int(contact_id), tag_name)
        
        elif choice == "7":
            contact_id = input("Enter Contact ID: ").strip()
            if not contact_id.isdigit():
                print("Invalid contact ID")
                continue
            
            tag_name = input("Enter tag name: ").strip()
            if tag_name:
                manager.remove_tag(int(contact_id), tag_name)
        
        elif choice == "8":
            filename = input("Export filename (default: contacts_export.csv): ").strip()
            filename = filename or 'contacts_export.csv'
            manager.export_contacts(filename)
        
        elif choice == "9":
            filename = input("Import filename: ").strip()
            if filename:
                manager.import_contacts(filename)
        
        elif choice == "10":
            print("Goodbye!")
            break
        
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
