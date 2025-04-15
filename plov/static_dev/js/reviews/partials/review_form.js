function showRatingError() {
    let starContainer = document.querySelector('.star-rating');
    starContainer.classList.add('border', 'border-danger', 'rounded', 'p-2');
    starContainer.style.animation = 'shake 0.5s';

    let ratingError = document.querySelector('.rating-error');
    ratingError.classList.remove('d-none');
}

function showContentError() {
    let contentField = document.querySelector('#content-input');
    contentField.classList.add('is-invalid');
    contentField.focus();

    let contentError = document.querySelector('.content-error');
    contentError.classList.remove('d-none');
}

function clearRatingError() {
    let starContainer = document.querySelector('.star-rating');
    starContainer.classList.remove('border', 'border-danger', 'rounded', 'p-2');
    starContainer.style.animation = '';

    let ratingError = document.querySelector('.rating-error');
    ratingError.classList.add('d-none');
}

document.querySelectorAll('.star-rating input').forEach(radio => {
    radio.addEventListener('change', clearRatingError);
});

function clearContentError() {
    let contentField = document.querySelector('#content-input');
    contentField.classList.remove('is-invalid');

    let contentError = document.querySelector('.content-error');
    contentError.classList.add('d-none');
}

function resetForm() {
    clearRatingError();
    clearContentError();
    document.querySelector('#review-form').reset();
    document.querySelector('#review-form-container').style.display = 'none';
}

function submitReviewForm() {
    let form = document.querySelector('#review-form');
    let rating = form.querySelector('input[name="rating"]:checked');
    let content = form.querySelector('textarea[name="content"]').value.trim();

    clearRatingError();
    clearContentError();

    if (!rating || !content) {
        if (!rating) {
            showRatingError();
        }
        if (!content) {
            showContentError();
        }
        return;
    }

    let formData = new FormData(form);
    let headers = {
        'X-CSRFToken': form.querySelector('[name=csrfmiddlewaretoken]').value,
        'X-Requested-With': 'XMLHttpRequest'
    };
    htmx.ajax('POST', form.getAttribute('hx-post'), {
        values: Object.fromEntries(formData),
        target: form.getAttribute('hx-target'),
        swap: form.getAttribute('hx-swap'),
        headers: headers
    });

    document.querySelector('#review-form-container').style.display = 'none';
}