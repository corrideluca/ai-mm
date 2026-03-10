Publish a package to npm registry.

Steps:
1. Check if npm is authenticated: `npm whoami`
2. If not authenticated, run `npm login --auth-type=web` and tell the user to complete browser auth
3. Navigate to the package directory
4. Run `npm publish`
5. Verify the package is live: `npm view <package-name>`
6. Update memory/content.md with the published package
7. Tweet about the new package launch

If auth fails, remind the user they need to enter the OTP from their email in the browser.
