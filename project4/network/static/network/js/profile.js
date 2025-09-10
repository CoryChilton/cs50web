document.addEventListener('DOMContentLoaded', () => {
    const followButton = document.querySelector('#follow-button');
    if (followButton) {
        followButton.addEventListener('click', follow);
    }
    const unfollowButton = document.querySelector('#unfollow-button');
    if (unfollowButton) {
        unfollowButton.addEventListener('click', unfollow);
    }
    const editButtons = document.querySelectorAll('.edit-button');
    editButtons.forEach(eb => {
        eb.addEventListener('click', clickEditButton);
    })
    const editForms = document.querySelectorAll('.edit-form');
    editForms.forEach(ef => {
        ef.addEventListener('submit', submitEditForm);
    });
    

    function follow(e) {
        const userId = this.dataset.userId;
        fetch(`/follow/${userId}`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            location.reload();
        })
    }

    function unfollow(e) {
        const userId = this.dataset.userId;
        fetch(`/unfollow/${userId}`, {
            method: 'POST',
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            location.reload();
        })
    }

    function clickEditButton() {
        form_div = document.querySelector(`.form-div[data-post-id="${this.dataset.postId}"]`);
        post_div = document.querySelector(`.post-div[data-post-id="${this.dataset.postId}"]`);
        textarea = document.querySelector(`.form-div[data-post-id="${this.dataset.postId}"] textarea`);
        content_p = document.querySelector(`.content[data-post-id="${this.dataset.postId}"]`)
        textarea.value = content_p.innerText
        form_div.classList.toggle("hidden");
        post_div.classList.toggle("hidden");
    }

    function submitEditForm(e) {
        e.preventDefault();
        const editForm = new FormData(this);

        fetch(this.action, {
            method: "POST",
            body: editForm,
            headers: {
                "X-CSRFToken": editForm.get('csrfmiddlewaretoken')
            }
        })
        .then(response => response.json())
        .then(result => {
            console.log(result);
            // location.reload();
        })

        contentP = document.querySelector(`.content[data-post-id="${this.dataset.postId}"]`);
        contentP.innerText = editForm.get('content');
        const edit_button = document.querySelector(`.edit-button[data-post-id="${this.dataset.postId}"]`);
        clickEditButton.call(edit_button);

    }
})
