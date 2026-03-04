import tkinter as tk
from tkinter import messagebox, ttk
import mysql.connector

class StockManager:
    def __init__(self, root):
        # --- DATABASE CONNECTION ---
        try:
            self.db_connection = mysql.connector.connect(
                host="localhost",
                user="root",
                password="root", # Assurez-vous que c'est le bon mot de passe
                database="store"
            )
            self.db_cursor = self.db_connection.cursor()
        except mysql.connector.Error as err:
            messagebox.showerror("Database Error", f"Impossible de se connecter : {err}")
            root.destroy()

        # --- WINDOW CONFIGURATION ---
        self.root = root
        self.root.title("Store Management System")
        self.root.geometry("600x750") # Augmenté un peu pour la légende

        # --- GUI LAYOUT ---
        tk.Label(root, text="--- PRODUCT MANAGEMENT ---", font=("Arial", 14, "bold")).pack(pady=10)
        
        # Formulaire d'ajout
        self.setup_form()

        # Liste d'affichage
        tk.Label(root, text="--- INVENTORY LIST ---", font=("Arial", 12, "bold")).pack(pady=5)
        self.product_listbox = tk.Listbox(root, width=80, height=15, font=("Courier", 10))
        self.product_listbox.pack(padx=20, pady=5)

        # Boutons d'action
        actions_frame = tk.Frame(root)
        actions_frame.pack(pady=10)
        
        tk.Button(actions_frame, text="DELETE SELECTED", command=self.delete_product, bg="#e74c3c", fg="white", width=20).pack(side=tk.LEFT, padx=5)
        tk.Button(actions_frame, text="REFRESH LIST", command=self.load_data, bg="#3498db", fg="white", width=20).pack(side=tk.LEFT, padx=5)

        # Chargement des données au lancement
        self.load_data()

    def setup_form(self):
        """Crée les champs de saisie pour l'ajout de produit"""
        form_frame = tk.Frame(self.root)
        form_frame.pack(pady=10)

        # Labels et Entries
        tk.Label(form_frame, text="Name:").grid(row=0, column=0, sticky="e")
        self.name_entry = tk.Entry(form_frame, width=30)
        self.name_entry.grid(row=0, column=1, pady=2)

        tk.Label(form_frame, text="Description:").grid(row=1, column=0, sticky="e")
        self.desc_entry = tk.Entry(form_frame, width=30)
        self.desc_entry.grid(row=1, column=1, pady=2)

        tk.Label(form_frame, text="Price:").grid(row=2, column=0, sticky="e")
        self.price_entry = tk.Entry(form_frame, width=30)
        self.price_entry.grid(row=2, column=1, pady=2)

        tk.Label(form_frame, text="Quantity:").grid(row=3, column=0, sticky="e")
        self.quantity_entry = tk.Entry(form_frame, width=30)
        self.quantity_entry.grid(row=3, column=1, pady=2)

        # Note pour l'utilisateur sur les catégories
        tk.Label(form_frame, text="Category ID:", fg="blue").grid(row=4, column=0, sticky="e")
        self.cat_entry = tk.Entry(form_frame, width=30)
        self.cat_entry.grid(row=4, column=1, pady=2)

        # Ajout de la légende explicative
        legend = "1 = Pantalon de survêtement\n2 = Pantalon jeans"
        tk.Label(form_frame, text=legend, fg="#d35400", justify=tk.LEFT, font=("Arial", 9, "italic")).grid(row=5, column=1, sticky="w")

        tk.Button(self.root, text="ADD TO DATABASE", command=self.add_product, bg="#2ecc71", fg="white", font=("Arial", 10, "bold")).pack(pady=15)

    def load_data(self):
        """Récupère les produits et fait une jointure pour afficher le nom de la catégorie"""
        self.product_listbox.delete(0, tk.END)
        query = """
            SELECT p.id, p.name, p.price, p.quantity, c.name 
            FROM product p 
            LEFT JOIN category c ON p.id_category = c.id
        """
        self.db_cursor.execute(query)
        
        for (p_id, name, price, qty, cat_name) in self.db_cursor.fetchall():
            display = f"ID:{p_id:<3} | {name:<12} | {price:>5}€ | Qty:{qty:<4} | Cat:{cat_name}"
            self.product_listbox.insert(tk.END, display)

    def add_product(self):
        """Récupère les saisies, valide l'ID et insère dans MySQL"""
        name = self.name_entry.get()
        desc = self.desc_entry.get()
        price = self.price_entry.get()
        qty = self.quantity_entry.get()
        cat = self.cat_entry.get()

        # 1. Vérification des champs vides
        if not (name and price and qty and cat):
            messagebox.showwarning("Input Error", "Tous les champs sont obligatoires")
            return

        # 2. VALIDATION : Seuls l'ID 1 ou 2 sont acceptés
        if cat not in ["1", "2"]:
            messagebox.showerror("Invalid Category", "Erreur : Seuls l'ID 1 (Survêtement) ou 2 (Jeans) sont autorisés !")
            return

        # 3. Insertion SQL
        try:
            sql = "INSERT INTO product (name, description, price, quantity, id_category) VALUES (%s, %s, %s, %s, %s)"
            self.db_cursor.execute(sql, (name, desc, price, qty, cat))
            self.db_connection.commit()
            
            self.load_data() 
            self.clear_form() 
            messagebox.showinfo("Success", "Produit ajouté avec succès !")
        except mysql.connector.Error as err:
            messagebox.showerror("SQL Error", f"Erreur : {err}")

    def delete_product(self):
        """Supprime l'élément sélectionné"""
        selection = self.product_listbox.curselection()
        if selection:
            item_text = self.product_listbox.get(selection)
            product_id = item_text.split('|')[0].replace("ID:", "").strip()
            
            if messagebox.askyesno("Confirm", "Voulez-vous vraiment supprimer ce produit ?"):
                try:
                    self.db_cursor.execute("DELETE FROM product WHERE id = %s", (product_id,))
                    self.db_connection.commit()
                    self.load_data()
                except mysql.connector.Error as err:
                    messagebox.showerror("Error", f"Erreur de suppression : {err}")
        else:
            messagebox.showwarning("Selection", "Veuillez sélectionner un produit")

    def clear_form(self):
        """Vide les champs du formulaire"""
        self.name_entry.delete(0, tk.END)
        self.desc_entry.delete(0, tk.END)
        self.price_entry.delete(0, tk.END)
        self.quantity_entry.delete(0, tk.END)
        self.cat_entry.delete(0, tk.END)

if __name__ == "__main__":
    window = tk.Tk()
    app = StockManager(window)
    window.mainloop()