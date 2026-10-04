# Test flow

```text
Authenticated session
        |
        v
Account settings
        |
        v
Danger Zone -> Delete Account
        |
        v
Confirmation modal
        |
        v
Enter correct email
        |
        v
Click final Delete Account
        |
        +---- expected ----> state-changing request -> explicit completion state
        |
        +---- observed ----> no visible completion; dialog remains
```
