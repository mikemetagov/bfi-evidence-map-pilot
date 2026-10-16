# Blockchain for Impact Funding Evidence Map – Pilot (restricted)

**Restricted: GSR Foundation and Metagov only.** This private repository holds the pilot protocol, outputs O1–O19, the coded data, the evidence map and the visuals. Keep it private. The design is posted publicly only after Gate 0 approval, from a separate public repository.

## What is where

| Location | What it holds | Edit? |
|---|---|---|
| `docs/protocol/files/` | Pilot design report versions (PDF and Word) | Yes, add each new version |
| `docs/outputs/<section>/` | Output files, in the same 13 sections as the Google Drive folder (`00_Admin_and_Approvals` … `12_Full_Scope`) | Yes, upload files here |
| `data/outputs_register.csv` | Status, file path and date for O1–O19. Drives the Outputs pages. | Yes |
| `data/cases.csv` | One row per use case | Yes, at Gate 4 (O12) |
| `data/coding.csv` | One row per use case and outcome domain, with evidence level, quote and source | Yes, at Gate 4 (O12) |
| `data/codebook.csv` | Draft codebook v0.1 (protocol Annex B): allowed values, labels, definitions | Only at approved codebook versions |
| `docs/visuals/` | Visual pack V1–V7 (O15) | Yes |
| `docs/gates/index.md` | Gate and deviations log (O18) | Yes |
| `docs/index.md` | Home page, including the gate status table | Yes |
| `docs/map/eppi-mapper/index.html` | EPPI-Mapper version of the map | Replace after Gate 4 |
| `scripts/build.py` | Checks the data and generates map data, outputs pages and downloads | Rarely |
| `.github/workflows/check.yml` | Runs the checks and builds the site on every change | Rarely |
| `HOSTING.md` | How to host the site behind a login with Cloudflare | Read once |

Pages under `docs/outputs/` (the `index.md` files) and `docs/map/map-data.json` are generated. Edit the register and data files, not those pages.

## Adding an output file

1. Open the section folder, for example `docs/outputs/02_Sampling/`, then click **Add file > Upload files**.
2. Use the Drive naming pattern, for example `20261020_O2_Sampling-Frame_v1.0.xlsx`. PDFs open in the browser; other files download.
3. Commit.
4. Open `data/outputs_register.csv` and edit the output's row: set `status` (for example `Final v1.0`), `file` (path from `docs/`, for example `outputs/02_Sampling/20261020_O2_Sampling-Frame_v1.0.xlsx`) and `updated` (YYYY-MM-DD). Commit.

Every file in a section folder is also listed automatically on that section's page.

## Adding the coded data (Gate 4)

1. Paste the final dataset into `data/cases.csv` and `data/coding.csv`, keeping the column headings. Use the codes in `data/codebook.csv` (for example `1`–`6` or `none` for domains, `A`–`F` for outcomes, `L1`–`L5` for evidence levels).
2. Commit. The **Check data and build site** run on the Actions tab either passes (green tick) or stops with a list of problems and line numbers.
3. If the codebook changes at an approved version, update `data/codebook.csv` at the same time and note it in the changelog.

## Checking a change

Every commit starts a run on the **Actions** tab:
- **Green tick**: the data passed every check and the site was built. The built site is attached to the run under **Artifacts** as `pilot-site` for 30 days.
- **Red X**: open the run, then **build**, then **Check data and build generated files** to see each problem.

## Size limits

- GitHub's web upload accepts files up to 25 MB, and GitHub rejects any file over 100 MB.
- Cloudflare Pages also limits each file to 25 MB. Keep large raw files (for example web archives) on the restricted Drive and link to them.

## Previewing on your own computer (optional)

```sh
pip install -r requirements.txt
python scripts/build.py
zensical serve
```
