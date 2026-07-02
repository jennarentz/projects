function deletePost(postId) {
    if (!confirm('Are you sure you want to delete this post?')) {
        return;  // cancel if not confirmed
    }

    fetch('/delete-post', {
        method: 'POST',
        body: JSON.stringify({ postId: postId }),
        headers: {
            'Content-Type': 'application/json'
        }
    }).then((_res) => {
        window.location.href = '/';
    });
}
