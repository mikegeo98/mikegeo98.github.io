# mikegeo98.github.io

Personal academic page. Plain HTML/CSS/JS, no build step.

## Structure

- `index.html` – all content lives here; edit it directly.
- `css/style.css` – design tokens at the top (`:root`), dark theme below them.
- `js/main.js` – theme toggle and mobile menu only.
- `papers/` – drop PDFs here and link them from the publication entries.
- `img/portrait.jpg` – your photo (square, ~600px). The page shows initials until it exists.
- `cv.pdf` – linked from the header.

## Updating

- News: keep to the latest 4-5 items.
- New paper: add an entry under the right year in Publications (with a `dir` tag), and link it from the matching direction in Research.
- New thesis: add a row under Ongoing in Students; move it to Completed with the year when done.
- CV: replace `cv.pdf`.

## Deploy

```sh
cd /Users/mikeg/Documents/mikegeo98.github.io
git init -b main
git add .
git commit -m "Initial personal page"
gh repo create mikegeo98/mikegeo98.github.io --public --source=. --push
```

Then on GitHub: Settings → Pages → Source: Deploy from branch `main`, folder `/ (root)`.
The site appears at https://mikegeo98.github.io within a minute or two.

## Preview locally

```sh
cd /Users/mikeg/Documents/mikegeo98.github.io && python3 -m http.server 8000
```
