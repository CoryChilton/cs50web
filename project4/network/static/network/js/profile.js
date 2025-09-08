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

    function clickEditButton(e) {
        console.log(this.dataset.postId);
        form_div = document.querySelector(`.form-div[data-post-id="${this.dataset.postId}"]`);
        post_div = document.querySelector(`.post-div[data-post-id="${this.dataset.postId}"]`);
        textarea = document.querySelector(`.form-div[data-post-id="${this.dataset.postId}"] textarea`);
        content_p = document.querySelector(`.content[data-post-id="${this.dataset.postId}"]`)
        textarea.value = content_p.innerText
        form_div.classList.toggle("hidden");
        post_div.classList.toggle("hidden");
    }
})
