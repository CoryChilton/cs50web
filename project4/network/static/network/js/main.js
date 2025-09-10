document.addEventListener('DOMContentLoaded', () => {
    const likeForms = document.querySelectorAll('.like-form');
    likeForms.forEach(lf => {
        lf.addEventListener('submit', submitLikeForm);
    })

    function submitLikeForm(e) {
        e.preventDefault();

        const likeForm = new FormData(this);
        fetch(this.action, {
            method: "POST",
            body: likeForm,
            headers: {
                "X-CSRFToken": likeForm.get('csrfmiddlewaretoken')
            }
        })
        .then(response => {
            if (response.ok) {
                addLike(this.dataset.postId)
            }
            return response.json()
        })
        .then(result => {
            console.log(result);
        })
        
    }

    function addLike(postId) {
        const likeCountSpan = document.querySelector(`.like-count[data-post-id="${postId}"]`);
        let likeCount = parseInt(likeCountSpan.innerText);
        likeCount += 1;
        console.log(likeCount);
        likeCountSpan.innerText = likeCount;
    }

});