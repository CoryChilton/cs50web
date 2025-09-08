document.addEventListener('DOMContentLoaded', () => {
    const followButton = document.querySelector('#follow-button');
    if (followButton) {
        followButton.addEventListener('click', follow);
    }
    const unfollowButton = document.querySelector('#unfollow-button');
    if (unfollowButton) {
        unfollowButton.addEventListener('click', unfollow);
    }

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
})
