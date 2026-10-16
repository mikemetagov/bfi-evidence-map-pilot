# Hosting the pilot site behind a login (Cloudflare Pages + Access)

GitHub cannot host this site privately on a free account: GitHub Pages works only from public repositories on the free plan, and only GitHub Enterprise Cloud can restrict who sees a Pages site. Cloudflare Pages can build the site from this private repository, and Cloudflare Access can require an emailed one-time code before anyone sees it. Access is free for small teams.

The steps below keep the site closed from the start: the first build is set to fail on purpose, so nothing is published until the login is in place.

## 1. Create a Cloudflare account

1. Sign up at [dash.cloudflare.com](https://dash.cloudflare.com/sign-up) with your Metagov email.
2. Verify the email.

## 2. Connect the repository (first build fails on purpose)

1. In the Cloudflare dashboard, go to **Workers & Pages**.
2. Click **Create application**, then the **Pages** tab, then **Connect to Git**.
3. Choose **GitHub** and click **Install & Authorize**. When GitHub asks which repositories to allow, choose **Only select repositories** and pick `bfi-evidence-map-pilot`.
4. Select `bfi-evidence-map-pilot` and click **Begin setup**.
5. Fill in **Set up builds and deployments**:
   - **Project name:** pick something hard to guess, for example `bfi-pilot-7q4m`. It becomes the address `https://bfi-pilot-7q4m.pages.dev` and cannot be changed later.
   - **Production branch:** `main`
   - **Framework preset:** `None`
   - **Build command:** `exit 1`   (temporary, so the first build fails and publishes nothing)
   - **Build output directory:** `site`
6. Click **Save and Deploy**. The build fails. That is expected.

## 3. Turn on the login

1. Open the Pages project, go to **Settings**, and click **Enable access policy**. Cloudflare may ask you to set up Zero Trust first: choose a team name and the **Free** plan. It may ask for payment details even for the free plan.
2. That first policy covers preview addresses only. To also cover the main address:
   1. On the project's **Settings** page, select **Manage** on the Access policy.
   2. In **Access > Applications**, select the project, then **Configure**.
   3. Under **Public hostname**, delete the `*` in the **Subdomain** field and click **Save**. If an error appears, change the **Application name** slightly and save again.
   4. Go back to the project's **Settings** and click **Enable access policy** again, so preview addresses are covered too.
   5. Check that there are now two Access applications: one for `bfi-pilot-7q4m.pages.dev` and one for `*.bfi-pilot-7q4m.pages.dev`.
3. Set who can sign in, in each of the two applications: open **Policies** and edit the Allow policy. Under **Include**, choose **Emails** and add each person, for example you and named GSR Foundation contacts. You can also use **Emails ending in** with `@metagov.org`. Save.

## 4. Switch on the real build

1. In the Pages project, go to **Settings > Build** and edit the build configuration.
2. Set **Build command** to:
   ```
   pip install -r requirements.txt && python scripts/build.py && zensical build --clean
   ```
3. Under **Variables and secrets**, add `PYTHON_VERSION` with the value `3.12`.
4. Go to **Deployments** and click **Retry deployment** on the failed build, or push any change to the repository.

## 5. Test the login

1. Open `https://bfi-pilot-7q4m.pages.dev` in a private browser window. You should see a Cloudflare sign-in page, not the site.
2. Enter an allowed email address, then the code Cloudflare emails you. The site should open.
3. Try an email address that is not on the list. It should be refused.
4. Open a preview address, shown under **Deployments**, in a private window. It should also ask for sign-in.

From then on, every commit to `main` rebuilds the site within a few minutes, and only the people on the list can see it.

## Notes

- **Removing someone:** delete their email from both policies.
- **Custom address:** if you later add an address such as `pilot.metagov.org`, add an Access application for that address too. Without it, the login page appears but does not work there.
- **If the build fails:** open the deployment log in Cloudflare. The same data problems shown on the GitHub Actions tab appear there.
