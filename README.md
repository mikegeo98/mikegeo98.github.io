# mikegeo98.github.io

Personal academic page. Plain HTML/CSS/JS, no build step.

## Structure

- `index.html` – all content lives here; edit it directly.
- `css/style.css` – design tokens at the top (`:root`), dark theme below them.
- `js/main.js` – theme toggle and mobile menu only.
- `papers/` – drop PDFs here and link them from the publication entries.
- `img/portrait.jpg` – your photo (square, ~600px). The page shows initials until it exists.
- `cv.pdf` – linked from the header.

## Before publishing

Search `index.html` for `TODO` comments. Remaining ones: portrait, CV, Beyond-research text, two paper PDFs.

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
