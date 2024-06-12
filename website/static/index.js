if ( window.history.replaceState ) {
    window.history.replaceState( null, null, window.location.href );
}

function deleteBook(bookId, userId) {
    fetch('/delete-book', {
        method: 'POST',
        body: JSON.stringify({bookId: bookId, userId: userId})
    }).then((_res) => {
        window.location.href = currentPage;
    })
}