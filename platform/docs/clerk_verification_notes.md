# Clerk Verification Notes

On 2026-08-19, a real signed-in Clerk user successfully loaded `/workspace/literature-review`. The client received the authenticated workspace shell, user identity, protected sidebar, and all 15 records from the tRPC-backed literature matrix.

The same user was identified as `researcher`. A request to `/workspace/admin` redirected to `/workspace/literature-review`, confirming that standard research access does not grant administration access.

Administrator verification remains dependent on assigning the signed-in Clerk user `publicMetadata.role = "admin"` in Clerk Dashboard, then repeating the same browser check.

After assigning the metadata role, the same browser session successfully loaded `/workspace/admin`. The Clerk-authenticated sidebar and page correctly identified the user as `admin`, and the administrator tRPC overview rendered the users panel. The persisted PostgreSQL row still displayed the prior `researcher` role, so the identity adapter must synchronize the resolved Clerk role to the local user record for consistent administrator reporting.

After updating the identity adapter, a refreshed administrator session loaded the Administration workspace and the persisted PostgreSQL user row displayed `admin`. This confirms that Clerk public metadata, protected route access, tRPC administration access, and local user reporting are aligned.
