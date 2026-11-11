# Client approval for an agency, end to end

Read when an agency or team wants a client to sign off, or a client step refuses something. How a request works: [review-client-approval.md](review-client-approval.md). What the client can do: [review-client-details.md](review-client-details.md). Worked: [client-approval-agency](../examples/client-approval-agency.json).

## Choosing the setup

Advice from how Bolta behaves; the user decides.

- **Require sign-off** only when no post may go out without the client's yes (a contract, a regulated client). It is the "Client sign-off required" switch in the brand's settings, Approvals section, and only the organization owner can flip it. Turning it on pulls every scheduled post without a client yes back to waiting, so switch it on before scheduling the month, then send those posts. Turning it off releases nothing held.
- **Without it**, client review is per post: send what the client should see. While a post waits on the client, the team can't approve it around them.
- **Recipients:** invite the client as a reviewer (no seat) in the brand's People & access. Mark someone required only when their own yes is a must: each required reviewer has to approve the same version, while one change request or dismissal from anyone settles it.
- **Reminders** go out by themselves 2 and 5 days after the send, only to people still owed an answer, and stop after 14 days. After that, a personal nudge or a resend.
- **Settle copy and time first.** The client sees the time. Any edit while the client hasn't answered, a new time included, makes the request stale and it must go again. After their yes a time move is fine.
- **A steady flow:** a Bolta routine can send each run's drafts straight to the client, keeping about N waiting there: no team pass, no reminders, a daily summary to the team. It needs a client reviewer on the brand ([routine-outputs.md](routine-outputs.md)).

## From here, step by step

1. Look once. Teammates' names to ids: `list-workspace-members` (it never lists client reviewers: ask who the client is). Not on this app: use the names.
2. Write the drafts ([post](post.md)) and show them in full.
3. Send them: "Send these to the client from Approvals in Bolta: bolta.ai/dashboard/approvals. Pick the client, mark who must sign off." A straight-to-client routine or a Library post marked "send to the client" are the two ways from here ([client approval](review-client-approval.md)), each only on a yes naming the client.
4. Follow up with `get-post` per post (`client_signoff`); review list rows don't show it.
5. After the client's yes the post is scheduled; read the times back with `list-workspace-posts` and their `account_ids`. If the sender's own setting approves without scheduling, a hand-made post with no time still needs one.

Later drafts from the same Bolta routine or Library fill join its open request without a second email; nothing else can be added to a request already sent.

## Refusals

| Refusal | Say or do |
|-|-|
| awaiting client sign-off, `client_review_pending` | "It's with the client." Wait, or withdraw it in Approvals. |
| `CLIENT_SIGNOFF_REQUIRED` | "This brand needs the client's yes first. Send it from Approvals." Not retryable. |
| stale review | "It changed since the client saw it." Show the new version; it has to be sent again. |
| a client's Approve refused (too long, out of credits) | [review-client-details.md](review-client-details.md). |

## Always

- Follow the house rules in the Bolta skill.
- Never move a time, edit or approve a post the client hasn't answered without saying it voids the request.
- Never claim a send, reminder or withdrawal was done from here.
