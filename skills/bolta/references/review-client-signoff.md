# Client sign-off required: how it behaves

A brand setting: no post is approved, scheduled or posted without a current client yes. Read with [review-client-approval.md](review-client-approval.md) and [review-client-details.md](review-client-details.md).

## Once it is on

- Turning it on pulls every scheduled or approved post without a current client yes back to waiting. The calendar shrinks; that is the setting working, not a fault.
- A post can also be held at the moment it would go out, if it has no current client yes. It returns to waiting.
- An edit to the text, media, destination, or the Pinterest, YouTube or Reddit details after the client said yes voids the yes. So does any change to the post's per-network text or settings (`platform_specific`); sending the same values again does not. A time change does not.
- The refusal code `CLIENT_SIGNOFF_REQUIRED` is not retryable. The fix is to send the post to the client, never to approve again.
- Only the organization owner (the brand owner if there is no organization) can turn it on or off, in the brand's settings in Bolta. Turning it off releases nothing that was held.
- Library posts the team put live directly, without a client review, are exempt.

## What to say

- The calendar shrank after it was turned on: "Turning on client sign-off pulled the scheduled posts without a client yes back to waiting. That's the setting working. Send them to the client from Approvals in Bolta."
- A yes was voided by an edit: "The post changed after the client approved, so their yes no longer counts. Send it to them again."
- Only the time moved: "Moving the time doesn't need a new client yes."

## Always

- Follow the house rules in the Bolta skill.
- Never approve, schedule or post around a client step: send the post to the client instead.
- Turning the setting on or off happens in Bolta, never from here.
