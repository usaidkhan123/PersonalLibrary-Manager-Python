
import json  # json is used for storing or managing data  
import streamlit as st  # Streamlit for UI

class BookCollection:  # class is blueprint for creating objects in which we define methods
    """A class to manage a collection of books, allowing users to store and organize their favorite books."""  # docstring code ko explain krne ke liye istemal hota hai
    
    def __init__(self):  # self keyword/parameter is used to manage data. init method is basically initializing our class.
        """ Initialize a new book collection with an empty list and set up file storage. """
        self.book_list = []  # book_list variable stores an empty list in it. In this list, users store multiple types of data
        self.storage_file = "books_data.json"  # the file where book data is stored
        self.read_from_file()  # call the function to load books from file
    
    def read_from_file(self):  # for reading file
        """Load saved books from a json file into memory.
        If the file does not exist or is corrupted, start with an empty collection. """
        try:
            with open(self.storage_file, "r") as file:  # with keyword is for resource management. Open function takes our variable (storage_file) and opens it in read format. file is the nickname of the expression
                self.book_list = json.load(file)  # convert json data into python list
        except (FileNotFoundError, json.JSONDecodeError):  # if file does not exist or is corrupted, show it as an empty list
            self.book_list = []
    
    def save_to_file(self):  # for storing data in file
        """Store the current book collection to a json file for permanent storage."""
        with open(self.storage_file, "w") as file:  # with keyword is for resource management. Open function takes our variable (storage_file) and opens it in write format. file is the nickname of the expression
            json.dump(self.book_list, file, indent=4)  # dump method is dumping our data in json format
    
    def create_new_book(self):  # for creating new book
        """Add a new book to the collection by gathering information from the user."""
        st.subheader("Add a New Book")
        book_title = st.text_input("Enter The Book Title")
        book_author = st.text_input("Enter Author")
        publication_year = st.text_input("Enter Publication Year")
        book_genre = st.text_input("Enter Genre")
        is_book_read = st.checkbox("Have you read this book?")
        
        if st.button("Add Book"):  # if user clicks add button
            new_book = {
                "title": book_title,
                "author": book_author,
                "year": publication_year,
                "genre": book_genre,
                "read": is_book_read,
            }
            self.book_list.append(new_book)  # adding dictionary in empty book_list
            self.save_to_file()  # method call
            st.success("Book added successfully!")
    
    def delete_book(self):  # for removing book
        """Remove a book from the collection using its title."""
        st.subheader("Remove a Book")
        book_titles = [book["title"] for book in self.book_list]
        book_to_remove = st.selectbox("Select a book to remove", book_titles) if book_titles else None
        
        if book_to_remove and st.button("Remove Book"):  # if book exists and button is clicked
            self.book_list = [book for book in self.book_list if book["title"] != book_to_remove]
            self.save_to_file()
            st.success("Book removed successfully!")
    
    def show_all_books(self):  # for displaying books
        """Display all books in the collection with their details."""
        st.subheader("Your Book Collection")
        if not self.book_list:  # if no book exists
            st.info("Your collection is empty.")
        else:
            for index, book in enumerate(self.book_list, 1):  # enumerate loops through each list and gives each book a number
                reading_status = "Read" if book["read"] else "Unread"
                st.write(f"{index}. **{book['title']}** by {book['author']} ({book['year']}) - {book['genre']} - {reading_status}")
    
    def show_reading_progress(self):  # for calculating progress
        """Calculate and display statistics about your reading progress."""
        total_books = len(self.book_list)
        completed_books = sum(1 for book in self.book_list if book["read"])  # count how many books are marked as read
        completion_rate = (completed_books / total_books * 100) if total_books > 0 else 0  # if there are zero books, avoid division error
        
        st.subheader("Reading Progress")
        st.write(f"Total books in collection: {total_books}")
        st.write(f"Reading progress: {completion_rate:.2f}%")  # .2f means print percentage with a maximum of two decimals
    
    def start_application(self):  # run Streamlit UI
        """Run the Streamlit UI."""
        st.title("📚 Book Collection Manager")
        menu = ["Add Book", "Remove Book", "View Books", "View Progress"]
        choice = st.sidebar.radio("Select an option", menu)
        
        if choice == "Add Book":
            self.create_new_book()
        elif choice == "Remove Book":
            self.delete_book()
        elif choice == "View Books":
            self.show_all_books()
        elif choice == "View Progress":
            self.show_reading_progress()

if __name__ == "__main__":  # __name__ tells us the inner working of Python
    book_manager = BookCollection()  # when we run our main.py, first it runs book_manager variable
    book_manager.start_application()  # then it runs start_application method
