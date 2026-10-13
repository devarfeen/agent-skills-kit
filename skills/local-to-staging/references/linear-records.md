# Linear delivery and assignment records

Zero attribution: never add or leave co-author, AI, tool, or generator attribution in any output.

When reading delivery history or posting a manual-QA assignment on Linear, use readable Markdown instead of HTML control markers.

Read complete `## Delivered` fields PR, Merge commit and Base, and `## Manual QA assignment` fields PR, Merge commit and Staging commit. Commit values are full SHAs. Accept legacy records too. Missing/conflicting fields leave handoff pending; older merge records cannot suppress a returned fix.

Post the deployment/smoke evidence under `## Manual QA assignment` with readable PR, Merge commit and Staging commit fields. Read the saved fields back against the latest delivery and proven deployment. GitHub keeps its existing marker format. This formatting changes no approval, ancestry, deployment or assignment gate.
