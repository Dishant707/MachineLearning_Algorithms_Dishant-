#!/usr/bin/env python3
"""
Email and Password Manager Agent

A secure command-line tool for managing email accounts and passwords.
Uses Fernet symmetric encryption (AES-128-CBC) from the cryptography library
to securely store credentials.

Features:
- Secure encryption of passwords using Fernet (AES-128-CBC)
- Master password protection with key derivation (PBKDF2)
- Add, view, update, and delete email/password entries
- Search functionality
- Encrypted file-based storage

Requirements:
    pip install cryptography

Usage:
    python email_password_manager.py

Author: Email Password Manager Agent
Version: 1.0.0
"""

import os
import sys
import json
import base64
import getpass
from pathlib import Path
from typing import Optional, Dict, List

try:
    from cryptography.fernet import Fernet, InvalidToken
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.backends import default_backend
except ImportError:
    print("Error: 'cryptography' library is required.")
    print("Install it using: pip install cryptography")
    sys.exit(1)


class EmailPasswordManager:
    """
    A secure email and password management agent.
    
    This class provides functionality to securely store, retrieve, update,
    and delete email/password credentials using Fernet encryption.
    """
    
    # Default file paths for storage
    DEFAULT_DATA_FILE = "credentials.enc"
    DEFAULT_SALT_FILE = "salt.key"
    
    def __init__(self, data_file: Optional[str] = None, salt_file: Optional[str] = None):
        """
        Initialize the Email Password Manager.
        
        Args:
            data_file: Path to the encrypted credentials file
            salt_file: Path to the salt file for key derivation
        """
        self.data_file = Path(data_file or self.DEFAULT_DATA_FILE)
        self.salt_file = Path(salt_file or self.DEFAULT_SALT_FILE)
        self.fernet: Optional[Fernet] = None
        self.credentials: Dict[str, Dict[str, str]] = {}
        
    def _generate_salt(self) -> bytes:
        """Generate a random salt for key derivation."""
        return os.urandom(16)
    
    def _load_or_create_salt(self) -> bytes:
        """Load existing salt or create a new one."""
        if self.salt_file.exists():
            with open(self.salt_file, "rb") as f:
                return f.read()
        else:
            salt = self._generate_salt()
            with open(self.salt_file, "wb") as f:
                f.write(salt)
            return salt
    
    def _derive_key(self, master_password: str, salt: bytes) -> bytes:
        """
        Derive an encryption key from the master password using PBKDF2.
        
        Args:
            master_password: The master password provided by the user
            salt: Random salt for key derivation
            
        Returns:
            A base64-encoded key suitable for Fernet encryption
        """
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=480000,  # OWASP recommended minimum
            backend=default_backend()
        )
        key = base64.urlsafe_b64encode(kdf.derive(master_password.encode()))
        return key
    
    def initialize(self, master_password: str) -> bool:
        """
        Initialize the manager with a master password.
        
        This will either set up a new vault or unlock an existing one.
        
        Args:
            master_password: The master password for encryption/decryption
            
        Returns:
            True if initialization was successful, False otherwise
        """
        if len(master_password) < 8:
            print("Error: Master password must be at least 8 characters long.")
            return False
            
        salt = self._load_or_create_salt()
        key = self._derive_key(master_password, salt)
        self.fernet = Fernet(key)
        
        # Try to load existing credentials
        if self.data_file.exists():
            try:
                self._load_credentials()
                return True
            except InvalidToken:
                print("Error: Invalid master password or corrupted data file.")
                self.fernet = None
                return False
        else:
            # New vault, save empty credentials
            self._save_credentials()
            return True
    
    def _load_credentials(self) -> None:
        """Load and decrypt credentials from file."""
        if not self.fernet:
            raise RuntimeError("Manager not initialized. Call initialize() first.")
            
        with open(self.data_file, "rb") as f:
            encrypted_data = f.read()
        
        if encrypted_data:
            decrypted_data = self.fernet.decrypt(encrypted_data)
            self.credentials = json.loads(decrypted_data.decode())
        else:
            self.credentials = {}
    
    def _save_credentials(self) -> None:
        """Encrypt and save credentials to file."""
        if not self.fernet:
            raise RuntimeError("Manager not initialized. Call initialize() first.")
            
        data = json.dumps(self.credentials).encode()
        encrypted_data = self.fernet.encrypt(data)
        
        with open(self.data_file, "wb") as f:
            f.write(encrypted_data)
    
    def add_credential(self, email: str, password: str, 
                       service: Optional[str] = None,
                       notes: Optional[str] = None,
                       alias: Optional[str] = None) -> bool:
        """
        Add a new email/password credential.
        
        Args:
            email: The email address
            password: The password for this account
            service: Optional service name (e.g., "Gmail", "Facebook")
            notes: Optional notes about this credential
            alias: Optional short alias to quickly retrieve this credential
                   (e.g., "grok email", "twitter", "work gmail")
            
        Returns:
            True if credential was added successfully, False if it already exists
        """
        if not self.fernet:
            print("Error: Manager not initialized.")
            return False
            
        # Create a unique key for the credential
        key = f"{email}:{service or 'default'}"
        
        if key in self.credentials:
            print(f"Error: Credential for '{email}' with service '{service or 'default'}' already exists.")
            print("Use 'update' to modify existing credentials.")
            return False
        
        # Check if alias already exists
        if alias:
            for existing_key, cred in self.credentials.items():
                if cred.get("alias", "").lower() == alias.lower():
                    print(f"Error: Alias '{alias}' is already used by another credential.")
                    return False
        
        self.credentials[key] = {
            "email": email,
            "password": password,
            "service": service or "",
            "notes": notes or "",
            "alias": alias or ""
        }
        
        self._save_credentials()
        if alias:
            print(f"Credential for '{email}' added successfully with alias '{alias}'.")
        else:
            print(f"Credential for '{email}' added successfully.")
        return True
    
    def get_credential(self, email: str, service: Optional[str] = None) -> Optional[Dict[str, str]]:
        """
        Retrieve a credential by email and optional service.
        
        Args:
            email: The email address to look up
            service: Optional service name to narrow the search
            
        Returns:
            The credential dictionary if found, None otherwise
        """
        if not self.fernet:
            print("Error: Manager not initialized.")
            return None
            
        key = f"{email}:{service or 'default'}"
        return self.credentials.get(key)
    
    def get_credential_by_alias(self, alias: str) -> Optional[Dict[str, str]]:
        """
        Retrieve a credential by its alias.
        
        This allows quick access to credentials using a simple keyword or phrase
        like "grok email", "twitter", "work gmail", etc.
        
        Args:
            alias: The alias to search for (case-insensitive)
            
        Returns:
            The credential dictionary if found, None otherwise
        """
        if not self.fernet:
            print("Error: Manager not initialized.")
            return None
            
        alias_lower = alias.lower()
        for key, cred in self.credentials.items():
            if cred.get("alias", "").lower() == alias_lower:
                return cred
        return None
    
    def update_credential(self, email: str, 
                          new_password: Optional[str] = None,
                          service: Optional[str] = None,
                          new_notes: Optional[str] = None,
                          new_alias: Optional[str] = None) -> bool:
        """
        Update an existing credential.
        
        Args:
            email: The email address of the credential to update
            new_password: New password (if None, password remains unchanged)
            service: Service name to identify the credential
            new_notes: New notes (if None, notes remain unchanged)
            new_alias: New alias (if None, alias remains unchanged)
            
        Returns:
            True if credential was updated, False if not found
        """
        if not self.fernet:
            print("Error: Manager not initialized.")
            return False
            
        key = f"{email}:{service or 'default'}"
        
        if key not in self.credentials:
            print(f"Error: Credential for '{email}' with service '{service or 'default'}' not found.")
            return False
        
        if new_password:
            self.credentials[key]["password"] = new_password
        if new_notes is not None:
            self.credentials[key]["notes"] = new_notes
        if new_alias is not None and new_alias.strip():
            # Check if the new alias is already used by another credential
            for existing_key, cred in self.credentials.items():
                if existing_key != key and cred.get("alias", "").lower() == new_alias.lower():
                    print(f"Error: Alias '{new_alias}' is already used by another credential.")
                    return False
            self.credentials[key]["alias"] = new_alias
        elif new_alias == "":
            # Allow explicitly clearing the alias
            self.credentials[key]["alias"] = ""
            
        self._save_credentials()
        print(f"Credential for '{email}' updated successfully.")
        return True
    
    def delete_credential(self, email: str, service: Optional[str] = None) -> bool:
        """
        Delete a credential.
        
        Args:
            email: The email address of the credential to delete
            service: Service name to identify the credential
            
        Returns:
            True if credential was deleted, False if not found
        """
        if not self.fernet:
            print("Error: Manager not initialized.")
            return False
            
        key = f"{email}:{service or 'default'}"
        
        if key not in self.credentials:
            print(f"Error: Credential for '{email}' with service '{service or 'default'}' not found.")
            return False
        
        del self.credentials[key]
        self._save_credentials()
        print(f"Credential for '{email}' deleted successfully.")
        return True
    
    def list_all_credentials(self) -> List[Dict[str, str]]:
        """
        List all stored credentials (passwords masked).
        
        Returns:
            List of credential dictionaries with masked passwords
        """
        if not self.fernet:
            print("Error: Manager not initialized.")
            return []
            
        result = []
        for key, cred in self.credentials.items():
            result.append({
                "email": cred["email"],
                "service": cred["service"] or "default",
                "password": "*" * 8,  # Mask password
                "notes": cred["notes"],
                "alias": cred.get("alias", "")
            })
        return result
    
    def search_credentials(self, query: str) -> List[Dict[str, str]]:
        """
        Search credentials by email, service name, or alias.
        
        Args:
            query: Search string (case-insensitive)
            
        Returns:
            List of matching credentials with masked passwords
        """
        if not self.fernet:
            print("Error: Manager not initialized.")
            return []
            
        query_lower = query.lower()
        result = []
        
        for key, cred in self.credentials.items():
            if (query_lower in cred["email"].lower() or 
                query_lower in cred["service"].lower() or
                query_lower in cred["notes"].lower() or
                query_lower in cred.get("alias", "").lower()):
                result.append({
                    "email": cred["email"],
                    "service": cred["service"] or "default",
                    "password": "*" * 8,
                    "notes": cred["notes"],
                    "alias": cred.get("alias", "")
                })
        return result
    
    def generate_password(self, length: int = 16) -> str:
        """
        Generate a secure random password.
        
        Args:
            length: Length of the password (minimum 8, default 16)
            
        Returns:
            A randomly generated password string
        """
        import string
        import secrets
        
        if length < 8:
            length = 8
            
        # Define character sets
        lowercase = string.ascii_lowercase
        uppercase = string.ascii_uppercase
        digits = string.digits
        special = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        
        # Ensure at least one character from each set
        password = [
            secrets.choice(lowercase),
            secrets.choice(uppercase),
            secrets.choice(digits),
            secrets.choice(special)
        ]
        
        # Fill the rest randomly
        all_chars = lowercase + uppercase + digits + special
        password.extend(secrets.choice(all_chars) for _ in range(length - 4))
        
        # Shuffle the password
        password_list = list(password)
        secrets.SystemRandom().shuffle(password_list)
        
        return "".join(password_list)
    
    def export_credentials(self, output_file: str, include_passwords: bool = False) -> bool:
        """
        Export credentials to a JSON file.
        
        Args:
            output_file: Path to the output file
            include_passwords: Whether to include actual passwords (default False)
            
        Returns:
            True if export was successful
        """
        if not self.fernet:
            print("Error: Manager not initialized.")
            return False
            
        export_data = []
        for key, cred in self.credentials.items():
            export_entry = {
                "email": cred["email"],
                "service": cred["service"] or "default",
                "notes": cred["notes"],
                "alias": cred.get("alias", "")
            }
            if include_passwords:
                export_entry["password"] = cred["password"]
            else:
                export_entry["password"] = "[HIDDEN]"
            export_data.append(export_entry)
        
        with open(output_file, "w") as f:
            json.dump(export_data, f, indent=2)
            
        print(f"Credentials exported to '{output_file}'")
        return True


