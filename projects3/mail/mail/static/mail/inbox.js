document.addEventListener('DOMContentLoaded', function() {
  // Use buttons to toggle between views
  // let mail = null;
  document.querySelector('#inbox').addEventListener('click', () => load_mailbox('inbox'));
  document.querySelector('#sent').addEventListener('click', () => load_mailbox('sent'));
  document.querySelector('#archived').addEventListener('click', () => load_mailbox('archive'));
  document.querySelector('#compose').addEventListener('click', () => compose_email(''));

  // By default, load the inbox
  load_mailbox('inbox');
});

function compose_email(mail) {
  // Show compose view and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#open-email-view').style.display='none';
  document.querySelector('#compose-view').style.display = 'block';
  
  console.log('compose email: '+ (mail !== ''));
  console.log(mail)
  // const
  const recipients = (mail !== '') ? (mail.recipients.join(', ')) : ('');
  var subject = (mail !== '') ? (mail.subject) : ('');
  var body = (mail !== '') ? (mail.body) : ('');

  // for reply adding 'Re: subject'
  if (mail !== '') {
    subject = (subject.substring(0,3).toUpperCase() =='RE:') ? (subject) : ('RE: '+subject);
    body = `On ${mail.timestamp} ${recipients} wrote:\n ${body}\n`;
  }

  // set values in form for each case
  document.querySelector('#compose-recipients').value = recipients;
  document.querySelector('#compose-subject').value = subject;
  document.querySelector('#compose-body').value = body;

  // send email
  document.querySelector('#compose-form').onsubmit = send_mail;
}

function load_mailbox(mailbox) {
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'block';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#open-email-view').style.display='none';

  // Show the mailbox name
  document.querySelector('#emails-view').innerHTML = `<h3>${mailbox.charAt(0).toUpperCase() + mailbox.slice(1)}</h3>`;

  // adding my changes
  console.log(`${mailbox}`)
  
  fetch(`/emails/${mailbox}`)
  .then(response => response.json())
  .then(emails => {
    console.log(emails);

    for(var k in emails) {  
      const id = emails[k].id;
      const sender = emails[k].sender;
      const subject = emails[k].subject;
      const timestamp = emails[k].timestamp;

      // creating new element and adding class
      let element = document.createElement('div');
      element.classList.add('row');
      element.style.cssText = (emails[k].read) ? ("border: double; background-color: gray;") : ("border: double; background-color: white;");

      // create div's to insert
      element.innerHTML = `<div class="col-sm"><b>${sender}</b></div>`;
      element.innerHTML +=`<div class="col-sm">${subject}</div>`;
      element.innerHTML +=`<div class="col-sm">${timestamp}</div>`;

      element.addEventListener('click', () => open_email(id,mailbox));
      // inserting new data 
      document.querySelector('#emails-view').append(element);
      }
  });
}

// my functions

function send_mail() {
  // get values from form
  const recipients = document.querySelector('#compose-recipients').value;
  const subject = document.querySelector('#compose-subject').value;
  const body = document.querySelector('#compose-body').value;

  fetch('/emails', {
    method: 'POST',
    body: JSON.stringify({
        recipients: recipients,
        subject: subject,
        body: body
    })
  })
  .then(response => response.json())
  .then(result => {
      // Print result
      console.log(result);
  });
  // reload page - index
  location.reload();
}

function open_email(mail_id,mailbox) {
  console.log('opening email: ' + mail_id + 'with type:'+ mailbox);
  // Show the mailbox and hide other views
  document.querySelector('#emails-view').style.display = 'none';
  document.querySelector('#compose-view').style.display = 'none';
  document.querySelector('#open-email-view').style.display='block';

  // view of email
  fetch(`/emails/${mail_id}`)
  .then(response => response.json())
  .then(email => {
      // Print email
      console.log(email);
      // change state of email
      update_email_state(email,'read');
      let mail = email;
      // const
      const subject = email.subject;
      const from = email.sender;
      const to = email.recipients.join(', ');
      const body = email.body;
      const timestamp = email.timestamp;

      // adding new elements
      let element = document.querySelector('#open-email-view > #email-document');
      element.innerHTML = `<h3><b>${subject.toUpperCase()}</b></h3>`;
      element.innerHTML += `<h5><b>From: </b>${from}</h5>`;
      element.innerHTML += `<h5><b>To: </b>${to}</h5>`;
      element.innerHTML += `<p style="text-align: right;">${timestamp}</p>`;
      element.innerHTML += '<hr>';
      element.innerHTML += `<div><p>${body}</p></div>`;

      // buttons functions
      document.querySelector('#reply').addEventListener('click', () => compose_email(email));
      // archive button
      if ( mailbox !== 'sent') {
        document.querySelector('#archive').style.display = 'block';
        document.querySelector('#archive').innerHTML= (email.archived) ? ('Unarchived') : ('Archived');
        document.querySelector('#archive').addEventListener('click', () => update_email_state(email,'archived'));
      }else{
        document.querySelector('#archive').style.display = 'none';
      }
    });
    
  // document.querySelector('#reply').onclick = compose_email(mail);
}


function update_email_state(mail,type) {
  console.log('update email state: '+type);
  if (type == 'archived'){
    const bool_archived = (mail.archived) ? (false) : (true);

    fetch(`/emails/${mail.id}`, {
      method: 'PUT',
      body: JSON.stringify({archived: bool_archived})
    })

    // reload page
    location.reload();
  }

  if (type == 'read') {
    console.log('read process')
    fetch(`/emails/${mail.id}`, {
      method: 'PUT',
      body: JSON.stringify({read: true})
    })
  }
}


