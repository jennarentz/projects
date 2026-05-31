function deleteNote(noteId) {
    if (!confirm('Are you sure you want to delete this note?')) {
        return;  // cancel if not confirmed
    }

    fetch('/delete-note', {
        method: 'POST',
        body: JSON.stringify({ noteId: noteId }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then((_res) => {
        window.location.href = '/';
    });
}
