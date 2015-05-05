Claims extension
=========================================
* **Claim numbers**
    * Generates claim numbers for all existing claims
    * Tracks the current claim number and assigns an unique claim number for all new claims
    * Starts from 10001 by default, can be customized in data XML file

* **Views and Visualization**
    * Removes settled and rejected claims from (default) tree view
    * Extends the claims search to partner names, claim number and claim description
    * Adds the first-level child partner claims to partner view claims-button count
        * TODO: Add a recursive claims count for all children
    * Adds claim coloring and bolding for claims depending on their state (treeview)
    * Overwrites the claim tree view to colorize claims with new messages and past deadlines
    * Splits the 'Claims' submenu element to 'My claims' and 'All claims' for easier access

* **Email and Messaging**
    * Adds message history to mails sent by claims module
    * Adds a company-spesific message header to mails sent by claims module
    * Adds a company-spesific message footer to mails sent by claims module
    * Overrides notify_email when sending helpdesk-messages: helpdesk will send mails to partners even if they have receive messages-option disabled
    * Has a fallback claims matching by claim number in the subject

* **Multi-company**
    * Adds a company for claims
    * Adds a company for fetchmail servers
    * Adds a company-spesific options for claims

* **Workflow and Stages**
    * Adds stage dates for start date, waiting date, settled date and rejected date
    * Saves latest stage changes: start date, waiting date, settled date, rejected date.
        * NOTE: The timestamp only holds the latest stage change. If the stage is reverted, the current timestamp is overwritten
    * Reopens a claim if a new message is received on a closed claim
    * Marks stage changer new->started as responsible if not set
    * Updates followers on partner change
* **Other**
    * Adds a possibility for inline attachments
    * Adds a partner email format validation
    * Adds a "killswitch" for sending autoreplies: autoreply won't be sent if a partner has three open claims within the last 15 minutes