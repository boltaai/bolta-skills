# Send for approval to a person

The user wants someone in particular to approve drafts: "send these to Sam for approval", "get the client's OK on these". Bolta emails that person, and reminds them 2 and 5 days later if they haven't answered.

## The steps

1. **Which posts.** The drafts just shown, or the ones the user names. Only posts not yet approved: drafts, Needs Revision, or waiting for the team. Up to 50 at a time.
2. **Who.** No one named ("send these for approval"): ask who should approve them. Never pick someone yourself.
3. **Find them.** `list-workspace-members`. Only people with `can_receive_approval_requests` true can be picked: the brand's client reviewers (`role` reviewer) and creators. Owners and admins approve in the team list instead: for them, `submit-for-review` without `reviewer_ids`. Two people match a name, or none: show the names and ask. Someone not on the brand is invited from People & access in Bolta first ([agency setup](review-client-howto.md)).
4. **Show and ask.** Number the posts (account, full text) and name the people: "Send these 3 to Terry for approval? Terry gets an email." Wait for a yes in the user's latest message.
5. **Send.** One `submit-for-review` with `post_ids`, `reviewer_ids` (the ids from step 3), a short `title` if the user gave one, and `note` for anything the person should read. `notify_email` false only when the user says no email.
6. **Tell them** what came back: who it went to (`sent_to`), whether they get an email (`email_notification`), reminders after 2 and 5 days, and that each post they approve is scheduled ([client approval](review-client-approval.md)). Show `dashboard_url`.

## When it is refused

Nothing was sent; follow `what_to_do`. `invalid_recipient`: that person can't be picked (an owner, an admin, a viewer, or someone not on this brand). `already_in_review`: a post is already with someone; leave it out. `self_review`: the user can't send to themselves. A post with `quality_block`: fix it with `save-post`, then send again.

## Always

- Follow the house rules in the Bolta skill.
- It reaches a real person: send only after the user saw the posts and the names and said yes. Never with nobody present (a scheduled task).
- Never send to a person in place of approving, or to get round a no.
