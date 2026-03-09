import tkinter as tk
from tkinter import messagebox, ttk, filedialog
import mysql.connector
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import pandas as pd

class ModernStockManager:
    def __init__(self, root):
        self.colors = {
            "bg": "#f0f2f5",
            "sidebar": "#1e293b",
            "accent": "#3b82f6",
            "success": "#10b981",
            "danger": "#ef4444",
            "card": "#ffffff"
        }
        
        try:
            self.db_connection = mysql.connector.connect(host="localhost", user="root", password="root", database="store")
            self.db_cursor = self.db_connection.cursor()
        except Exception as e:
            messagebox.showerror("Erreur", f"Base de données non trouvée : {e}"); root.destroy()

        self.root = root
        self.root.title("Inventory Pro - Dashboard Optimisé")
        self.root.geometry("1400x850") # Taille optimisée pour la visibilité
        self.root.configure(bg=self.colors["bg"])
        
        self.setup_styles()
        self.setup_ui()
        self.refresh_categories()
        self.load_data()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure("Treeview", background="white", fieldbackground="white", rowheight=30, font=("Segoe UI", 10))
        style.configure("Treeview.Heading", font=("Segoe UI", 10, "bold"), background="#f8fafc")
        style.configure("TNotebook", background=self.colors["bg"], borderwidth=0)
        style.configure("TNotebook.Tab", font=("Segoe UI", 0)) # Cache les onglets texte

    def setup_ui(self):
        # --- SIDEBAR (Largeur fixe réduite) ---
        sidebar = tk.Frame(self.root, bg=self.colors["sidebar"], width=200)
        sidebar.pack(side="left", fill="y")
        sidebar.pack_propagate(False)

        tk.Label(sidebar, text="📦 STOCK PRO", fg="white", bg=self.colors["sidebar"], font=("Segoe UI", 14, "bold"), pady=25).pack()

        for txt, idx in [("📊 Dashboard", 0), ("📁 Catégories", 1)]:
            btn = tk.Button(sidebar, text=txt, fg="white", bg=self.colors["sidebar"], bd=0, font=("Segoe UI", 11), 
                            pady=12, cursor="hand2", anchor="w", padx=20, command=lambda i=idx: self.notebook.select(i))
            btn.pack(fill="x")

        # --- MAIN CONTAINER ---
        self.main_container = tk.Frame(self.root, bg=self.colors["bg"], padx=20, pady=15)
        self.main_container.pack(side="right", fill="both", expand=True)

        # KPI Bar (Plus compacte)
        self.kpi_frame = tk.Frame(self.main_container, bg=self.colors["bg"])
        self.kpi_frame.pack(fill="x", pady=(0, 15))
        
        self.stats = {}
        for label, color in [("Total Produits", self.colors["accent"]), ("Valeur Stock", self.colors["success"]), ("Alertes", self.colors["danger"])]:
            card = tk.Frame(self.kpi_frame, bg="white", padx=15, pady=10, highlightthickness=1, highlightbackground="#e2e8f0")
            card.pack(side="left", fill="both", expand=True, padx=5)
            tk.Label(card, text=label, bg="white", fg="gray", font=("Segoe UI", 9)).pack(anchor="w")
            self.stats[label] = tk.Label(card, text="0", bg="white", font=("Segoe UI", 15, "bold"), fg=color)
            self.stats[label].pack(anchor="w")

        # Notebook sans bordures
        self.notebook = ttk.Notebook(self.main_container)
        self.notebook.pack(fill="both", expand=True)
        
        self.tab_stock = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.tab_cat = tk.Frame(self.notebook, bg=self.colors["bg"])
        self.notebook.add(self.tab_stock, text="S")
        self.notebook.add(self.tab_cat, text="C")

        self.setup_stock_content()
        self.setup_category_content()

    def setup_stock_content(self):
        # Zone de contenu principal
        content = tk.Frame(self.tab_stock, bg=self.colors["bg"])
        content.pack(fill="both", expand=True)

        # GAUCHE : Table (Plus large)
        left_side = tk.Frame(content, bg="white", padx=15, pady=15, highlightthickness=1, highlightbackground="#e2e8f0")
        left_side.pack(side="left", fill="both", expand=True)

        # Recherche
        search_f = tk.Frame(left_side, bg="white")
        search_f.pack(fill="x", pady=(0, 10))
        self.search_entry = ttk.Entry(search_f, font=("Segoe UI", 10))
        self.search_entry.pack(side="left", fill="x", expand=True)
        self.search_entry.insert(0, "Rechercher...")
        self.search_entry.bind("<KeyRelease>", lambda e: self.load_data())

        # Table + Scrollbar
        table_frame = tk.Frame(left_side, bg="white")
        table_frame.pack(fill="both", expand=True)
        
        self.tree = ttk.Treeview(table_frame, columns=("name", "qty", "cat", "price"), show="headings")
        sb = ttk.Scrollbar(table_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=sb.set)
        
        for col, head, w in [("name", "Nom", 200), ("qty", "Qté", 60), ("cat", "Catégorie", 100), ("price", "Prix (€)", 80)]:
            self.tree.heading(col, text=head)
            self.tree.column(col, width=w, anchor="center")
        
        self.tree.pack(side="left", fill="both", expand=True)
        sb.pack(side="right", fill="y")

        # DROITE : Formulaire et Graphique (Plus étroit pour laisser place au tableau)
        right_side = tk.Frame(content, bg=self.colors["bg"], width=320)
        right_side.pack(side="right", fill="y", padx=(15, 0))
        right_side.pack_propagate(False)

        # Formulaire compact
        form_card = tk.Frame(right_side, bg="white", padx=15, pady=15, highlightthickness=1, highlightbackground="#e2e8f0")
        form_card.pack(fill="x")
        
        self.entries = {}
        for label, key in [("Nom", "name"), ("Prix", "price"), ("Quantité", "qty")]:
            tk.Label(form_card, text=label, bg="white", font=("Segoe UI", 9)).pack(anchor="w")
            self.entries[key] = ttk.Entry(form_card)
            self.entries[key].pack(fill="x", pady=(0, 8))

        tk.Label(form_card, text="Catégorie", bg="white", font=("Segoe UI", 9)).pack(anchor="w")
        self.cat_selector = ttk.Combobox(form_card, state="readonly")
        self.cat_selector.pack(fill="x", pady=(0, 15))

        tk.Button(form_card, text="Ajouter au Stock", bg=self.colors["accent"], fg="white", bd=0, pady=8, command=self.add_product).pack(fill="x", pady=2)
        tk.Button(form_card, text="Supprimer", bg=self.colors["danger"], fg="white", bd=0, pady=5, command=self.delete_product).pack(fill="x", pady=5)

        # Graphique (Taille fixe)
        self.chart_card = tk.Frame(right_side, bg="white", pady=5, padx=5, highlightthickness=1, highlightbackground="#e2e8f0")
        self.chart_card.pack(fill="both", expand=True, pady=(15, 0))
        self.fig, self.ax = plt.subplots(figsize=(3, 2.5), dpi=80)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self.chart_card)
        self.canvas.get_tk_widget().pack(fill="both")

    def setup_category_content(self):
        card = tk.Frame(self.tab_cat, bg="white", padx=30, pady=30, highlightthickness=1, highlightbackground="#e2e8f0")
        card.place(relx=0.5, rely=0.4, anchor="center")
        
        tk.Label(card, text="Gestion des Catégories", font=("Segoe UI", 12, "bold"), bg="white").pack(pady=(0, 15))
        self.new_cat_entry = ttk.Entry(card, width=35)
        self.new_cat_entry.pack(pady=5)
        tk.Button(card, text="Créer", bg=self.colors["success"], fg="white", bd=0, pady=8, width=20, command=self.add_category).pack(pady=10)
        
        self.cat_listbox = tk.Listbox(card, width=40, height=8, font=("Segoe UI", 10), bd=0, highlightthickness=1)
        self.cat_listbox.pack(pady=10)
        tk.Button(card, text="Supprimer sélection", bg=self.colors["danger"], fg="white", bd=0, pady=5, command=self.delete_category).pack(fill="x")

    # --- LOGIQUE ---
    def load_data(self):
        for i in self.tree.get_children(): self.tree.delete(i)
        search = self.search_entry.get() if self.search_entry.get() != "Rechercher..." else ""
        self.db_cursor.execute("SELECT p.name, p.quantity, c.name, p.price, p.id FROM product p LEFT JOIN category c ON p.id_category = c.id WHERE p.name LIKE %s", (f"%{search}%",))
        rows = self.db_cursor.fetchall()
        
        total_val, total_items, alerts = 0, 0, 0
        for row in rows:
            self.tree.insert("", "end", values=row[:4], tags=(row[4],))
            total_items += row[1]
            total_val += (row[1] * row[3])
            if row[1] < 5: alerts += 1

        self.stats["Total Produits"].config(text=str(total_items))
        self.stats["Valeur Stock"].config(text=f"{total_val:,.0f} €")
        self.stats["Alertes"].config(text=str(alerts))
        self.update_chart()

    def update_chart(self):
        self.db_cursor.execute("SELECT c.name, SUM(p.quantity) FROM product p JOIN category c ON p.id_category = c.id GROUP BY c.name")
        data = self.db_cursor.fetchall()
        self.ax.clear()
        if data:
            self.ax.pie([r[1] for r in data], labels=[r[0] for r in data], autopct='%1.0f%%', colors=['#3b82f6', '#10b981', '#f59e0b', '#ef4444'], textprops={'fontsize': 8})
        self.canvas.draw()

    def refresh_categories(self):
        self.db_cursor.execute("SELECT id, name FROM category")
        self.categories_data = self.db_cursor.fetchall()
        names = [c[1] for c in self.categories_data]
        self.cat_selector['values'] = names
        self.cat_listbox.delete(0, tk.END)
        for name in names: self.cat_listbox.insert(tk.END, name)

    def add_product(self):
        vals = {k: e.get() for k, e in self.entries.items()}
        cat = self.cat_selector.get()
        if all(vals.values()) and cat:
            cat_id = [c[0] for c in self.categories_data if c[1] == cat][0]
            self.db_cursor.execute("INSERT INTO product (name, price, quantity, id_category) VALUES (%s,%s,%s,%s)", (vals['name'], vals['price'], vals['qty'], cat_id))
            self.db_connection.commit(); self.load_data()
            for e in self.entries.values(): e.delete(0, tk.END)

    def delete_product(self):
        sel = self.tree.selection()
        if sel:
            db_id = self.tree.item(sel[0])['tags'][0]
            if messagebox.askyesno("?", "Supprimer cet article ?"):
                self.db_cursor.execute("DELETE FROM product WHERE id = %s", (db_id,))
                self.db_connection.commit(); self.load_data()

    def add_category(self):
        name = self.new_cat_entry.get()
        if name:
            self.db_cursor.execute("INSERT INTO category (name) VALUES (%s)", (name,))
            self.db_connection.commit(); self.refresh_categories(); self.new_cat_entry.delete(0, tk.END)

    def delete_category(self):
        sel = self.cat_listbox.curselection()
        if sel:
            name = self.cat_listbox.get(sel)
            self.db_cursor.execute("DELETE FROM category WHERE name = %s", (name,))
            self.db_connection.commit(); self.refresh_categories(); self.load_data()

if __name__ == "__main__":
    root = tk.Tk()
    app = ModernStockManager(root)
    root.mainloop()