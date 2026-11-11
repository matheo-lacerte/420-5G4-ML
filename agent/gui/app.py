"""Interface graphique de consultation de la bibliotheque C++."""

import argparse
import sys
from pathlib import Path

import customtkinter as ctk


PROJECT_DIR = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PROJECT_DIR / "build"))

try:
    import bibliotheque_cpp as library_cpp
except ImportError as error:
    raise SystemExit(
        "Module C++ introuvable. Compilez le projet avec "
        "'cmake -S agent -B agent/build && cmake --build agent/build'."
    ) from error


class LibraryApp(ctk.CTk):
    def __init__(self, data_dir: Path):
        super().__init__()
        self.data_dir = data_dir
        self.library = library_cpp.Library()
        self.manager = library_cpp.FileManager(str(data_dir / "books.txt"), str(data_dir / "users.txt"))
        self.available_only = False
        self.search_text = ""
        self.view = "books"

        self.title("Bibliotheque personnelle")
        self.geometry("980x650")
        self.minsize(760, 520)
        self.configure(fg_color=("#f4f0e8", "#1c2228"))

        self.create_layout()
        self.reload_data()

    def create_layout(self):
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(2, weight=1)

        header = ctk.CTkFrame(self, corner_radius=0, fg_color=("#243b53", "#14212e"))
        header.grid(row=0, column=0, sticky="ew")
        header.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(
            header, text="BIBLIOTHEQUE", font=ctk.CTkFont(size=26, weight="bold"), text_color="#f7d488"
        ).grid(row=0, column=0, padx=28, pady=(22, 2), sticky="w")
        ctk.CTkLabel(
            header, text="Consultation du catalogue", font=ctk.CTkFont(size=14), text_color="#d7e2eb"
        ).grid(row=1, column=0, padx=28, pady=(0, 22), sticky="w")

        dashboard = ctk.CTkFrame(self, fg_color="transparent")
        dashboard.grid(row=1, column=0, padx=28, pady=22, sticky="ew")
        for column in range(4):
            dashboard.grid_columnconfigure(column, weight=1)
        self.total_label = self.stat_card(dashboard, 0, "CATALOGUE", "Livres charges")
        self.available_label = self.stat_card(dashboard, 1, "DISPONIBLES", "Prets a emprunter")
        self.borrowed_label = self.stat_card(dashboard, 2, "EMPRUNTES", "Livres sortis")
        self.users_label = self.stat_card(dashboard, 3, "LECTEURS", "Utilisateurs inscrits")

        content = ctk.CTkFrame(self, corner_radius=14)
        content.grid(row=2, column=0, padx=28, pady=(0, 28), sticky="nsew")
        content.grid_columnconfigure(0, weight=1)
        content.grid_rowconfigure(1, weight=1)

        self.toolbar = ctk.CTkFrame(content, fg_color="transparent")
        self.toolbar.grid(row=0, column=0, padx=20, pady=(18, 8), sticky="ew")
        self.toolbar.grid_columnconfigure(0, weight=1)
        self.search = ctk.CTkEntry(self.toolbar, placeholder_text="Rechercher par titre ou auteur")
        self.search.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        self.search.bind("<KeyRelease>", lambda event: self.filter_books())
        self.filter_button = ctk.CTkButton(self.toolbar, text="Disponibles", width=115, command=self.toggle_available)
        self.filter_button.grid(row=0, column=1, padx=4)
        ctk.CTkButton(self.toolbar, text="Ajouter un livre", command=self.show_add_book, width=125).grid(row=0, column=2, padx=4)
        ctk.CTkButton(self.toolbar, text="Ajouter un lecteur", command=self.show_add_user, width=135).grid(row=0, column=3, padx=4)
        ctk.CTkButton(self.toolbar, text="Lecteurs", command=self.show_users_view, width=100).grid(row=0, column=4, padx=4)
        ctk.CTkButton(self.toolbar, text="Emprunter", command=self.show_checkout, width=105).grid(row=0, column=5, padx=4)
        ctk.CTkButton(self.toolbar, text="Sauvegarde", command=self.create_backup, width=110).grid(row=0, column=6, padx=4)
        ctk.CTkButton(self.toolbar, text="Actualiser", command=self.reload_data, width=110).grid(row=0, column=7, padx=(4, 0))

        self.book_list = ctk.CTkScrollableFrame(content, fg_color="transparent")
        self.book_list.grid(row=1, column=0, padx=20, pady=(0, 12), sticky="nsew")
        self.status_label = ctk.CTkLabel(content, text="", anchor="w", text_color="gray")
        self.status_label.grid(row=2, column=0, padx=20, pady=(0, 16), sticky="ew")

    def stat_card(self, parent, column, title, subtitle):
        card = ctk.CTkFrame(parent, corner_radius=14)
        card.grid(row=0, column=column, padx=5, sticky="ew")
        ctk.CTkLabel(card, text=title, font=ctk.CTkFont(size=11, weight="bold"), text_color="#d9993c").pack(
            anchor="w", padx=15, pady=(12, 0)
        )
        value = ctk.CTkLabel(card, text="-", font=ctk.CTkFont(size=27, weight="bold"))
        value.pack(anchor="w", padx=15)
        ctk.CTkLabel(card, text=subtitle, text_color="gray").pack(anchor="w", padx=15, pady=(0, 12))
        return value

    def reload_data(self):
        if not self.data_dir.is_dir():
            self.status_label.configure(text=f"Repertoire introuvable : {self.data_dir}", text_color="#c94c4c")
            return
        self.library = library_cpp.Library()
        self.manager.load(self.library)
        self.total_label.configure(text=str(self.library.total_books))
        self.available_label.configure(text=str(self.library.available_book_count))
        self.borrowed_label.configure(text=str(self.library.checked_out_book_count))
        self.users_label.configure(text=str(len(self.library.all_users())))
        self.render_view()
        self.status_label.configure(text=f"Donnees chargees depuis {self.data_dir}", text_color="gray")

    def toggle_available(self):
        self.available_only = not self.available_only
        self.filter_button.configure(text="Tous les livres" if self.available_only else "Disponibles")
        self.filter_books()

    def filter_books(self):
        self.search_text = self.search.get().casefold()
        if self.view == "books":
            self.show_books()

    def render_view(self):
        if self.view == "books":
            self.show_books()
        else:
            self.show_users()

    def show_users_view(self):
        self.view = "users"
        for widget in self.toolbar.winfo_children():
            widget.destroy()
        self.toolbar.grid_columnconfigure(0, weight=1)
        ctk.CTkLabel(self.toolbar, text="Lecteurs et emprunts", font=ctk.CTkFont(size=17, weight="bold")).grid(
            row=0, column=0, sticky="w"
        )
        ctk.CTkButton(self.toolbar, text="Catalogue", command=self.show_books_view, width=110).grid(row=0, column=1, padx=4)
        ctk.CTkButton(self.toolbar, text="Ajouter un lecteur", command=self.show_add_user, width=135).grid(row=0, column=2, padx=4)
        ctk.CTkButton(self.toolbar, text="Sauvegarde", command=self.create_backup, width=110).grid(row=0, column=3, padx=4)
        ctk.CTkButton(self.toolbar, text="Actualiser", command=self.reload_data, width=110).grid(row=0, column=4, padx=(4, 0))
        self.show_users()

    def show_books_view(self):
        self.view = "books"
        for widget in self.toolbar.winfo_children():
            widget.destroy()
        self.toolbar.grid_columnconfigure(0, weight=1)
        self.search = ctk.CTkEntry(self.toolbar, placeholder_text="Rechercher par titre ou auteur")
        self.search.insert(0, self.search_text)
        self.search.grid(row=0, column=0, padx=(0, 8), sticky="ew")
        self.search.bind("<KeyRelease>", lambda event: self.filter_books())
        self.filter_button = ctk.CTkButton(self.toolbar, text="Tous les livres" if self.available_only else "Disponibles", width=115, command=self.toggle_available)
        self.filter_button.grid(row=0, column=1, padx=4)
        ctk.CTkButton(self.toolbar, text="Ajouter un livre", command=self.show_add_book, width=125).grid(row=0, column=2, padx=4)
        ctk.CTkButton(self.toolbar, text="Ajouter un lecteur", command=self.show_add_user, width=135).grid(row=0, column=3, padx=4)
        ctk.CTkButton(self.toolbar, text="Lecteurs", command=self.show_users_view, width=100).grid(row=0, column=4, padx=4)
        ctk.CTkButton(self.toolbar, text="Emprunter", command=self.show_checkout, width=105).grid(row=0, column=5, padx=4)
        ctk.CTkButton(self.toolbar, text="Sauvegarde", command=self.create_backup, width=110).grid(row=0, column=6, padx=4)
        ctk.CTkButton(self.toolbar, text="Actualiser", command=self.reload_data, width=110).grid(row=0, column=7, padx=(4, 0))
        self.show_books()

    def show_books(self):
        for widget in self.book_list.winfo_children():
            widget.destroy()
        books = [
            book
            for book in self.library.all_books()
            if self.search_text in book.title.casefold() or self.search_text in book.author.casefold()
        ]
        if self.available_only:
            books = [book for book in books if book.available]
        if not books:
            ctk.CTkLabel(self.book_list, text="Aucun livre ne correspond a cette recherche.", text_color="gray").pack(pady=30)
            return
        for book in books:
            row = ctk.CTkFrame(self.book_list)
            row.pack(fill="x", pady=4)
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(row, text=book.title, font=ctk.CTkFont(weight="bold"), anchor="w").grid(
                row=0, column=0, padx=14, pady=(9, 0), sticky="ew"
            )
            ctk.CTkLabel(row, text=f"{book.author}  |  ISBN {book.isbn}", text_color="gray", anchor="w").grid(
                row=1, column=0, padx=14, pady=(0, 9), sticky="ew"
            )
            status = "Disponible" if book.available else f"Emprunte par {book.borrower_id}"
            color = "#397a57" if book.available else "#b66a45"
            ctk.CTkLabel(row, text=status, text_color=color).grid(row=0, column=1, rowspan=2, padx=14)
            checkout_button = ctk.CTkButton(
                row,
                text="Emprunter",
                width=100,
                command=lambda isbn=book.isbn: self.show_checkout(isbn),
            )
            checkout_button.grid(row=0, column=2, rowspan=2, padx=(0, 4))
            if not book.available:
                checkout_button.configure(state="disabled")
            return_button = ctk.CTkButton(
                row,
                text="Retourner",
                width=100,
                command=lambda isbn=book.isbn: self.return_book(isbn),
            )
            return_button.grid(row=0, column=3, rowspan=2, padx=(0, 4))
            if book.available:
                return_button.configure(state="disabled")
            delete_button = ctk.CTkButton(
                row,
                text="Supprimer",
                width=100,
                fg_color="#a64b4b",
                hover_color="#873c3c",
                command=lambda isbn=book.isbn: self.remove_book(isbn),
            )
            delete_button.grid(row=0, column=4, rowspan=2, padx=(0, 14))
            if not book.available:
                delete_button.configure(state="disabled")

    def show_users(self):
        for widget in self.book_list.winfo_children():
            widget.destroy()
        users = self.library.all_users()
        if not users:
            ctk.CTkLabel(self.book_list, text="Aucun lecteur enregistre.", text_color="gray").pack(pady=30)
            return
        for user in users:
            row = ctk.CTkFrame(self.book_list)
            row.pack(fill="x", pady=4)
            row.grid_columnconfigure(0, weight=1)
            ctk.CTkLabel(row, text=user.name, font=ctk.CTkFont(weight="bold"), anchor="w").grid(
                row=0, column=0, padx=14, pady=(9, 0), sticky="ew"
            )
            borrowed = ", ".join(user.borrowed_books) or "Aucun emprunt"
            ctk.CTkLabel(row, text=f"ID {user.user_id}  |  {borrowed}", text_color="gray", anchor="w").grid(
                row=1, column=0, padx=14, pady=(0, 9), sticky="ew"
            )

    def show_add_book(self):
        window = ctk.CTkToplevel(self)
        window.title("Ajouter un livre")
        window.geometry("390x280")
        window.resizable(False, False)
        window.transient(self)
        window.grab_set()

        entries = []
        for label, placeholder in [
            ("Titre", "Titre du livre"),
            ("Auteur", "Nom de l'auteur"),
            ("ISBN", "Identifiant unique"),
        ]:
            ctk.CTkLabel(window, text=label).pack(fill="x", padx=24, pady=(16 if not entries else 8, 0))
            entry = ctk.CTkEntry(window, placeholder_text=placeholder)
            entry.pack(fill="x", padx=24, pady=(4, 0))
            entries.append(entry)
        ctk.CTkButton(window, text="Ajouter", command=lambda: self.add_book(window, entries)).pack(pady=22)
        entries[0].focus()

    def add_book(self, window, entries):
        title, author, isbn = (entry.get().strip() for entry in entries)
        if not title or not author or not isbn:
            self.show_status("Tous les champs sont requis.", error=True)
            return
        if self.library.get_book(isbn):
            self.show_status(f"Un livre avec l'ISBN {isbn} existe deja.", error=True)
            return
        self.library.add_book(library_cpp.Book(title, author, isbn))
        if not self.manager.save_books(self.library):
            self.show_status("Impossible de sauvegarder le livre.", error=True)
            return
        self.show_books()
        self.total_label.configure(text=str(self.library.total_books))
        self.available_label.configure(text=str(self.library.available_book_count))
        self.show_status(f"Livre '{title}' ajoute et sauvegarde.")
        window.destroy()

    def remove_book(self, isbn):
        book = self.library.get_book(isbn)
        if not book or not book.available:
            self.show_status("Un livre emprunte ne peut pas etre supprime.", error=True)
            return
        if not self.library.remove_book(isbn):
            self.show_status("Impossible de supprimer le livre.", error=True)
            return
        if not self.manager.save_books(self.library):
            self.show_status("Livre supprime, mais sauvegarde impossible.", error=True)
            return
        self.show_books()
        self.total_label.configure(text=str(self.library.total_books))
        self.available_label.configure(text=str(self.library.available_book_count))
        self.show_status(f"Livre {isbn} supprime et sauvegarde.")

    def show_add_user(self):
        window = ctk.CTkToplevel(self)
        window.title("Ajouter un lecteur")
        window.geometry("390x220")
        window.resizable(False, False)
        window.transient(self)
        window.grab_set()

        ctk.CTkLabel(window, text="Nom du lecteur").pack(fill="x", padx=24, pady=(20, 0))
        name_entry = ctk.CTkEntry(window, placeholder_text="Nom complet")
        name_entry.pack(fill="x", padx=24, pady=(4, 0))
        ctk.CTkLabel(window, text="ID du lecteur").pack(fill="x", padx=24, pady=(12, 0))
        user_id_entry = ctk.CTkEntry(window, placeholder_text="Identifiant unique")
        user_id_entry.pack(fill="x", padx=24, pady=(4, 0))
        ctk.CTkButton(
            window,
            text="Ajouter le lecteur",
            command=lambda: self.add_user(window, name_entry.get().strip(), user_id_entry.get().strip()),
        ).pack(pady=22)
        name_entry.focus()

    def add_user(self, window, name, user_id):
        if not name or not user_id:
            self.show_status("Le nom et l'ID du lecteur sont requis.", error=True)
            return
        if self.library.get_user(user_id):
            self.show_status(f"Un lecteur avec l'ID {user_id} existe deja.", error=True)
            return
        self.library.add_user(library_cpp.User(name, user_id))
        if not self.manager.save_users(self.library):
            self.show_status("Impossible de sauvegarder le lecteur.", error=True)
            return
        self.users_label.configure(text=str(len(self.library.all_users())))
        self.show_status(f"Lecteur '{name}' ajoute et sauvegarde.")
        window.destroy()

    def show_checkout(self, isbn=""):
        window = ctk.CTkToplevel(self)
        window.title("Emprunter un livre")
        window.geometry("390x220")
        window.resizable(False, False)
        window.transient(self)
        window.grab_set()

        ctk.CTkLabel(window, text="ISBN du livre").pack(fill="x", padx=24, pady=(20, 0))
        isbn_entry = ctk.CTkEntry(window, placeholder_text="ISBN")
        isbn_entry.insert(0, isbn)
        isbn_entry.pack(fill="x", padx=24, pady=(4, 0))
        ctk.CTkLabel(window, text="ID du lecteur").pack(fill="x", padx=24, pady=(12, 0))
        user_entry = ctk.CTkEntry(window, placeholder_text="Identifiant du lecteur")
        user_entry.pack(fill="x", padx=24, pady=(4, 0))
        ctk.CTkButton(
            window,
            text="Confirmer l'emprunt",
            command=lambda: self.checkout(window, isbn_entry.get().strip(), user_entry.get().strip()),
        ).pack(pady=22)
        (user_entry if isbn else isbn_entry).focus()

    def checkout(self, window, isbn, user_id):
        if not isbn or not user_id:
            self.show_status("L'ISBN et l'ID du lecteur sont requis.", error=True)
            return
        if not self.library.check_out_book(isbn, user_id):
            self.show_status("Emprunt impossible : livre, lecteur ou disponibilite invalide.", error=True)
            return
        if not self.manager.save(self.library):
            self.show_status("Emprunt effectue, mais sauvegarde impossible.", error=True)
            return
        self.available_label.configure(text=str(self.library.available_book_count))
        self.borrowed_label.configure(text=str(self.library.checked_out_book_count))
        self.render_view()
        self.show_status(f"Livre {isbn} emprunte par le lecteur {user_id}.")
        window.destroy()

    def return_book(self, isbn):
        if not self.library.return_book(isbn):
            self.show_status("Retour impossible : ISBN invalide ou livre non emprunte.", error=True)
            return
        if not self.manager.save(self.library):
            self.show_status("Retour effectue, mais sauvegarde impossible.", error=True)
            return
        self.available_label.configure(text=str(self.library.available_book_count))
        self.borrowed_label.configure(text=str(self.library.checked_out_book_count))
        self.render_view()
        self.show_status(f"Livre {isbn} retourne et sauvegarde.")

    def create_backup(self):
        try:
            self.manager.create_backup()
        except RuntimeError as error:
            self.show_status(f"Sauvegarde impossible : {error}", error=True)
            return
        self.show_status("Sauvegardes books.txt.backup et users.txt.backup creees.")

    def show_status(self, text, error=False):
        self.status_label.configure(text=text, text_color="#c94c4c" if error else "gray")


def main():
    parser = argparse.ArgumentParser(description="Interface graphique de la bibliotheque")
    parser.add_argument("--data-dir", type=Path, default=PROJECT_DIR / "data")
    arguments = parser.parse_args()
    ctk.set_appearance_mode("system")
    ctk.set_default_color_theme("blue")
    LibraryApp(arguments.data_dir).mainloop()


if __name__ == "__main__":
    main()
