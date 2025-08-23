document.addEventListener('DOMContentLoaded', function() {

  // Use buttons to toggle between views
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', compose_email);

  const compose_form = document.querySelector('#compose-form');
  compose_form.addEventListener('submit', function(event) {
    event.preventDefault();
    fetch('/emails', {
      method: 'POST',
      body: JSON.stringify({
        recipients: event.target.querySelector('#compose-recipients').value,
        subject: event.target.querySelector('#compose-subject').value,
        body: event.target.querySelector('#compose-body').value
      })
    })
    .then(response => response.json())
    .then(result => {
        // Print result
        console.log(result);
    });
    load_mailbox('sent');
  })

  // By default, load the inbox
  load_mailbox('inbox');
});



function compose_email() {

  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'block';

  // Clear out composition fields
  document.querySelector('#compose-recipients').value = '';
  document.querySelector('#compose-subject').value = '';
  document.querySelector('#compose-body').value = '';
}

function load_mailbox(mailbox) {
  const emails_view = document.querySelector('#emails-view');

  //clear the mailbox
  document.querySelector('#emails-view').innerHTML = "";
  
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#email-view').style.display = 'none';
  
  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  

  //fetch the latest emails in the appropriate mailbox
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
      // Print emails
      console.log(emails);

      emails.forEach(e => {
        const email_div = document.createElement('div');
        email_div.innerHTML = `Subject: ${e.subject} From: ${e.sender} Timestamp: ${e.timestamp}`;
        email_div.classList.add('email');
        if (e.read){
          email_div.classList.add('read')
        }
        email_div.dataset.id = e.id;
        email_div.addEventListener('click', load_email)
        emails_view.appendChild(email_div);
    });
  });

  function load_email(e) {
    const email_view = document.querySelector('#email-view');
    // clear previous email from view
    email_view.innerHTML = "";

    document.querySelector('#email-view').style.display = 'block';
    document.querySelector('#compose-view').style.display = 'none';
    document.querySelector('#emails-view').style.display = 'none';
    fetch(`/emails/${e.target.dataset.id}`)
    .then(response => response.json())
    .then(email => {
        // Print email
        console.log(email);
        const subject_h1 = document.createElement('h1');
        const sender_p = document.createElement('p');
        const recipients_p = document.createElement('p');
        const timestamp_p = document.createElement('p');
        const body_p = document.createElement('p');
        const archive_btn = document.createElement('button');
        archive_btn.dataset.email_id = email.id;
        archive_btn.dataset.archived = email.archived;
        archive_btn.addEventListener('click', archive);
        const reply_btn = document.createElement('button');
        reply_btn.dataset.email_id = email.id;
        reply_btn.addEventListener('click', reply);

        subject_h1.innerText = email.subject;
        sender_p.innerText = "From: " + email.sender;
        recipients_p.innerText = "To: " + email.recipients;
        timestamp_p.innerText = "Sent at: " + email.timestamp;
        body_p.innerText = "Message: " + email.body;
        archive_btn.innerText = email.archived ? "Unarchive" : "Archive";
        reply_btn.innerText = "Reply";
        email_view.append(subject_h1);
        email_view.append(sender_p);
        email_view.append(recipients_p);
        email_view.append(timestamp_p);
        email_view.append(body_p);
        email_view.append(archive_btn);
        email_view.append(reply_btn);

    });

    // mark the email as read
    fetch(`/emails/${e.target.dataset.id}`, {
      method: 'PUT',
      body: JSON.stringify({
          read: true
      })
    })
  }

  function archive(e) {
    console.log(e.target.dataset.email_id)
    fetch(`/emails/${e.target.dataset.email_id}`, {
      method: 'PUT',
      body: JSON.stringify({
          archived: e.target.dataset.archived === "true" ? false : true
      })
    })

    load_mailbox('inbox');
  }

  function reply(e) {
    console.log(e.target.dataset.email_id);
    fetch(`/emails/${e.target.dataset.email_id}`)
    .then(response => response.json())
    .then(email => {
      compose_email();
      const compose_recipients = document.querySelector('#compose-recipients');
      compose_recipients.value = email.sender;
      const compose_subject = document.querySelector('#compose-subject');
      compose_subject.value = "Re: " + email.subject;
      const compose_body = document.querySelector('#compose-body');
      compose_body.value = `On ${email.timestamp} ${email.sender} wrote: ${email.body}\n------------------------------\n`
    });
    

  }
}