def print_menu():
    """Print the main menu."""
    print("\n" + "=" * 50)
    print("       Email & Password Manager Agent")
    print("=" * 50)
    print("1. Add new credential")
    print("2. View credential (by email)")
    print("3. Quick view by alias (e.g., 'twitter', 'grok email')")
    print("4. View all credentials")
    print("5. Update credential")
    print("6. Delete credential")
    print("7. Search credentials")
    print("8. Generate secure password")
    print("9. Export credentials")
    print("10. Exit")
    print("=" * 50)


def get_password_input(prompt: str = "Password: ") -> str:
    """Get password input without echoing."""
    try:
        return getpass.getpass(prompt)
    except Exception:
        return input(prompt)


def main():
    """Main function to run the Email Password Manager CLI."""
    print("\n" + "=" * 50)
    print("   Welcome to the Email & Password Manager Agent")
    print("=" * 50)
    print("\nThis tool securely manages your email accounts and passwords.")
    print("All data is encrypted using AES-128-CBC encryption.\n")
    
    manager = EmailPasswordManager()
    
    # Get or create master password
    if manager.data_file.exists():
        print("Existing vault found. Please enter your master password.")
        master_password = get_password_input("Master Password: ")
    else:
        print("No existing vault found. Let's create a new one.")
        print("Please create a master password (min 8 characters).")
        master_password = get_password_input("Create Master Password: ")
        confirm_password = get_password_input("Confirm Master Password: ")
        
        if master_password != confirm_password:
            print("Error: Passwords do not match. Exiting.")
            sys.exit(1)
    
    if not manager.initialize(master_password):
        print("Failed to initialize the password manager. Exiting.")
        sys.exit(1)
    
    print("\n✓ Vault unlocked successfully!")
    
    while True:
        print_menu()
        choice = input("Select an option (1-10): ").strip()
        
        if choice == "1":
            # Add new credential
            print("\n--- Add New Credential ---")
            email = input("Email address: ").strip()
            service = input("Service name (e.g., Gmail, Facebook) [optional]: ").strip()
            
            gen_password = input("Generate secure password? (y/n): ").strip().lower()
            if gen_password == "y":
                password = manager.generate_password()
                print(f"Generated password: {password}")
            else:
                password = get_password_input("Password: ")
                
            notes = input("Notes [optional]: ").strip()
            alias = input("Quick access alias (e.g., 'twitter', 'grok email') [optional]: ").strip()
            
            manager.add_credential(email, password, service or None, notes or None, alias or None)
            
        elif choice == "2":
            # View credential by email
            print("\n--- View Credential by Email ---")
            email = input("Email address: ").strip()
            service = input("Service name [optional]: ").strip()
            
            cred = manager.get_credential(email, service or None)
            if cred:
                print(f"\nEmail: {cred['email']}")
                print(f"Service: {cred['service'] or 'default'}")
                print(f"Alias: {cred.get('alias', '') or '(none)'}")
                show_pass = input("Show password? (y/n): ").strip().lower()
                if show_pass == "y":
                    print(f"Password: {cred['password']}")
                else:
                    print("Password: ********")
                print(f"Notes: {cred['notes']}")
            else:
                print("Credential not found.")
                
        elif choice == "3":
            # Quick view by alias
            print("\n--- Quick View by Alias ---")
            print("Enter your alias (e.g., 'twitter', 'grok email', 'work gmail'):")
            alias = input("Alias: ").strip()
            
            cred = manager.get_credential_by_alias(alias)
            if cred:
                print(f"\n✓ Found credential for alias '{alias}':")
                print(f"Email: {cred['email']}")
                print(f"Service: {cred['service'] or 'default'}")
                show_pass = input("Show password? (y/n): ").strip().lower()
                if show_pass == "y":
                    print(f"Password: {cred['password']}")
                else:
                    print("Password: ********")
                print(f"Notes: {cred['notes']}")
            else:
                print(f"No credential found with alias '{alias}'.")
                
        elif choice == "4":
            # View all credentials
            print("\n--- All Credentials ---")
            all_creds = manager.list_all_credentials()
            if all_creds:
                for i, cred in enumerate(all_creds, 1):
                    print(f"\n{i}. Email: {cred['email']}")
                    print(f"   Service: {cred['service']}")
                    print(f"   Alias: {cred.get('alias', '') or '(none)'}")
                    print(f"   Notes: {cred['notes']}")
            else:
                print("No credentials stored yet.")
                
        elif choice == "5":
            # Update credential
            print("\n--- Update Credential ---")
            email = input("Email address: ").strip()
            service = input("Service name [optional]: ").strip()
            
            cred = manager.get_credential(email, service or None)
            if cred:
                print(f"\nCurrent credential for: {email}")
                print(f"Current alias: {cred.get('alias', '') or '(none)'}")
                new_password = get_password_input("New password (leave blank to keep current): ")
                new_notes = input("New notes (leave blank to keep current): ").strip()
                new_alias = input("New alias (leave blank to keep current): ").strip()
                
                manager.update_credential(
                    email,
                    new_password if new_password else None,
                    service or None,
                    new_notes if new_notes else None,
                    new_alias if new_alias else None
                )
            else:
                print("Credential not found.")
                
        elif choice == "6":
            # Delete credential
            print("\n--- Delete Credential ---")
            email = input("Email address: ").strip()
            service = input("Service name [optional]: ").strip()
            
            confirm = input(f"Are you sure you want to delete '{email}'? (yes/no): ").strip().lower()
            if confirm == "yes":
                manager.delete_credential(email, service or None)
            else:
                print("Deletion cancelled.")
                
        elif choice == "7":
            # Search credentials
            print("\n--- Search Credentials ---")
            print("Search by email, service, alias, or notes:")
            query = input("Search query: ").strip()
            results = manager.search_credentials(query)
            
            if results:
                print(f"\nFound {len(results)} matching credential(s):")
                for i, cred in enumerate(results, 1):
                    print(f"\n{i}. Email: {cred['email']}")
                    print(f"   Service: {cred['service']}")
                    print(f"   Alias: {cred.get('alias', '') or '(none)'}")
                    print(f"   Notes: {cred['notes']}")
            else:
                print("No matching credentials found.")
                
        elif choice == "8":
            # Generate password
            print("\n--- Generate Secure Password ---")
            length_input = input("Password length (8-64) [default: 16]: ").strip()
            try:
                length = int(length_input) if length_input else 16
                length = max(8, min(64, length))
            except ValueError:
                length = 16
                
            password = manager.generate_password(length)
            print(f"\nGenerated Password: {password}")
            
        elif choice == "9":
            # Export credentials
            print("\n--- Export Credentials ---")
            output_file = input("Output file path [default: exported_credentials.json]: ").strip()
            output_file = output_file or "exported_credentials.json"
            
            include_pass = input("Include passwords in export? (yes/no): ").strip().lower()
            manager.export_credentials(output_file, include_pass == "yes")
            
        elif choice == "10":
            # Exit
            print("\nThank you for using Email & Password Manager Agent!")
            print("Your data has been securely saved. Goodbye!")
            break
            
        else:
            print("Invalid option. Please select 1-10.")


if __name__ == "__main__":
    main()
