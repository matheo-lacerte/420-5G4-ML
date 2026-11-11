#include <pybind11/pybind11.h>
#include <pybind11/stl.h>

#include "book.h"
#include "filemanager.h"
#include "library.h"
#include "user.h"

namespace py = pybind11;

PYBIND11_MODULE(bibliotheque_cpp, module) {
    module.doc() = "Bibliotheque C++ exposee a Python.";

    py::class_<Book>(module, "Book")
        .def(py::init<const std::string&, const std::string&, const std::string&>())
        .def_property("title", &Book::getTitle, &Book::setTitle)
        .def_property("author", &Book::getAuthor, &Book::setAuthor)
        .def_property("isbn", &Book::getISBN, &Book::setISBN)
        .def_property_readonly("available", &Book::getAvailability)
        .def_property_readonly("borrower_id", &Book::getBorrowerId);

    py::class_<User>(module, "User")
        .def(py::init<const std::string&, const std::string&>())
        .def_property("name", &User::getName, &User::setName)
        .def_property("user_id", &User::getUserId, &User::setUserId)
        .def_property_readonly("borrowed_books", &User::getBorrowedBooks);

    py::class_<Library>(module, "Library")
        .def(py::init<>())
        .def("add_book", &Library::addBook)
        .def("remove_book", &Library::removeBook)
        .def("get_book", &Library::findBookByISBN,
             py::return_value_policy::reference_internal)
        .def("search_books_by_title", &Library::searchBooksByTitle,
             py::return_value_policy::reference_internal)
        .def("search_books_by_author", &Library::searchBooksByAuthor,
             py::return_value_policy::reference_internal)
        .def("available_books", &Library::getAvailableBooks,
             py::return_value_policy::reference_internal)
        .def("all_books", &Library::getAllBooks,
             py::return_value_policy::reference_internal)
        .def("add_user", &Library::addUser)
        .def("get_user", &Library::findUserById,
             py::return_value_policy::reference_internal)
        .def("all_users", &Library::getAllUsers,
             py::return_value_policy::reference_internal)
        .def("check_out_book", &Library::checkOutBook)
        .def("return_book", &Library::returnBook)
        .def_property_readonly("total_books", &Library::getTotalBooks)
        .def_property_readonly("available_book_count", &Library::getAvailableBookCount)
        .def_property_readonly("checked_out_book_count", &Library::getCheckedOutBookCount);

    py::class_<FileManager>(module, "FileManager")
        .def(py::init<const std::string&, const std::string&>())
        .def("load", &FileManager::loadLibraryData)
        .def("save", &FileManager::saveLibraryData)
        .def("save_books", &FileManager::saveBooksToFile)
        .def("save_users", &FileManager::saveUsersToFile)
        .def("create_backup", &FileManager::createBackup);
}
