document.addEventListener('DOMContentLoaded', function() {
    document.body.addEventListener('htmx:afterRequest', function(evt) {
        if (evt.detail.elt.id === 'review-form') {
            document.getElementById('review-form-container').style.display = 'none';
            document.getElementById('review-form-container').innerHTML = '';
        }
    });

    document.body.addEventListener('refreshReviews', function() {
        htmx.ajax('GET', '/reviews', '#reviews-list', {
            swap: 'innerHTML',
            headers: {'HX-Request': 'true'},
        });
    });

    document.body.addEventListener('hideWriteButton', function() {
        const writeButton = document.querySelector('#write-review-btn');
        if (writeButton) {
            writeButton.style.display = 'none';
        }
    });

    document.body.addEventListener('htmx:beforeSwap', function(evt) {
        if (evt.detail.target.id === 'review-form-container' && evt.detail.xhr.status === 400) {
            document.getElementById('write-review-btn').style.display = 'block';
        }
    });

    document.body.addEventListener('reviewCreated', function() {
        const writeBtn = document.getElementById('write-review-btn');
        if (writeBtn) {
            writeBtn.style.display = 'none';
        }
    });
});
